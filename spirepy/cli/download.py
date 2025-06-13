import urllib
import os
import tarfile
from tqdm import tqdm
import os.path as path

import spirepy.logger as logger
from spirepy import Study


def download(item: str, target: str, output: str):
    """
    Dowload data from a SPIRE item.

    Arguments:

    item: str
        ID of the target item.
    target: str
        What you want to dowload (MAGs, metadata, genecalls, proteins).
    output: str
        The output folder where the items will be downloaded.
    """
    os.makedirs(output, exist_ok=True)
    if type(item) is Study:
        if target == "metadata":
            item.metadata.write_csv(output)
        elif target == "manifest":
            pass
        elif target == "mags":
            item.download_mags(output)
        else:
            logger.error("No matching item for Study type")
    else:
        if target == "metadata":
            print(item.metadata)
        elif target == "manifest":
            print(item.manifest)
        elif target == "mags":
            item.download_mags(out_folder=path.join(output, item.id))
        else:
            print(item.amr_annotations)
