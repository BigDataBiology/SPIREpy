import polars as pl
from spirepy import Study, Sample
from spirepy.logger import logger


def view(item: str, target: str):
    """
    View a SPIRE item.

    :param item: The item to be viewed (:class:`spirepy.sample.Sample` or :class:`spirepy.study.Study`).
    :type item: class:`spirepy.sample.Sample` or class:`spirepy.study.Study`

    :param target: What you want to view (metadata, antibiotic resistance annotations, manifest)
    :type target: str
    """

    if isinstance(item, Study):
        study_match = {
            "metadata": item.get_metadata,
            "mags": item.get_mags,
        }.get(target)

        if study_match:
            print(study_match())
        else:
            logger.error("No matching item for Study type")
    else:  # Assumes item is a Sample
        sample_match = {
            "metadata": item.get_metadata,
            "mags": item.get_mags,
            "eggnog": item.get_eggnog_data,
            "amr": item.get_amr_annotations,
        }.get(target)

        if sample_match:
            print(sample_match())
        else:
            logger.error("No matching item")
