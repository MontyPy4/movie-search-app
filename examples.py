"""
Examples and demonstration of the Movie Search application functionality.
Shows how to use the modules programmatically.
"""

# Example 1: Direct keyword search without UI
# ============================================

from mysql_connector import search_by_keyword, get_all_genres, get_year_range
from log_writer import log_keyword_search
from formatter import print_movies_table

def example_keyword_search():
    """Example of performing a keyword search."""
    print("Example 1: Keyword Search")
    print("-" * 50)
    
    keyword = "Matrix"
    movies, total_count = search_by_keyword(keyword, page=1)
    
    if movies:
        log_keyword_search(keyword, total_count)
        print_movies_table(movies, page=1, total_count=total_count)
    else:
        print(f"No movies found for: {keyword}")


# Example 2: Genre and year range search
# ========================================

from mysql_connector import search_by_genre_and_years
from log_writer import log_genre_years_search

def example_genre_years_search():
    """Example of performing a genre and year range search."""
    print("\n\nExample 2: Genre and Year Range Search")
    print("-" * 50)
    
    genre = "Action"
    start_year = 2005
    end_year = 2010
    
    movies, total_count = search_by_genre_and_years(
        genre, start_year, end_year, page=1
    )
    
    if movies:
        years_range = f"{start_year}-{end_year}"
        log_genre_years_search(genre, years_range, total_count)
        print_movies_table(movies, page=1, total_count=total_count)
    else:
        print(f"No movies found for genre={genre}, years={start_year}-{end_year}")


# Example 3: Getting available genres
# ====================================

def example_get_genres():
    """Example of getting all available genres."""
    print("\n\nExample 3: Available Genres")
    print("-" * 50)
    
    genres = get_all_genres()
    print(f"Total genres: {len(genres)}")
    print("First 10 genres:", genres[:10])


# Example 4: Getting year range
# ==============================

def example_get_year_range():
    """Example of getting available year range."""
    print("\n\nExample 4: Available Year Range")
    print("-" * 50)
    
    min_year, max_year = get_year_range()
    print(f"Films in database range from {min_year} to {max_year}")


# Example 5: Getting statistics
# ==============================

from log_stats import (
    get_popular_searches, get_latest_searches, get_total_searches_count
)
from formatter import print_popular_searches, print_latest_searches

def example_statistics():
    """Example of getting search statistics."""
    print("\n\nExample 5: Search Statistics")
    print("-" * 50)
    
    # Popular searches
    popular = get_popular_searches()
    print(f"\nMost popular searches: {len(popular)} entries")
    print_popular_searches(popular)
    
    # Latest searches
    latest = get_latest_searches()
    print(f"\nLatest searches: {len(latest)} entries")
    print_latest_searches(latest)
    
    # Total count
    total = get_total_searches_count()
    print(f"\nTotal searches in database: {total}")


# Example 6: Pagination example
# ==============================

def example_pagination():
    """Example of handling pagination."""
    print("\n\nExample 6: Pagination")
    print("-" * 50)
    
    keyword = "The"
    page = 1
    
    while True:
        movies, total_count = search_by_keyword(keyword, page=page)
        
        if not movies:
            print(f"No more results on page {page}")
            break
        
        print(f"\nPage {page}:")
        print_movies_table(movies, page=page, total_count=total_count)
        
        max_pages = (total_count + 10 - 1) // 10  # 10 results per page
        
        if page >= max_pages:
            break
        
        page += 1


# Example 7: Error handling
# ==========================

def example_error_handling():
    """Example of error handling."""
    print("\n\nExample 7: Error Handling")
    print("-" * 50)
    
    try:
        # Try to search with empty keyword
        movies, total_count = search_by_keyword("", page=1)
        print(f"Found {total_count} movies")
    except Exception as e:
        print(f"Error during search: {e}")
    
    try:
        # Try to search with invalid page number
        movies, total_count = search_by_genre_and_years(
            "Action", 1999, 1990, page=1  # invalid year range
        )
    except Exception as e:
        print(f"Error with invalid year range: {e}")


# Example 8: Using utilities
# ============================

from utils import (
    safe_convert_to_int, validate_year_range,
    format_timestamp, log_function_call
)

def example_utilities():
    """Example of using utility functions."""
    print("\n\nExample 8: Utility Functions")
    print("-" * 50)
    
    # Safe integer conversion
    value = safe_convert_to_int("2005", default=2000)
    print(f"Converted year: {value}")
    
    # Year range validation
    is_valid = validate_year_range(2005, 2010, 2000, 2024)
    print(f"Year range valid: {is_valid}")
    
    # Timestamp formatting
    timestamp = "2025-01-15T10:30:45.123456"
    formatted = format_timestamp(timestamp)
    print(f"Formatted timestamp: {formatted}")


# Example 9: Decorator usage
# ============================

from utils import log_function_call

@log_function_call
def example_decorated_function(search_term: str):
    """Example function with logging decorator."""
    print(f"Searching for: {search_term}")
    return search_by_keyword(search_term, page=1)


def example_decorators():
    """Example of using decorators."""
    print("\n\nExample 9: Decorators")
    print("-" * 50)
    
    try:
        movies, count = example_decorated_function("Matrix")
        print(f"Results: {count} movies found")
    except Exception as e:
        print(f"Error: {e}")


# Example 10: Search cache usage
# ===============================

from utils import search_cache

def example_caching():
    """Example of using search cache."""
    print("\n\nExample 10: Search Caching")
    print("-" * 50)
    
    # First search (cached)
    cache_key = "Matrix:1"
    cached_result = search_cache.get(cache_key)
    
    if cached_result:
        print(f"Using cached result for {cache_key}")
    else:
        print(f"Fetching fresh result for {cache_key}")
        movies, count = search_by_keyword("Matrix", page=1)
        search_cache.set(cache_key, (movies, count))
    
    # Second search (from cache)
    cached_result = search_cache.get(cache_key)
    if cached_result:
        print(f"Using cached result for {cache_key} (second attempt)")


# ==========================================
# Run examples
# ==========================================

if __name__ == '__main__':
    import sys
    
    examples = {
        '1': ('Найти фильм по ключевому слову', example_keyword_search),
        '2': ('Найти фильмы по жанру и годам выпуска', example_genre_years_search),
        '3': ('Посмотреть все доступные жанры', example_get_genres),
        '4': ('Узнать диапазон лет фильмов в базе', example_get_year_range),
        '5': ('Посмотреть статистику поисковых запросов', example_statistics),
        '6': ('Как работает пагинация результатов', example_pagination),
        '7': ('Примеры обработки ошибок', example_error_handling),
        '8': ('Использование вспомогательных функций', example_utilities),
        '9': ('Как работают декораторы логирования', example_decorators),
        '10': ('Кэширование результатов поиска', example_caching),
    }
    
    if len(sys.argv) > 1 and sys.argv[1] in examples:
        try:
            print(f"\nЗапуск примера {sys.argv[1]}: {examples[sys.argv[1]][0]}")
            print("=" * 60)
            examples[sys.argv[1]][1]()
            print("\n✅ Пример выполнен успешно!")
        except Exception as e:
            print(f"\n❌ Ошибка при запуске примера: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("Приложение для поиска фильмов - Примеры использования")
        print("=" * 60)
        print("\nДоступные примеры:")
        for num, (description, func) in examples.items():
            print(f"  {num}. {description}")
        
        print("\nИспользование: python examples.py <номер>")
        print("Пример: python examples.py 1")
