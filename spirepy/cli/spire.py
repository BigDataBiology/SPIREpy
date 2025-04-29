import re
import argparse

from spirepy import Study, Sample
from spirepy.cli import download, view


def maincall(input, action: str, type: str, output=None):
    if action == "view":
        view(item=input, target=type)
    else:
        pass
        # download()


def main():
    parser = argparse.ArgumentParser(
        description="Interact with the SPIRE database",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparsers = parser.add_subparsers(help="subcommand help", dest="command")

    # create the parser for the "view" command
    parser_view = subparsers.add_parser("view", help="view the data from an object")
    parser_view.add_argument(
        dest="type",
        choices=["metadata", "amr", "manifest", "eggnog", "mags"],
        action="store",
        help="types of items to view",
    )
    parser_view.add_argument(
        "input", metavar="INPUT", nargs="+", help="Input (study or sample ID)", type=str
    )
    # create the parser for the "download" command
    parser_download = subparsers.add_parser(
        "download", help="download data from an item"
    )
    parser_download.add_argument(
        dest="type",
        choices=["mags", "proteins", "genecalls", "metadata"],
        action="store",
        help="types of items to dowload",
    )
    parser_download.add_argument(
        "input", metavar="INPUT", nargs="+", help="Input (study or sample ID)"
    )
    parser_download.add_argument(
        "-o",
        "--output",
        dest="output",
        help="output folder; defaults to current folder",
        default="./",
    )

    args = parser.parse_args()
    print(args)

    # FIX: Won't work with all samples in SPIRE, needs to be fixed
    if re.match(r"^SAMN\d{8}$", args.input[0]):
        input = Sample(id=args.input[0])
        maincall(input, action=args.command, type=args.type)
    else:
        input = Study(name=args.input[0], out_folder=args.output)
        maincall(input, action=args.command, type=args.type, output=args.output)


if __name__ == "__main__":
    main()
