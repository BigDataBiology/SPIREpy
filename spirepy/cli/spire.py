import argparse
# from spirepy import Study, Sample


def main():
    parser = argparse.ArgumentParser(
        description="Interact with the SPIRE database",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparsers = parser.add_subparsers(help="subcommand help")

    # create the parser for the "view" command
    parser_view = subparsers.add_parser("view", help="view the data from an object")
    parser_view.add_argument(
        "--type",
        choices=("metadata", "amr", "manifest"),
        default="metadata",
        help="types of items to view",
    )
    parser_view.add_argument(
        "input", metavar="INPUT", nargs="+", help="Input (study or sample ID)"
    )
    # create the parser for the "download" command
    parser_download = subparsers.add_parser(
        "download", help="download data from an item"
    )
    parser_download.add_argument(
        "--type",
        choices=("mags", "proteins", "genecalls", "metadata"),
        default="metadata",
        help="types of items to dowload",
    )
    parser_download.add_argument(
        "input", metavar="INPUT", nargs="+", help="Input (study or sample ID)"
    )
    parser_download.add_argument("-o", "--output", dest="output", help="output folder")

    args = parser.parse_args()


if __name__ == "__main__":
    main()
