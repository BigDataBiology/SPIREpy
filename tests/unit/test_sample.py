import unittest
from unittest.mock import patch, MagicMock, call
import polars as pl
import pandas as pd
from polars.testing import assert_frame_equal

from spirepy import Sample, Study


class TestSample(unittest.TestCase):
    def setUp(self):
        """Set up a common Sample instance for all tests."""
        self.sample_id = "SAMPLE_01"
        self.study = Study(name="STUDY_A")
        self.sample = Sample(id=self.sample_id, study=self.study)

    def test_initialization_and_str(self):
        """Tests the __init__, __str__, and __repr__ methods."""
        self.assertEqual(self.sample.id, self.sample_id)
        self.assertEqual(self.sample.study, self.study)
        self.assertIsNone(self.sample._metadata)
        self.assertIsNone(self.sample._mags)
        self.assertIsNone(self.sample._eggnog_data)
        self.assertEqual(self.sample._amr_annotations, {})

        expected_str = f"Sample id: {self.sample_id} \tStudy: {self.study.name}"
        self.assertEqual(str(self.sample), expected_str)
        self.assertEqual(repr(self.sample), expected_str)

    @patch("spirepy.sample.pl.read_csv")
    def test_get_metadata(self, mock_read_csv: MagicMock):
        """Tests get_metadata for successful data retrieval and caching."""
        mock_data = pl.DataFrame({"sample_id": [self.sample_id]})
        mock_read_csv.return_value = mock_data

        # First call - should fetch data
        result1 = self.sample.get_metadata()
        expected_url = f"https://spire.embl.de/spire/api/sample/{self.sample_id}?format=tsv"
        mock_read_csv.assert_called_once_with(expected_url, separator="\t")
        assert_frame_equal(result1, mock_data)

        # Second call - should use cache
        result2 = self.sample.get_metadata()
        mock_read_csv.assert_called_once()  # Should still be called only once
        assert_frame_equal(result2, mock_data)

    @patch("spirepy.sample.genome_metadata")
    def test_get_mags(
        self,  mock_genome_metadata: MagicMock
    ):
        """Tests get_mags for data processing and caching."""
        # Mock input data
        mock_genome_data = pl.DataFrame(
            {
                "derived_from_sample": [self.sample_id, "OTHER_SAMPLE", self.sample_id],
                "spire_id": ["MAG_A", "MAG_B", "MAG_C"],
                "quality": [90, 95, 88],
            }
        )
        mock_genome_metadata.return_value = mock_genome_data

        # Expected result after filtering
        expected_mags = pl.DataFrame(
            {
                "derived_from_sample": [self.sample_id, self.sample_id],
                "spire_id": ["MAG_A", "MAG_C"],
                "quality": [90, 88],
            }
        )

        # First call - should process data
        result1 = self.sample.get_mags()
        mock_genome_metadata.assert_called_once()
        assert_frame_equal(result1, expected_mags)

        # Second call - should use cache
        result2 = self.sample.get_mags()
        mock_genome_metadata.assert_called_once()
        assert_frame_equal(result2, expected_mags)

    @patch("pandas.read_csv")
    def test_get_eggnog_data(self, mock_read_csv: MagicMock):
        """Tests get_eggnog_data for data retrieval and caching."""
        mock_df = pd.DataFrame({"gene": ["gene1"], "annotation": ["annot1"]})
        mock_read_csv.return_value = mock_df
        expected_data = pl.from_pandas(mock_df)

        # First call
        result1 = self.sample.get_eggnog_data()
        expected_url = f"https://spire.embl.de/download_eggnog/{self.sample_id}"
        mock_read_csv.assert_called_once_with(
            expected_url,
            sep="\t",
            skiprows=4,
            skipfooter=3,
            compression="gzip",
            engine="python",
        )
        assert_frame_equal(result1, expected_data)

        # Second call
        result2 = self.sample.get_eggnog_data()
        mock_read_csv.assert_called_once()
        assert_frame_equal(result2, expected_data)

    @patch("spirepy.sample.pl.read_csv")
    def test_get_amr_annotations(self, mock_read_csv: MagicMock):
        """Tests get_amr_annotations for all modes, caching, and invalid input."""
        mock_data = pl.DataFrame({"gene": ["gene_amr"], "resistance": ["drug_x"]})
        mock_read_csv.return_value = mock_data

        # Test 'deeparg' mode (default)
        result_deeparg = self.sample.get_amr_annotations(mode="deeparg")
        expected_url_deeparg = (
            f"https://spire.embl.de/download_deeparg/{self.sample_id}"
        )
        mock_read_csv.assert_called_with(expected_url_deeparg, separator="\t")
        assert_frame_equal(result_deeparg, mock_data)

        # Test caching for the same mode
        self.sample.get_amr_annotations(mode="deeparg")
        self.assertEqual(mock_read_csv.call_count, 1)

        # Test 'megares' mode - should be a new call
        result_megares = self.sample.get_amr_annotations(mode="megares")
        expected_url_megares = (
            f"https://spire.embl.de/download_abricate_megares/{self.sample_id}"
        )
        self.assertEqual(mock_read_csv.call_count, 2)
        mock_read_csv.assert_called_with(expected_url_megares, separator="\t")
        assert_frame_equal(result_megares, mock_data)

        # Test 'vfdb' mode - should be a new call
        result_vfdb = self.sample.get_amr_annotations(mode="vfdb")
        expected_url_vfdb = (
            f"https://spire.embl.de/download_abricate_vfdb/{self.sample_id}"
        )
        self.assertEqual(mock_read_csv.call_count, 3)
        mock_read_csv.assert_called_with(expected_url_vfdb, separator="\t")
        assert_frame_equal(result_vfdb, mock_data)

        # Verify all results are cached correctly
        self.assertEqual(len(self.sample._amr_annotations), 3)
        self.assertIn("deeparg", self.sample._amr_annotations)
        self.assertIn("megares", self.sample._amr_annotations)
        self.assertIn("vfdb", self.sample._amr_annotations)

    @patch("spirepy.sample.logger.error")
    def test_get_amr_annotations_invalid_mode(self, mock_logger_error: MagicMock):
        """Tests that an invalid mode returns None and logs an error."""
        result = self.sample.get_amr_annotations(mode="invalid_mode")
        self.assertIsNone(result)
        mock_logger_error.assert_called_once_with(
            "Invalid option, please choose one of the following: deeparg, megares, vfdb"
        )

    @patch("spirepy.sample.urllib.request.urlretrieve")
    @patch("spirepy.sample.os.makedirs")
    @patch.object(Sample, "get_mags")
    def test_download_mags(
        self,
        mock_get_mags: MagicMock,
        mock_makedirs: MagicMock,
        mock_urlretrieve: MagicMock,
    ):
        """Tests the download_mags functionality."""
        output_folder = "/fake/dir"
        mock_mags_data = pl.DataFrame({"spire_id": ["MAG_1", "MAG_2"]})
        mock_get_mags.return_value = mock_mags_data

        self.sample.download_mags(out_folder=output_folder)

        # Check that the output folder is created
        mock_makedirs.assert_called_once_with(output_folder, exist_ok=True)

        # Check that urlretrieve is called for each MAG
        expected_calls = [
            call(
                f"https://spire.embl.de/download_file/MAG_1",
                f"{output_folder}/MAG_1.fa.gz",
            ),
            call(
                f"https://spire.embl.de/download_file/MAG_2",
                f"{output_folder}/MAG_2.fa.gz",
            ),
        ]
        mock_urlretrieve.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_urlretrieve.call_count, 2)

    @patch("spirepy.sample.urllib.request.urlretrieve")
    @patch("spirepy.sample.os.makedirs")
    @patch.object(Sample, "get_mags")
    def test_download_mags_no_mags(
        self,
        mock_get_mags: MagicMock,
        mock_makedirs: MagicMock,
        mock_urlretrieve: MagicMock,
    ):
        """Tests that no downloads are attempted if there are no MAGs."""
        output_folder = "/fake/dir"
        # Mock get_mags to return an empty DataFrame
        mock_get_mags.return_value = pl.DataFrame({"spire_id": []})

        self.sample.download_mags(out_folder=output_folder)

        # The directory should still be created
        mock_makedirs.assert_called_once_with(output_folder, exist_ok=True)
        # No download calls should be made
        mock_urlretrieve.assert_not_called()


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
