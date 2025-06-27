import unittest
from unittest.mock import patch
import polars as pl
from spirepy.data import cluster_metadata, genome_metadata, cache_dir
import shutil
import os

class TestDataCacheOnDisk(unittest.TestCase):
    def setUp(self):
        """Ensure the cache directory is clean before each test."""
        cluster_metadata.clear()
        genome_metadata.clear()
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)

    def tearDown(self):
        """Clean up the cache directory after each test."""
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)

    @patch('polars.read_csv')
    def test_disk_cache_creation(self, mock_read_csv):
        """Test that calling a cached function creates the on-disk cache."""
        mock_read_csv.return_value = pl.DataFrame({'a': [1]})
        
        self.assertFalse(os.path.exists(cache_dir))
        
        cluster_metadata()
        
        self.assertTrue(os.path.exists(cache_dir))
        self.assertTrue(len(os.listdir(cache_dir)) > 0)

if __name__ == '__main__':
    unittest.main()
