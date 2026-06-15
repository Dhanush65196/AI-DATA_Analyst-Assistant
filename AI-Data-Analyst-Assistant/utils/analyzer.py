"""
Data analysis utility module
"""
import pandas as pd
import numpy as np
from typing import Dict, Any


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
        analysis = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "statistics": self._get_statistics(df),
            "correlations": self._get_correlations(df),
            "duplicate_rows": df.duplicated().sum()
        }
        return analysis
    
    def _get_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate descriptive statistics"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return {}
        
        stats = df[numeric_cols].describe().to_dict()
        return stats
    
    def _get_correlations(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Calculate correlations between numeric columns"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return {}
        
        corr_matrix = numeric_df.corr()
        return corr_matrix.to_dict()
    
    def get_column_info(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """Get detailed information about a specific column"""
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")
        
        col_data = df[column]
        info = {
            "dtype": str(col_data.dtype),
            "missing": col_data.isnull().sum(),
            "unique_values": col_data.nunique(),
            "top_values": col_data.value_counts().head().to_dict() if col_data.dtype == 'object' else None
        }
        
        if col_data.dtype in ['int64', 'float64']:
            info.update({
                "mean": col_data.mean(),
                "median": col_data.median(),
                "std": col_data.std(),
                "min": col_data.min(),
                "max": col_data.max()
            })
        
        return info
