import polars as pl


def cluster_metadata():
    cluster = pl.read_csv(
        "https://swifter.embl.de/~fullam/spire/metadata/spire_v1_cluster_metadata.tsv.gz",
        separator="\t",
    )
    return cluster
