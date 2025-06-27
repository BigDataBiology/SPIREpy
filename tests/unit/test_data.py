import unittest
from unittest.mock import patch, MagicMock
import polars as pl
from spirepy.data import cluster_metadata, genome_metadata

class TestDataFunctions(unittest.TestCase):
    @patch('polars.read_csv')
    def test_cluster_metadata_returns_polars_dataframe(self, mock_read_csv):
        mock_read_csv.return_value = pl.DataFrame({
            'cluster_id': [1, 2],
            'description': ['Cluster 1', 'Cluster 2']
        })
        
        result = cluster_metadata()
        
        self.assertIsInstance(result, pl.DataFrame)

    @patch('polars.read_csv')
    def test_genome_metadata_returns_polars_dataframe(self, mock_read_csv):
        mock_read_csv.return_value = pl.DataFrame({
            'genome_id': [1, 2],
            'species': ['Species A', 'Species B']
        })
        
        result = genome_metadata()
        
        self.assertIsInstance(result, pl.DataFrame)

    @patch('polars.read_csv')
    def test_cluster_metadata_caching(self, mock_read_csv):
        cluster_metadata.clear()
        mock_read_csv.return_value = pl.DataFrame({'a': [1]})
        
        cluster_metadata()
        cluster_metadata()
        
        mock_read_csv.assert_called_once()

    @patch('polars.read_csv')
    def test_genome_metadata_caching(self, mock_read_csv):
        genome_metadata.clear()
        mock_read_csv.return_value = pl.DataFrame({'a': [1]})
        
        genome_metadata()
        genome_metadata()
        
        mock_read_csv.assert_called_once()

if __name__ == '__main__':
    unittest.main()
