"""
Data loading utility module
"""
import logging
import pandas as pd
from pathlib import Path
from typing import Optional, Union

logger = logging.getLogger(__name__)

# Restrict file operations to these directories (relative to project root)
_ALLOWED_DIRECTORIES = {"data", "charts", "output"}
_MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _validate_path(file_path: Path, allowed_dirs: Optional[set] = None) -> Path:
    """
    Resolve and validate that file_path stays within allowed directories.

    Raises:
        ValueError: on path-traversal attempts or disallowed locations.
    """
    project_root = _get_project_root()
    resolved = file_path.resolve()

    if allowed_dirs is None:
        allowed_dirs = _ALLOWED_DIRECTORIES

    allowed_roots = [project_root / d for d in allowed_dirs]
    if not any(resolved == root or root in resolved.parents for root in allowed_roots):
        raise ValueError(
            f"Access denied: path must be inside one of {allowed_dirs}"
        )
    return resolved


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
            ValueError: If file format is not supported or path is disallowed
        """
        file_path = Path(file_path)
        resolved = _validate_path(file_path)

        if not resolved.exists():
            raise FileNotFoundError("Requested file does not exist")

        if resolved.stat().st_size > _MAX_FILE_SIZE_BYTES:
            raise ValueError("File exceeds the maximum allowed size of 50 MB")

        suffix = resolved.suffix.lower()
        if suffix not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {suffix}")

        if suffix == '.csv':
            return pd.read_csv(resolved)
        elif suffix in {'.xlsx', '.xls'}:
            return pd.read_excel(resolved)
        elif suffix == '.json':
            return pd.read_json(resolved)
        elif suffix == '.parquet':
            return pd.read_parquet(resolved)

        raise ValueError(f"Unsupported file format: {suffix}")

    def save_data(self, df: pd.DataFrame, file_path: Union[str, Path], format: str = 'csv') -> None:
        """
        Save data to file
        
        Args:
            df: DataFrame to save
            file_path: Output file path
            format: Output format (csv, xlsx, json, parquet)
        """
        if format not in ('csv', 'xlsx', 'json', 'parquet'):
            raise ValueError(f"Unsupported format: {format}")

        file_path = Path(file_path)
        resolved = _validate_path(file_path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'csv':
            df.to_csv(resolved, index=False)
        elif format == 'xlsx':
            df.to_excel(resolved, index=False)
        elif format == 'json':
            df.to_json(resolved)
        elif format == 'parquet':
            df.to_parquet(resolved)
