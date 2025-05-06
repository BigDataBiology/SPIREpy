import polars as pl


def cluster_metadata():
    return pl.read_csv(
        "https://swifter.embl.de/~fullam/spire/metadata/spire_v1_cluster_metadata.tsv.gz",
        separator="\t",
    )


def genome_metadata():
    return pl.read_csv(
        "https://swifter.embl.de/~fullam/spire/metadata/spire_v1_genome_metadata.tsv.gz",
        separator="\t",
    )
