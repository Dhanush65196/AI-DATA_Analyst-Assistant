"""
Custom exceptions for the AI Data Analyst Assistant.

Provides a clear exception hierarchy so callers can distinguish
between different failure modes and handle them appropriately.
"""


class DataAnalystError(Exception):
    """Base exception for all application errors."""

    pass


class DataLoadError(DataAnalystError):
    """Raised when data cannot be loaded or parsed."""

    def __init__(self, file_path: str, reason: str):
        self.file_path = file_path
        self.reason = reason
        super().__init__(f"Failed to load '{file_path}': {reason}")


class DataSaveError(DataAnalystError):
    """Raised when data cannot be saved."""

    def __init__(self, file_path: str, reason: str):
        self.file_path = file_path
        self.reason = reason
        super().__init__(f"Failed to save to '{file_path}': {reason}")


class AnalysisError(DataAnalystError):
    """Raised when data analysis fails."""

    def __init__(self, operation: str, reason: str):
        self.operation = operation
        self.reason = reason
        super().__init__(f"Analysis failed during '{operation}': {reason}")


class LLMError(DataAnalystError):
    """Raised when LLM operations fail."""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"LLM error: {reason}")


class LLMConfigurationError(LLMError):
    """Raised when LLM is not properly configured."""

    pass
