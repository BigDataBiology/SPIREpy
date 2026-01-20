import os
import os.path as path
import tarfile
import tempfile
import urllib

import polars as pl

from spirepy.data import genome_metadata


class Study:
    """
    A study from SPIRE.

    This class represents a study from the SPIRE database. It automatically
    fetches metadata and automates the initialization of samples to further use
    to obtain its genomic, geographical or other types of data provided by it.

    :param name: Internal ID for the study.
    :type name: str
    """

    def __init__(self, name: str):
        """Constructor method."""
        self.name = name
        self._metadata = None
        self._samples = None
        self._mags = None

    def get_metadata(self) -> pl.dataframe.DataFrame:
        """Retrieve metadata for the study.

        :return: A Dataframe with the study's metadata.
        :rtype: :class:`polars.dataframe.DataFrame`
        """
        if self._metadata is None:
            study_meta = pl.read_csv(
                f"https://spire.embl.de/api/study/{self.name}?format=tsv",
                separator="\t",
            )
            self._metadata = study_meta
        return self._metadata

    def get_samples(self) -> list:
        """Retrive a list of samples for the study.

        :return: List of :class:`spirepy.sample.Sample` that belong to the study.
        :rtype: list
        """
        from spirepy.sample import Sample

        if self._samples is None:
            sample_list = []
            for s in self.get_metadata()["sample_id"].to_list():
                sample = Sample(s, self)
                sample_list.append(sample)
            self._samples = sample_list
        return self._samples

    def get_mags(self) -> pl.dataframe.DataFrame:
        """Get a DataFrame with information regarding the MAGs.

        :return: A Dataframe with the study's MAGs.
        :rtype: :class:`polars.dataframe.DataFrame`
        """
        if self._mags is None:
            genomes = genome_metadata()
            self._mags = genomes.filter(
                pl.col("derived_from_sample").is_in(
                    self.get_metadata()["sample_id"].to_list()
                )
            )
        return self._mags

    def download_assemblies(self, output: str):
        """Download the assemblies into a specified folder.

        :param output: Output folder to download the MAGs to.
        :type output: str
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tarfpath = path.join(tmpdir, f"{self.name}_assemblies.tar")
            urllib.request.urlretrieve(
                f"https://swifter.embl.de/~fullam/spire/compiled/{self.name}_spire_v1_assemblies.tar",
                tarfpath,
            )
            os.makedirs(output, exist_ok=True)
            with tarfile.open(tarfpath) as tar:
                tar.extractall(path.join(output, "assemblies"))

    def download_mags(self, output: str):
        """Download the MAGs into a specified folder.

        :param output: Output folder to download the MAGs to.
        :type output: str
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tarfpath = path.join(tmpdir, f"{self.name}_mags.tar")
            urllib.request.urlretrieve(
                f"https://swifter.embl.de/~fullam/spire/compiled/{self.name}_spire_v1_MAGs.tar",
                tarfpath,
            )
            os.makedirs(output, exist_ok=True)
            with tarfile.open(tarfpath) as tar:
                tar.extractall(path.join(output, "mags"))

    def download_genecalls(self, output: str):
        """Download the genecalls into a specified folder.

        :param output: Output folder to download the MAGs to.
        :type output: str
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tarfpath = path.join(tmpdir, f"{self.name}_genecalls.tar")
            urllib.request.urlretrieve(
                f"https://swifter.embl.de/~fullam/spire/genes_per_study/{self.name}_spire_v1_genecalls_fna.tar",
                tarfpath,
            )
            os.makedirs(output, exist_ok=True)
            with tarfile.open(tarfpath) as tar:
                tar.extractall(path.join(output, "genecalls"))

    def download_proteins(self, output: str):
        """Download the proteins into a specified folder.

        :param output: Output folder to download the MAGs to.
        :type output: str
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tarfpath = path.join(tmpdir, f"{self.name}_genecalls.tar")
            urllib.request.urlretrieve(
                f"https://swifter.embl.de/~fullam/spire/genes_per_study/{self.name}_spire_v1_proteins_faa.tar",
                tarfpath,
            )
            os.makedirs(output, exist_ok=True)
            with tarfile.open(tarfpath) as tar:
                tar.extractall(path.join(output, "proteins"))
