"""
Shared column-detection utilities.

Provides a generic keyword-based column detector and thin convenience
wrappers for sales and category columns, replacing the duplicated
detection loops that lived in app.py.
"""

import pandas as pd
import numpy as np
from typing import Callable, List, Optional

SALES_KEYWORDS: List[str] = [
    "sales", "revenue", "amount", "total", "price",
    "quantity", "units", "qty", "cost", "profit",
    "income", "earnings", "value",
]

CATEGORY_KEYWORDS: List[str] = [
    "category", "type", "status", "region", "state",
    "country", "city", "product", "department", "name",
    "brand", "segment",
]


def detect_columns_by_keywords(
    df: pd.DataFrame,
    keywords: List[str],
    dtype_filter: Optional[Callable[[pd.Series], bool]] = None,
) -> List[str]:
    """
    Return column names whose lowercased name contains any of *keywords*
    and (optionally) whose series passes *dtype_filter*.

    Args:
        df: Input DataFrame.
        keywords: Substrings to look for in column names (case-insensitive).
        dtype_filter: Optional predicate applied to the column Series.
                      Column is included only when the predicate returns True.

    Returns:
        List of matching column names.
    """
    matched: List[str] = []
    for col in df.columns:
        if not any(kw in col.lower() for kw in keywords):
            continue
        if dtype_filter is not None and not dtype_filter(df[col]):
            continue
        matched.append(col)
    return matched


def detect_sales_columns(df: pd.DataFrame) -> List[str]:
    """Detect numeric columns whose names suggest sales/revenue data."""
    return detect_columns_by_keywords(
        df,
        SALES_KEYWORDS,
        dtype_filter=lambda s: pd.api.types.is_numeric_dtype(s),
    )


def detect_category_columns(df: pd.DataFrame) -> List[str]:
    """Detect categorical columns suitable for grouping."""
    return detect_columns_by_keywords(
        df,
        CATEGORY_KEYWORDS,
        dtype_filter=lambda s: s.dtype == "object" or s.nunique() < 50,
    )
