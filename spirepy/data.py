import polars as pl
from joblib import Memory
from platformdirs import user_cache_dir

cache_dir = user_cache_dir("spirepy", "spirepy-dev")
memory = Memory(cache_dir, verbose=0)


@memory.cache
def cluster_metadata():
    """Fetches and caches the SPIRE cluster metadata from the remote server.

    This is slow for the first time, as it downloads a large file, but
    subsequent calls will use the cached version.

    :return: A DataFrame with the SPIRE cluster metadata.
    """
    return pl.read_csv(
        "https://swifter.embl.de/~fullam/spire/metadata/spire_v1_cluster_metadata.tsv.gz",
        separator="\t",
    )


@memory.cache
def genome_metadata():
    """Fetches and caches the SPIRE genome metadata from the remote server.

    This is slow for the first time, as it downloads a large file, but
    subsequent calls will use the cached version.

    :return: A DataFrame with the SPIRE genome metadata.
    """
    return pl.read_csv(
        "https://swifter.embl.de/~fullam/spire/metadata/spire_v1_genome_metadata.tsv.gz",
        separator="\t",
    )
