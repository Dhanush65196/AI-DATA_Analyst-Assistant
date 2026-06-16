"""
Data analysis utility module
"""
import pandas as pd
import numpy as np
from typing import Dict, Any

from .data_profiler import get_missing_values, get_numeric_columns


class DataAnalyzer:
    """Analyze data and generate insights"""

    def __init__(self):
        """Initialize DataAnalyzer"""
        pass

    def analyze(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform comprehensive data analysis

        Args:
            df: DataFrame to analyze

        Returns:
            dict: Analysis results
        """
        numeric_cols = get_numeric_columns(df)

        analysis = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": get_missing_values(df),
            "statistics": self._get_statistics(df, numeric_cols),
            "correlations": self._get_correlations(df, numeric_cols),
            "duplicate_rows": df.duplicated().sum(),
        }
        return analysis

    def _get_statistics(
        self, df: pd.DataFrame, numeric_cols: list[str] | None = None
    ) -> Dict[str, Any]:
        """Calculate descriptive statistics"""
        if numeric_cols is None:
            numeric_cols = get_numeric_columns(df)

        if not numeric_cols:
            return {}

        return df[numeric_cols].describe().to_dict()

    def _get_correlations(
        self, df: pd.DataFrame, numeric_cols: list[str] | None = None
    ) -> Dict[str, Dict[str, float]]:
        """Calculate correlations between numeric columns"""
        if numeric_cols is None:
            numeric_cols = get_numeric_columns(df)

        if len(numeric_cols) < 2:
            return {}

        return df[numeric_cols].corr().to_dict()

    def get_column_info(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """Get detailed information about a specific column"""
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")

        col_data = df[column]
        info: Dict[str, Any] = {
            "dtype": str(col_data.dtype),
            "missing": int(col_data.isnull().sum()),
            "unique_values": col_data.nunique(),
            "top_values": (
                col_data.value_counts().head().to_dict()
                if col_data.dtype == "object"
                else None
            ),
        }

        if col_data.dtype in ["int64", "float64"]:
            info.update({
                "mean": col_data.mean(),
                "median": col_data.median(),
                "std": col_data.std(),
                "min": col_data.min(),
                "max": col_data.max(),
            })

        return info
