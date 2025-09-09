"""
Error Handling Utilities for TradingAgents

This module provides standardized error handling, logging, and retry
mechanisms for the TradingAgents framework.
"""

import logging
import functools
import time
from typing import Any, Callable, Optional, Type, Union, List
from datetime import datetime


class TradingAgentsError(Exception):
    """Base exception for TradingAgents framework."""
    pass


class ConfigurationError(TradingAgentsError):
    """Raised when there are configuration issues."""
    pass


class DataSourceError(TradingAgentsError):
    """Raised when data source operations fail."""
    pass


class APIError(TradingAgentsError):
    """Raised when API calls fail."""
    pass


class AnalysisError(TradingAgentsError):
    """Raised when analysis operations fail."""
    pass


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging for TradingAgents.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file to write logs to
        format_string: Custom format string for log messages
    
    Returns:
        Configured logger instance
    """
    
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Create logger
    logger = logging.getLogger("tradingagents")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Union[Type[Exception], tuple] = Exception,
    logger: Optional[logging.Logger] = None
):
    """
    Decorator for retrying function calls with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between attempts in seconds
        backoff: Exponential backoff multiplier
        exceptions: Exception types to catch and retry
        logger: Logger instance for retry messages
    
    Returns:
        Decorated function with retry logic
    """
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts - 1:
                        # Last attempt failed
                        if logger:
                            logger.error(f"Function {func.__name__} failed after {max_attempts} attempts: {e}")
                        raise
                    
                    if logger:
                        logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {current_delay}s...")
                    
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            # Should never reach here, but just in case
            raise last_exception
        
        return wrapper
    return decorator


def safe_execute(
    func: Callable,
    default_return: Any = None,
    error_message: str = None,
    logger: Optional[logging.Logger] = None,
    raise_on_error: bool = False
) -> Any:
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        default_return: Value to return if function fails
        error_message: Custom error message
        logger: Logger instance
        raise_on_error: Whether to re-raise the exception
    
    Returns:
        Function result or default_return on error
    """
    
    try:
        return func()
    except Exception as e:
        message = error_message or f"Error executing {func.__name__}: {e}"
        
        if logger:
            logger.error(message)
        else:
            print(f"ERROR: {message}")
        
        if raise_on_error:
            raise
        
        return default_return


def validate_inputs(**validators):
    """
    Decorator for validating function inputs.
    
    Args:
        **validators: Dict of parameter_name -> validation_function
    
    Returns:
        Decorated function with input validation
    """
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature for parameter mapping
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate parameters
            for param_name, validator in validators.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    
                    try:
                        if not validator(value):
                            raise ValueError(f"Validation failed for parameter '{param_name}' with value: {value}")
                    except Exception as e:
                        raise ValueError(f"Validation error for parameter '{param_name}': {e}")
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def handle_api_errors(
    api_name: str,
    logger: Optional[logging.Logger] = None,
    default_return: Any = None
):
    """
    Decorator for handling API-specific errors.
    
    Args:
        api_name: Name of the API for error messages
        logger: Logger instance
        default_return: Default value to return on error
    
    Returns:
        Decorated function with API error handling
    """
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f"{api_name} API error in {func.__name__}: {e}"
                
                if logger:
                    logger.error(error_msg)
                else:
                    print(f"ERROR: {error_msg}")
                
                # Convert to appropriate exception type
                if "timeout" in str(e).lower():
                    raise APIError(f"{api_name} API timeout: {e}")
                elif "rate limit" in str(e).lower() or "429" in str(e):
                    raise APIError(f"{api_name} API rate limit exceeded: {e}")
                elif "authentication" in str(e).lower() or "401" in str(e):
                    raise APIError(f"{api_name} API authentication failed: {e}")
                else:
                    raise APIError(f"{api_name} API error: {e}")
        
        return wrapper
    return decorator


# Common validators
def is_valid_date(date_str: str) -> bool:
    """Validate date string in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_ticker(ticker: str) -> bool:
    """Validate ticker symbol."""
    if not isinstance(ticker, str):
        return False
    
    # Basic validation - alphanumeric, 1-10 characters
    return ticker.isalnum() and 1 <= len(ticker) <= 10


def is_positive_int(value: int) -> bool:
    """Validate positive integer."""
    return isinstance(value, int) and value > 0


def is_non_empty_string(value: str) -> bool:
    """Validate non-empty string."""
    return isinstance(value, str) and len(value.strip()) > 0


# Get default logger instance
logger = setup_logging()
