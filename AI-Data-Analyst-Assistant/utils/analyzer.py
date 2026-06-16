"""
Data analysis utility module
"""
import logging
import pandas as pd
import numpy as np
from typing import Dict, Any

from .exceptions import AnalysisError

logger = logging.getLogger(__name__)


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

        Raises:
            AnalysisError: If analysis cannot be completed
        """
        if df.empty:
            raise AnalysisError("analyze", "DataFrame is empty")

        try:
            analysis = {
                "shape": df.shape,
                "columns": list(df.columns),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "statistics": self._get_statistics(df),
                "correlations": self._get_correlations(df),
                "duplicate_rows": int(df.duplicated().sum())
            }
        except AnalysisError:
            raise
        except Exception as e:
            logger.error("Unexpected error during analysis: %s", e)
            raise AnalysisError("analyze", str(e)) from e

        return analysis

    def _get_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate descriptive statistics.

        Raises:
            AnalysisError: If statistics computation fails
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return {}

        try:
            stats = df[numeric_cols].describe().to_dict()
        except Exception as e:
            logger.warning("Failed to compute statistics: %s", e)
            raise AnalysisError("statistics", str(e)) from e

        return stats

    def _get_correlations(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        Calculate correlations between numeric columns.

        Raises:
            AnalysisError: If correlation computation fails
        """
        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.shape[1] < 2:
            return {}

        try:
            corr_matrix = numeric_df.corr()
            return corr_matrix.to_dict()
        except ValueError as e:
            logger.warning("Correlation calculation failed: %s", e)
            raise AnalysisError("correlations", str(e)) from e
        except Exception as e:
            logger.warning("Unexpected error in correlation: %s", e)
            raise AnalysisError("correlations", str(e)) from e

    def get_column_info(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific column.

        Raises:
            ValueError: If column does not exist in the DataFrame
            AnalysisError: If column analysis fails
        """
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")

        try:
            col_data = df[column]
            info: Dict[str, Any] = {
                "dtype": str(col_data.dtype),
                "missing": int(col_data.isnull().sum()),
                "unique_values": int(col_data.nunique()),
                "top_values": (
                    col_data.value_counts().head().to_dict()
                    if col_data.dtype == 'object'
                    else None
                )
            }

            if col_data.dtype in ['int64', 'float64']:
                info.update({
                    "mean": float(col_data.mean()),
                    "median": float(col_data.median()),
                    "std": float(col_data.std()),
                    "min": float(col_data.min()),
                    "max": float(col_data.max())
                })
        except ValueError:
            raise
        except Exception as e:
            logger.error("Error analyzing column '%s': %s", column, e)
            raise AnalysisError(f"column_info({column})", str(e)) from e

        return info
