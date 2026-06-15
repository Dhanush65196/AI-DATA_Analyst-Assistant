"""
Data loading utility module
"""
import pandas as pd
from pathlib import Path
from typing import Union


class DataLoader:
    """Load and manage data from various file formats"""
    
    SUPPORTED_FORMATS = {'.csv', '.xlsx', '.xls', '.json', '.parquet'}
    
    def __init__(self):
        """Initialize DataLoader"""
        pass
    
    def load_data(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from file
        
        Args:
            file_path: Path to data file
            
        Returns:
            pd.DataFrame: Loaded data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = file_path.suffix.lower()
        
        if suffix == '.csv':
            return pd.read_csv(file_path)
        elif suffix in {'.xlsx', '.xls'}:
            return pd.read_excel(file_path)
        elif suffix == '.json':
            return pd.read_json(file_path)
        elif suffix == '.parquet':
            return pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    def save_data(self, df: pd.DataFrame, file_path: Union[str, Path], format: str = 'csv') -> None:
        """
        Save data to file
        
        Args:
            df: DataFrame to save
            file_path: Output file path
            format: Output format (csv, xlsx, json, parquet)
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'csv':
            df.to_csv(file_path, index=False)
        elif format == 'xlsx':
            df.to_excel(file_path, index=False)
        elif format == 'json':
            df.to_json(file_path)
        elif format == 'parquet':
            df.to_parquet(file_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
