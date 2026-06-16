"""
Shared data profiling utilities.

Centralizes data summary, missing-value analysis, and numeric-column
detection that were previously duplicated across app.py and analyzer.py.
"""

import pandas as pd
import numpy as np
from typing import Any, Dict, List


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """Return the names of all numeric columns in *df*."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_missing_values(df: pd.DataFrame) -> Dict[str, int]:
    """Return a ``{column: missing_count}`` mapping."""
    return df.isnull().sum().to_dict()


def get_missing_values_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with per-column missing counts and percentages."""
    counts = df.isnull().sum()
    pcts = (counts / len(df) * 100).round(2) if len(df) > 0 else counts * 0
    return pd.DataFrame({
        "Column": df.columns,
        "Missing Count": counts.values,
        "Missing %": pcts.values,
    })


def get_data_profile(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Comprehensive data profile combining the fields previously produced by
    ``app.get_data_summary`` and ``analyzer.DataAnalyzer.analyze``.

    Returns a dict with: rows, columns, column_names, dtypes,
    missing_values, memory_usage_mb, duplicate_rows.
    """
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": get_missing_values(df),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 ** 2),
        "duplicate_rows": int(df.duplicated().sum()),
    }
