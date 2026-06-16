"""
Unit tests for utils/analyzer.py
"""
import pytest
import pandas as pd
import numpy as np

from utils.analyzer import DataAnalyzer


@pytest.fixture
def analyzer():
    return DataAnalyzer()


@pytest.fixture
def numeric_df():
    """DataFrame with numeric columns."""
    return pd.DataFrame({
        "sales": [100.0, 200.0, 300.0, 400.0, 500.0],
        "quantity": [1, 2, 3, 4, 5],
        "category": ["A", "B", "A", "B", "A"]
    })


@pytest.fixture
def all_string_df():
    """DataFrame with only string columns."""
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "city": ["NYC", "LA", "SF"]
    })


@pytest.fixture
def single_numeric_df():
    """DataFrame with one numeric column (not enough for correlations)."""
    return pd.DataFrame({
        "value": [10, 20, 30],
        "label": ["x", "y", "z"]
    })


class TestAnalyze:
    def test_analyze_returns_expected_keys(self, analyzer, numeric_df):
        result = analyzer.analyze(numeric_df)
        assert "shape" in result
        assert "columns" in result
        assert "dtypes" in result
        assert "missing_values" in result
        assert "statistics" in result
        assert "correlations" in result
        assert "duplicate_rows" in result

    def test_analyze_shape(self, analyzer, numeric_df):
        result = analyzer.analyze(numeric_df)
        assert result["shape"] == (5, 3)

    def test_analyze_columns(self, analyzer, numeric_df):
        result = analyzer.analyze(numeric_df)
        assert result["columns"] == ["sales", "quantity", "category"]

    def test_analyze_missing_values(self, analyzer):
        df = pd.DataFrame({"a": [1, None, 3], "b": [None, None, "x"]})
        result = analyzer.analyze(df)
        assert result["missing_values"]["a"] == 1
        assert result["missing_values"]["b"] == 2

    def test_analyze_duplicate_rows(self, analyzer):
        df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
        result = analyzer.analyze(df)
        assert result["duplicate_rows"] == 1

    def test_analyze_correlations_with_multiple_numeric_cols(self, analyzer, numeric_df):
        result = analyzer.analyze(numeric_df)
        assert "sales" in result["correlations"]
        assert "quantity" in result["correlations"]

    def test_analyze_correlations_with_single_numeric_col(self, analyzer, single_numeric_df):
        result = analyzer.analyze(single_numeric_df)
        assert result["correlations"] == {}

    def test_analyze_statistics_no_numeric(self, analyzer, all_string_df):
        result = analyzer.analyze(all_string_df)
        assert result["statistics"] == {}


class TestGetStatistics:
    def test_returns_stats_for_numeric_cols(self, analyzer, numeric_df):
        stats = analyzer._get_statistics(numeric_df)
        assert "sales" in stats
        assert "quantity" in stats
        assert "mean" in stats["sales"]

    def test_returns_empty_for_non_numeric(self, analyzer, all_string_df):
        stats = analyzer._get_statistics(all_string_df)
        assert stats == {}


class TestGetCorrelations:
    def test_correlation_matrix(self, analyzer, numeric_df):
        corr = analyzer._get_correlations(numeric_df)
        assert "sales" in corr
        assert abs(corr["sales"]["quantity"] - 1.0) < 1e-10

    def test_single_column_returns_empty(self, analyzer, single_numeric_df):
        corr = analyzer._get_correlations(single_numeric_df)
        assert corr == {}


class TestGetColumnInfo:
    def test_numeric_column_info(self, analyzer, numeric_df):
        info = analyzer.get_column_info(numeric_df, "sales")
        assert info["dtype"] == "float64"
        assert info["missing"] == 0
        assert info["unique_values"] == 5
        assert "mean" in info
        assert "median" in info
        assert "std" in info
        assert "min" in info
        assert "max" in info
        assert info["mean"] == 300.0
        assert info["min"] == 100.0
        assert info["max"] == 500.0

    def test_string_column_info(self, analyzer, numeric_df):
        info = analyzer.get_column_info(numeric_df, "category")
        assert info["dtype"] in ("object", "str")
        assert info["unique_values"] == 2
        # top_values is populated only when dtype == 'object'; newer pandas
        # uses 'str' dtype so top_values may be None
        if info["dtype"] == "object":
            assert info["top_values"] is not None
        assert "mean" not in info

    def test_nonexistent_column_raises(self, analyzer, numeric_df):
        with pytest.raises(ValueError, match="Column 'nonexistent' not found"):
            analyzer.get_column_info(numeric_df, "nonexistent")

    def test_column_with_missing_values(self, analyzer):
        df = pd.DataFrame({"val": [1.0, None, 3.0, None, 5.0]})
        info = analyzer.get_column_info(df, "val")
        assert info["missing"] == 2
