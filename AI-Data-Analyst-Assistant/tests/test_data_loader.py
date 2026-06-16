"""
Unit tests for utils/data_loader.py
"""
import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path

from utils.data_loader import DataLoader


@pytest.fixture
def loader():
    return DataLoader()


@pytest.fixture
def sample_csv(tmp_path):
    """Create a temporary CSV file for testing."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    path = tmp_path / "sample.csv"
    df.to_csv(path, index=False)
    return path


@pytest.fixture
def sample_json(tmp_path):
    """Create a temporary JSON file for testing."""
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    path = tmp_path / "sample.json"
    df.to_json(path)
    return path


@pytest.fixture
def sample_parquet(tmp_path):
    """Create a temporary Parquet file for testing."""
    pytest.importorskip("pyarrow")
    df = pd.DataFrame({"a": [10, 20], "b": [30, 40]})
    path = tmp_path / "sample.parquet"
    df.to_parquet(path)
    return path


class TestDataLoaderInit:
    def test_supported_formats(self, loader):
        assert ".csv" in loader.SUPPORTED_FORMATS
        assert ".xlsx" in loader.SUPPORTED_FORMATS
        assert ".json" in loader.SUPPORTED_FORMATS
        assert ".parquet" in loader.SUPPORTED_FORMATS
        assert ".xls" in loader.SUPPORTED_FORMATS


class TestLoadData:
    def test_load_csv(self, loader, sample_csv):
        df = loader.load_data(sample_csv)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["a", "b"]
        assert len(df) == 3

    def test_load_json(self, loader, sample_json):
        df = loader.load_data(sample_json)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2

    @pytest.mark.skipif(
        not pd.io.parquet.get_engine("auto") if False else True,
        reason="pyarrow/fastparquet not installed"
    )
    def test_load_parquet(self, loader, sample_parquet):
        pytest.importorskip("pyarrow")
        df = loader.load_data(sample_parquet)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["a", "b"]
        assert len(df) == 2

    def test_load_nonexistent_file(self, loader):
        with pytest.raises(FileNotFoundError):
            loader.load_data("/nonexistent/path/file.csv")

    def test_load_unsupported_format(self, loader, tmp_path):
        path = tmp_path / "data.txt"
        path.write_text("hello")
        with pytest.raises(ValueError, match="Unsupported file format"):
            loader.load_data(path)

    def test_load_data_accepts_string_path(self, loader, sample_csv):
        df = loader.load_data(str(sample_csv))
        assert isinstance(df, pd.DataFrame)


class TestSaveData:
    def test_save_csv(self, loader, tmp_path):
        df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
        path = tmp_path / "output.csv"
        loader.save_data(df, path, format="csv")
        assert path.exists()
        loaded = pd.read_csv(path)
        assert list(loaded.columns) == ["x", "y"]
        assert len(loaded) == 2

    def test_save_json(self, loader, tmp_path):
        df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
        path = tmp_path / "output.json"
        loader.save_data(df, path, format="json")
        assert path.exists()

    def test_save_parquet(self, loader, tmp_path):
        pytest.importorskip("pyarrow")
        df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
        path = tmp_path / "output.parquet"
        loader.save_data(df, path, format="parquet")
        assert path.exists()

    def test_save_creates_parent_dirs(self, loader, tmp_path):
        df = pd.DataFrame({"a": [1]})
        path = tmp_path / "nested" / "dir" / "output.csv"
        loader.save_data(df, path, format="csv")
        assert path.exists()

    def test_save_unsupported_format(self, loader, tmp_path):
        df = pd.DataFrame({"a": [1]})
        path = tmp_path / "output.txt"
        with pytest.raises(ValueError, match="Unsupported format"):
            loader.save_data(df, path, format="txt")
