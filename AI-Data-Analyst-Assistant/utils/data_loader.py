"""
Data loading utility module
"""
import logging
import pandas as pd
from pathlib import Path
from typing import Union

from .exceptions import DataLoadError, DataSaveError

logger = logging.getLogger(__name__)


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
            DataLoadError: If file cannot be parsed
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = file_path.suffix.lower()

        if suffix not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file format: {suffix}. "
                f"Supported formats: {', '.join(sorted(self.SUPPORTED_FORMATS))}"
            )

        try:
            if suffix == '.csv':
                return pd.read_csv(file_path)
            elif suffix in {'.xlsx', '.xls'}:
                return pd.read_excel(file_path)
            elif suffix == '.json':
                return pd.read_json(file_path)
            elif suffix == '.parquet':
                return pd.read_parquet(file_path)
        except (pd.errors.ParserError, pd.errors.EmptyDataError) as e:
            raise DataLoadError(str(file_path), f"Parsing error: {e}") from e
        except UnicodeDecodeError as e:
            raise DataLoadError(str(file_path), f"Encoding error: {e}") from e
        except PermissionError as e:
            raise DataLoadError(str(file_path), f"Permission denied: {e}") from e
        except Exception as e:
            logger.error("Unexpected error loading '%s': %s", file_path, e)
            raise DataLoadError(str(file_path), str(e)) from e

        # Should not reach here, but guard against future format additions
        raise ValueError(f"Unsupported file format: {suffix}")

    def save_data(self, df: pd.DataFrame, file_path: Union[str, Path], format: str = 'csv') -> None:
        """
        Save data to file

        Args:
            df: DataFrame to save
            file_path: Output file path
            format: Output format (csv, xlsx, json, parquet)

        Raises:
            ValueError: If format is not supported
            DataSaveError: If file cannot be written
        """
        supported_save_formats = {'csv', 'xlsx', 'json', 'parquet'}
        if format not in supported_save_formats:
            raise ValueError(
                f"Unsupported format: '{format}'. "
                f"Supported: {', '.join(sorted(supported_save_formats))}"
            )

        file_path = Path(file_path)

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise DataSaveError(str(file_path), f"Cannot create directory: {e}") from e

        try:
            if format == 'csv':
                df.to_csv(file_path, index=False)
            elif format == 'xlsx':
                df.to_excel(file_path, index=False)
            elif format == 'json':
                df.to_json(file_path)
            elif format == 'parquet':
                df.to_parquet(file_path)
        except PermissionError as e:
            raise DataSaveError(str(file_path), f"Permission denied: {e}") from e
        except OSError as e:
            raise DataSaveError(str(file_path), f"I/O error: {e}") from e
        except Exception as e:
            logger.error("Unexpected error saving to '%s': %s", file_path, e)
            raise DataSaveError(str(file_path), str(e)) from e
