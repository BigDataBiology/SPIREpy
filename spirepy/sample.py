import os

import urllib.request

import polars as pl
import os.path as path

from spirepy.study import Study
from spirepy.metadata import cluster_metadata
from spirepy.logger import logger
from spirepy.util import clean_emapper_data


class Sample:
    """
    A sample from SPIRE.

    This class represents a sample from the SPIRE database. It is designed to
    provide all the properties and methods to allow work with samples and
    provide tools for automation and scalability.

    Attributes:

    id: str
        Internal ID for the sample.
    study: Study
        Study ID to which the sample belongs to.
    """

    def __init__(self, id: str, study: Study):
        """
        Creates a new sample object.
        """
        self.id = id
        self.study = study
        self.out_folder = path.join(study.folder, self.id)
        self._eggnog_data = None
        self._mags = None
        self._metadata = None
        self._manifest = None

        os.makedirs(self.out_folder, exist_ok=True)

    def __str__(self):
        return f"Sample id: {self.id} \tStudy: {self.study.name}"

    def __repr__(self):
        return self.__str__()

    @property
    def eggnog_data(self):
        if self._eggnog_data is None:
            urllib.request.urlretrieve(
                f"https://spire.embl.de/download_eggnog/{self.id}",
                path.join(self.out_folder, "emapper_annotations.gz"),
            )
            eggnog_data = clean_emapper_data(
                path.join(self.out_folder, "emapper_annotations.gz")
            )
            eggnog_data.to_csv(
                path.join(self.out_folder, "emapper_annotations.tsv", sep="\t")
            )
            self._eggnog_data = eggnog_data
        return self._eggnog_data

    @property
    def mags(self, download: bool = False):
        if self._mags is None:
            cluster_meta = cluster_metadata()
            clusters = self.metadata.filter(self.metadata["spire_cluster"] != "null")
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
        if download:
            self.download_mags()
        return self._mags

    @property
    def metadata(self):
        if self._metadata is None:
            logger.warning("No sample metadata, downloading from SPIRE...\n")
            sample_meta = pl.read_csv(
                f"https://spire.embl.de/api/sample/{self.id}?format=tsv", separator="\t"
            )
            self._metadata = sample_meta
        return self._metadata

    def download_mags(self):
        mag_folder = path.join(self.out_folder, "mags/")
        os.makedirs(mag_folder, exist_ok=True)
        for mag in self.mags:
            urllib.request.urlretrieve(
                f"https://spire.embl.de/download_file/{mag}",
                path.join(mag_folder, "{mag}.fa.gz"),
            )
