import unittest
from unittest.mock import patch, MagicMock

from spirepy.cli.spire import main


class TestSpireCliMain(unittest.TestCase):
    @patch("spirepy.cli.spire.maincall")
    @patch("spirepy.cli.spire.argparse.ArgumentParser.parse_args")
    @patch("spirepy.cli.spire.Sample")
    def test_main_parses_sample_view_args(
        self, MockSample, mock_parse_args, mock_maincall
    ):
        """
        Tests that `main` correctly parses arguments for viewing a sample
        and calls maincall with a Sample object.
        """
        sample_id = "SAMPLE_ID_1"
        mock_args = MagicMock()
        mock_args.is_sample = True
        mock_args.is_study = False
        mock_args.action = "view"
        mock_args.target = "metadata"
        mock_args.input = [sample_id]
        mock_parse_args.return_value = mock_args

        mock_sample_instance = MagicMock()
        MockSample.return_value = mock_sample_instance

        main()

        MockSample.assert_called_once_with(id=sample_id)
        mock_maincall.assert_called_once_with(mock_sample_instance, "view", "metadata")

    @patch("spirepy.cli.spire.maincall")
    @patch("spirepy.cli.spire.argparse.ArgumentParser.parse_args")
    @patch("spirepy.cli.spire.Study")
    def test_main_parses_study_download_args(
        self, MockStudy, mock_parse_args, mock_maincall
    ):
        """
        Tests that `main` correctly parses arguments for downloading from a study
        and calls maincall with a Study object.
        """
        study_name = "STUDY_ID_X"
        output_dir = "/tmp/output"
        mock_args = MagicMock()
        mock_args.is_sample = False
        mock_args.is_study = True
        mock_args.action = "download"
        mock_args.target = "mags"
        mock_args.input = [study_name]
        mock_args.output = output_dir
        mock_parse_args.return_value = mock_args

        mock_study_instance = MagicMock()
        MockStudy.return_value = mock_study_instance

        main()

        MockStudy.assert_called_once_with(name=study_name)
        mock_maincall.assert_called_once_with(
            mock_study_instance, "download", "mags", output_dir
        )

    @patch("spirepy.cli.spire.maincall")
    @patch("spirepy.cli.spire.argparse.ArgumentParser.parse_args")
    @patch("spirepy.cli.spire.Study")
    def test_main_defaults_to_study(self, MockStudy, mock_parse_args, mock_maincall):
        """
        Tests that `main` defaults to creating a Study object if no type flag is given.
        """
        study_name = "DEFAULT_STUDY"
        mock_args = MagicMock()
        mock_args.is_sample = False
        mock_args.is_study = False
        mock_args.action = "view"
        mock_args.target = "mags"
        mock_args.input = [study_name]
        mock_parse_args.return_value = mock_args

        mock_study_instance = MagicMock()
        MockStudy.return_value = mock_study_instance

        main()

        MockStudy.assert_called_once_with(name=study_name)
        mock_maincall.assert_called_once_with(mock_study_instance, "view", "mags")


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
