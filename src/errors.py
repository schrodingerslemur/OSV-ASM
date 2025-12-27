class AssemblyError(Exception):
    """Custom exception for assembly errors."""
    pass

class MissingOperationError(AssemblyError):
    """Exception raised for missing operations."""
    pass

class InvalidOperationError(AssemblyError):
    """Exception raised for invalid operations."""
    pass