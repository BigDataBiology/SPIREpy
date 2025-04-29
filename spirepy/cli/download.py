import os.path as path

import spirepy.logger as logger
from spirepy import Study


def download(item: str, target: str, output: str = "./"):
    """
    Dowload data from a SPIRE item.

    Arguments:

    item: str
        ID of the target item.
    target: str
        What you want to dowload (MAGs, metadata, genecalls, proteins)
    """
    if type(item) is Study:
        if target == "metadata":
            pass
        elif target == "manifest":
            pass
        else:
            logger.error("No matching item for Study type")
    else:
        if target == "metada":
            print(item.metadata)
        elif target == "manifes":
            print(item.manifest)
        else:
            print(item.amr_annotations)
