import unittest
from unittest.mock import patch, MagicMock
import polars as pl
from polars.testing import assert_frame_equal

from spirepy import Study, Sample


class TestStudy(unittest.TestCase):
    def setUp(self):
        """Set up a common Study instance for all tests."""
        self.study_name = "STUDY_XYZ"
        self.study = Study(name=self.study_name)

    def test_initialization(self):
        """Tests that the Study object is initialized correctly."""
        self.assertEqual(self.study.name, self.study_name)
        self.assertIsNone(self.study._metadata)
        self.assertIsNone(self.study._samples)
        self.assertIsNone(self.study._mags)

    @patch("spirepy.study.pl.read_csv")
    def test_get_metadata(self, mock_read_csv: MagicMock):
        """Tests metadata retrieval and caching."""
        mock_data = pl.DataFrame(
            {"study_id": [self.study_name], "sample_id": ["sample1"]}
        )
        mock_read_csv.return_value = mock_data

        # First call should fetch data
        result1 = self.study.get_metadata()
        expected_url = f"https://spire.embl.de/spire/api/study/{self.study_name}?format=tsv"
        mock_read_csv.assert_called_once_with(expected_url, separator="\t")
        assert_frame_equal(result1, mock_data)

        # Second call should use the cache
        result2 = self.study.get_metadata()
        mock_read_csv.assert_called_once()  # Should not be called again
        assert_frame_equal(result2, mock_data)

    @patch.object(Study, "get_metadata")
    def test_get_samples(self, mock_get_metadata: MagicMock):
        """Tests the creation of Sample objects and caching."""
        mock_metadata = pl.DataFrame({"sample_id": ["sample_A", "sample_B"]})
        mock_get_metadata.return_value = mock_metadata

        # First call should create Sample objects
        samples1 = self.study.get_samples()
        mock_get_metadata.assert_called_once()
        self.assertEqual(len(samples1), 2)
        self.assertIsInstance(samples1[0], Sample)
        self.assertEqual(samples1[0].id, "sample_A")
        self.assertEqual(samples1[0].study, self.study)  # Check back-reference
        self.assertEqual(samples1[1].id, "sample_B")

        # Second call should use the cache
        samples2 = self.study.get_samples()
        mock_get_metadata.assert_called_once()  # Should not be called again
        self.assertIs(samples1, samples2)  # Should be the exact same list object

    @patch("spirepy.study.genome_metadata")
    @patch.object(Study, "get_metadata")
    def test_get_mags(
        self, mock_get_metadata: MagicMock, mock_genome_metadata: MagicMock
    ):
        """Tests MAG filtering and caching."""
        # Mock the study's metadata
        mock_study_samples = ["sample_1", "sample_2"]
        mock_get_metadata.return_value = pl.DataFrame({"sample_id": mock_study_samples})

        # Mock the global genome metadata
        mock_all_genomes = pl.DataFrame(
            {
                "mag_id": ["MAG_A", "MAG_B", "MAG_C"],
                "derived_from_sample": ["sample_1", "sample_3", "sample_2"],
            }
        )
        mock_genome_metadata.return_value = mock_all_genomes

        # Define the expected filtered result
        expected_mags = pl.DataFrame(
            {
                "mag_id": ["MAG_A", "MAG_C"],
                "derived_from_sample": ["sample_1", "sample_2"],
            }
        )

        # First call should fetch and filter
        result1 = self.study.get_mags()
        mock_get_metadata.assert_called_once()
        mock_genome_metadata.assert_called_once()
        assert_frame_equal(result1, expected_mags)

        # Second call should use the cache
        result2 = self.study.get_mags()
        mock_get_metadata.assert_called_once()
        mock_genome_metadata.assert_called_once()
        assert_frame_equal(result2, expected_mags)

    @patch("spirepy.study.tarfile.open")
    @patch("spirepy.study.os.makedirs")
    @patch("spirepy.study.urllib.request.urlretrieve")
    @patch("spirepy.study.tempfile.TemporaryDirectory")
    def test_download_mags(
        self,
        mock_tempdir: MagicMock,
        mock_urlretrieve: MagicMock,
        mock_makedirs: MagicMock,
        mock_tar_open: MagicMock,
    ):
        """Tests the entire MAG download and extraction process."""
        output_dir = "/path/to/output"
        fake_temp_dir = "/tmp/fake_dir"

        # Configure the TemporaryDirectory mock
        mock_tempdir.return_value.__enter__.return_value = fake_temp_dir

        # Configure the tarfile.open mock
        mock_tar_object = MagicMock()
        mock_tar_open.return_value.__enter__.return_value = mock_tar_object

        # Execute the method
        self.study.download_mags(output=output_dir)

        # 1. Check that the download was called correctly
        expected_url = f"https://swifter.embl.de/~fullam/spire/compiled/{self.study_name}_spire_v1_MAGs.tar"
        expected_tar_path = f"{fake_temp_dir}/{self.study_name}_mags.tar"
        mock_urlretrieve.assert_called_once_with(expected_url, expected_tar_path)

        # 2. Check that the output directory was created
        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)

        # 3. Check that the tar file was opened
        mock_tar_open.assert_called_once_with(expected_tar_path)

        # 4. Check that the contents were extracted to the correct location
        expected_extract_path = f"{output_dir}/mags"
        mock_tar_object.extractall.assert_called_once_with(expected_extract_path)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
