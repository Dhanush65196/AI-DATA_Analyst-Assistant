"""
Unit tests for app.py (pure functions only, no Streamlit UI)
"""
import pytest
import pandas as pd
import numpy as np
import io
from unittest.mock import MagicMock

import sys
# Mock streamlit so we can import app.py without a running Streamlit server
sys.modules.setdefault("streamlit", MagicMock())
sys.modules.setdefault("plotly", MagicMock())
sys.modules.setdefault("plotly.graph_objects", MagicMock())
sys.modules.setdefault("plotly.express", MagicMock())
sys.modules.setdefault("matplotlib", MagicMock())
sys.modules.setdefault("matplotlib.pyplot", MagicMock())

from app import (
    validate_csv_file,
    get_data_summary,
    detect_sales_columns,
    detect_category_columns,
)


class TestValidateCsvFile:
    def test_none_file(self):
        is_valid, msg = validate_csv_file(None)
        assert is_valid is False
        assert "No file uploaded" in msg

    def test_non_csv_extension(self):
        fake_file = MagicMock()
        fake_file.name = "data.xlsx"
        fake_file.size = 1024
        is_valid, msg = validate_csv_file(fake_file)
        assert is_valid is False
        assert "CSV" in msg

    def test_file_too_large(self):
        fake_file = MagicMock()
        fake_file.name = "data.csv"
        fake_file.size = 60 * 1024 * 1024  # 60 MB
        is_valid, msg = validate_csv_file(fake_file)
        assert is_valid is False
        assert "50MB" in msg

    def test_valid_csv_file(self):
        fake_file = MagicMock()
        fake_file.name = "data.csv"
        fake_file.size = 1024  # 1 KB
        is_valid, msg = validate_csv_file(fake_file)
        assert is_valid is True
        assert "passed" in msg

    def test_boundary_50mb_file(self):
        fake_file = MagicMock()
        fake_file.name = "data.csv"
        fake_file.size = 50 * 1024 * 1024  # exactly 50 MB
        is_valid, msg = validate_csv_file(fake_file)
        assert is_valid is True


class TestGetDataSummary:
    def test_basic_summary(self):
        df = pd.DataFrame({
            "a": [1, 2, 3],
            "b": ["x", "y", "z"],
            "c": [1.0, None, 3.0]
        })
        summary = get_data_summary(df)
        assert summary["rows"] == 3
        assert summary["columns"] == 3
        assert summary["column_names"] == ["a", "b", "c"]
        assert summary["missing_values"]["c"] == 1
        assert summary["missing_values"]["a"] == 0
        assert summary["memory_usage_mb"] > 0

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        summary = get_data_summary(df)
        assert summary["rows"] == 0
        assert summary["columns"] == 0
        assert summary["column_names"] == []

    def test_dtypes_present(self):
        df = pd.DataFrame({"x": [1, 2], "y": [1.5, 2.5]})
        summary = get_data_summary(df)
        assert "x" in summary["dtypes"]
        assert "y" in summary["dtypes"]


class TestDetectSalesColumns:
    def test_detects_sales_column(self):
        df = pd.DataFrame({
            "Total_Sales": [100, 200, 300],
            "category": ["A", "B", "C"]
        })
        result = detect_sales_columns(df)
        assert "Total_Sales" in result

    def test_detects_revenue_column(self):
        df = pd.DataFrame({
            "revenue": [1000.0, 2000.0],
            "name": ["x", "y"]
        })
        result = detect_sales_columns(df)
        assert "revenue" in result

    def test_ignores_non_numeric_sales_column(self):
        df = pd.DataFrame({
            "sales_category": ["high", "low", "medium"]
        })
        result = detect_sales_columns(df)
        assert result == []

    def test_detects_multiple_sales_columns(self):
        df = pd.DataFrame({
            "price": [10, 20],
            "quantity": [5, 10],
            "name": ["a", "b"]
        })
        result = detect_sales_columns(df)
        assert "price" in result
        assert "quantity" in result

    def test_no_sales_columns(self):
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["a", "b", "c"]
        })
        result = detect_sales_columns(df)
        assert result == []


class TestDetectCategoryColumns:
    def test_detects_category_column(self):
        df = pd.DataFrame({
            "category": ["A", "B", "C"],
            "value": [1, 2, 3]
        })
        result = detect_category_columns(df)
        assert "category" in result

    def test_detects_region_column(self):
        df = pd.DataFrame({
            "region": ["North", "South", "East"],
            "sales": [100, 200, 300]
        })
        result = detect_category_columns(df)
        assert "region" in result

    def test_detects_product_column(self):
        df = pd.DataFrame({
            "product_name": ["Widget", "Gadget"],
            "price": [10, 20]
        })
        result = detect_category_columns(df)
        assert "product_name" in result

    def test_no_category_columns(self):
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "y": [4, 5, 6]
        })
        result = detect_category_columns(df)
        assert result == []

    def test_numeric_with_few_unique_and_keyword(self):
        df = pd.DataFrame({
            "status": [0, 1, 0, 1, 0]
        })
        result = detect_category_columns(df)
        assert "status" in result
