import os
import os.path as path
import urllib.request

import polars as pl

from spirepy.data import cluster_metadata
from spirepy.logger import logger
from spirepy.study import Study


class Sample:
    """
    A sample from SPIRE.

    This class represents a sample from the SPIRE database. It is designed to
    provide all the properties and methods to allow work with samples and
    provide tools for automation and scalability.

    :param id: Internal ID for the sample.
    :type id: str

    :param study: The :class:`spirepy.study.Study` to which the sample belongs to, defaults to :class:`None`.
    :type study: :class:`spirepy.study.Study`, optional
    """

    def __init__(self, id: str, study: Study = None):
        """Constructor method."""
        self.id = id
        self.study = study
        self._metadata = None
        self._mags = None
        self._eggnog_data = None
        self._amr_annotations = {}

    def __str__(self):
        study_name = self.study.name if isinstance(self.study, Study) else None
        return f"Sample id: {self.id} 	Study: {study_name}"

    def __repr__(self):
        return self.__str__()

    def get_metadata(self) -> pl.dataframe.DataFrame:
        """Retrieve the metadata for a sample.

        :return: A Dataframe with the sample's metadata.
        :rtype: :class:`polars.dataframe.DataFrame`
        """
        if self._metadata is None:
            sample_meta = pl.read_csv(
                f"https://spire.embl.de/api/sample/{self.id}?format=tsv", separator="\t"
            )
            self._metadata = sample_meta
        return self._metadata

    def get_mags(self) -> pl.dataframe.DataFrame:
        """Retrieve the MAGs for a sample.

        :return: A Dataframe with the sample's MAGs.
        :rtype: :class:`polars.dataframe.DataFrame`
        """
        if self._mags is None:
            cluster_meta = cluster_metadata()
            metadata = self.get_metadata()
            clusters = metadata.filter(metadata["spire_cluster"] != "null")
            mags = cluster_meta.filter(
                cluster_meta["spire_cluster"].is_in(clusters["spire_cluster"])
            )
            mags = mags.join(clusters, on="spire_cluster")
            mags = mags.select(
                pl.col("spire_id"),
                pl.col("sample_id"),
                pl.all().exclude(["spire_id", "sample_id"]),
            )
            self._mags = mags
        return self._mags

    def get_eggnog_data(self) -> pl.dataframe.DataFrame:
        """Retrive the EggNOG-mapper data for a sample.

        :return: A Dataframe with the sample's EggNOG-mapper data.
        :rtype: :class:`polars.dataframe.DataFrame`
        """
        if self._eggnog_data is None:
            import pandas as pd
            egg = pd.read_csv(
                f"https://spire.embl.de/download_eggnog/{self.id}",
                sep="\t",
                skiprows=4,
                skipfooter=3,
                compression="gzip",
                engine="python",
            )
            eggnog_data = pl.from_pandas(egg)
            self._eggnog_data = eggnog_data
        return self._eggnog_data

    def get_amr_annotations(self, mode: str = "deeparg") -> pl.dataframe.DataFrame:
        """Obtain the anti-microbial resistance annotations for the sample.

        :param mode: Tool to select the AMR data from. Options are deepARG (deeparg), abricate-megares (megares) and abricate-vfdb (vfdb); defaults to deepARG.
        :type mode: str, optional

        :return: A Dataframe with the sample's AMR data.
        :rtype: :class:`polars.dataframe.DataFrame`
        """
        if mode not in self._amr_annotations:
            url = {
                "deeparg": f"https://spire.embl.de/download_deeparg/{self.id}",
                "megares": f"https://spire.embl.de/download_abricate_megares/{self.id}",
                "vfdb": f"https://spire.embl.de/download_abricate_vfdb/{self.id}",
            }.get(mode)
            if url is None:
                logger.error(
                    "Invalid option, please choose one of the following: deeparg, megares, vfdb"
                )
                return None
            amr = pl.read_csv(url, separator="\t")
            self._amr_annotations[mode] = amr
        return self._amr_annotations[mode]

    def download_mags(self, out_folder: str):
        """Download the MAGs into a specified folder.

        :param output: Output folder to download the MAGs to.
        :type output: str
        """
        os.makedirs(out_folder, exist_ok=True)
        for mag in self.get_mags()["spire_id"].to_list():
            urllib.request.urlretrieve(
                f"https://spire.embl.de/download_file/{mag}",
                path.join(out_folder, f"{mag}.fa.gz"),
            )
