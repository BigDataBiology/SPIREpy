import os
import os.path as path
from typing import Union

from spirepy import Sample, Study
from spirepy.logger import logger


def download(item: Union[Study, Sample], target: str, output: str):
    """
    Dowload data from a SPIRE item.

    :param item: The item to be viewed (:class:`spirepy.sample.Sample` or :class:`spirepy.study.Study`).
    :type item: :class:`spirepy.sample.Sample` or :class:`spirepy.study.Study`

    :param target: What you want to view (metadata, antibiotic resistance annotations, manifest)
    :type target: str

    :param output: The output folder where the items will be downloaded.
    :type output: str
    """
    os.makedirs(output, exist_ok=True)
    if type(item) is Study:
        if target == "metadata":
            item.get_metadata().write_csv(path.join(output, f"{item.name}.csv"))
        elif target == "mags":
            item.download_mags(output)
        else:
            logger.error("No matching item for Study type")
    else:
        if target == "metadata":
            item.get_metadata().write_csv(path.join(output, f"{item.id}.csv"))
        elif target == "mags":
            item.download_mags(output)
        else:
            logger.error("No matching item")
