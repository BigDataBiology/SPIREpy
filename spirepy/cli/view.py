import polars as pl
from spirepy import Study, Sample
from spirepy.logger import logger


def view(item: str, target: str):
    """
    View a SPIRE item.

    Arguments:

    item: str
        ID of the item to be viewed.
    target: str
        What you want to view (metadata, antibiotic resistance annotations, manifest)
    """

    if type(item) is Study:
        if target == "metadata":
            print(item.metadata)
        if target == "mags":
            print(item.mags)
        elif target == "manifest":
            print(item.manifest)
        else:
            logger.error("No matching item for Study type")
    else:
        if target == "metadata":
            print(item.metadata)
        if target == "mags":
            print(item.mags)
        elif target == "manifest":
            print(item.manifest)
        elif target == "eggnog":
            print(item.eggnog_data)
        elif target == "amr":
            print(item.amr_annotations)
