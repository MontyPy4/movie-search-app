"""Модуль с утилитами, декораторами и настройкой логирования для приложения поиска фильмов."""

import functools
import logging
from typing import Any, Callable
from config import LOG_FILE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_function_call(func: Callable) -> Callable:
    """
    Decorator for logging function calls with arguments and results.
    Logs successful executions and exceptions.
    
    Args:
        func: Function to decorate
        
    Returns:
        Callable: Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        func_name = func.__name__
        try:
            logger.info(f"Calling {func_name} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"{func_name} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in {func_name}: {e}", exc_info=True)
            raise
    
    return wrapper


def log_database_query(query_type: str) -> Callable:
    """
    Decorator for logging database queries.
    
    Args:
        query_type: Type of query (e.g., 'SELECT', 'INSERT')
        
    Returns:
        Callable: Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.info(f"Executing {query_type} query: {func.__name__}")
            try:
                result = func(*args, **kwargs)
                if isinstance(result, tuple):
                    logger.info(f"Query returned {len(result[0]) if result[0] else 0} results")
                return result
            except Exception as e:
                logger.error(f"Database query failed: {e}")
                raise
        
        return wrapper
    
    return decorator


def safe_convert_to_int(value: str, default: int = None) -> int:
    """
    Safely convert string to integer with default fallback.
    
    Args:
        value: String value to convert
        default: Default value if conversion fails
        
    Returns:
        int: Converted value or default
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def validate_year_range(start_year: int, end_year: int,
                        min_allowed: int, max_allowed: int) -> bool:
    """
    Validate year range for search.
    
    Args:
        start_year: Start year from user input
        end_year: End year from user input
        min_allowed: Minimum allowed year in database
        max_allowed: Maximum allowed year in database
        
    Returns:
        bool: True if range is valid, False otherwise
    """
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        logger.warning("Year range validation failed: non-integer values")
        return False
    
    if start_year > end_year:
        logger.warning(f"Invalid range: start_year ({start_year}) > end_year ({end_year})")
        return False
    
    if start_year < min_allowed or end_year > max_allowed:
        logger.warning(f"Year range out of bounds: {start_year}-{end_year}, allowed: {min_allowed}-{max_allowed}")
        return False
    
    return True


def format_timestamp(timestamp: str) -> str:
    """
    Format MongoDB timestamp for display.
    
    Args:
        timestamp: ISO format timestamp string
        
    Returns:
        str: Formatted timestamp (YYYY-MM-DD HH:MM:SS)
    """
    try:
        if len(timestamp) >= 19:
            return timestamp[:19].replace('T', ' ')
        return timestamp
    except (ValueError, TypeError, AttributeError):
        return timestamp


class SearchCache:
    """
    Simple cache for search results to avoid repeated queries.
    """
    
    def __init__(self, max_size: int = 100):
        """
        Initialize cache.
        
        Args:
            max_size: Maximum number of cached items
        """
        self._cache = {}
        self._max_size = max_size
        self._access_count = {}
    
    def get(self, key: str) -> Any:
        """
        Get item from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Any: Cached value or None if not found
        """
        if key in self._cache:
            self._access_count[key] = self._access_count.get(key, 0) + 1
            return self._cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """
        Set item in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        if len(self._cache) >= self._max_size:
            # Remove least accessed item
            least_accessed = min(self._access_count, key=self._access_count.get)
            del self._cache[least_accessed]
            del self._access_count[least_accessed]
        
        self._cache[key] = value
        self._access_count[key] = 0
    
    def clear(self) -> None:
        """Clear all cache."""
        self._cache.clear()
        self._access_count.clear()


# Global cache instance
search_cache = SearchCache()
