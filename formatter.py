"""
Formatter module for console output.
Provides functions for beautiful table formatting and result display.
"""

from typing import List, Dict
from tabulate import tabulate
from config import RESULTS_PER_PAGE


def print_header(title: str):
    """
    Print a formatted header.

    Args:
        title (str): Header title
    """
    print("\n" + "=" * 80)
    print(f"  {title}".center(80))
    print("=" * 80)


def print_subheader(title: str):
    """
    Print a formatted subheader.

    Args:
        title (str): Subheader title
    """
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}")


def print_movies_table(movies: List[Dict], page: int, total_count: int):
    """
    Print movies in a formatted table with pagination info.

    Args:
        movies (List[Dict]): List of movie dictionaries
        page (int): Current page number
        total_count (int): Total number of results
    """
    if not movies:
        print("\n❌ Фильмы не найдены.")
        return

    # Prepare table data
    table_data = []
    for idx, movie in enumerate(movies, 1):
        table_data.append([
            idx,
            movie.get('title', 'N/A'),
            movie.get('release_year', 'N/A'),
            movie.get('rating', 'N/A'),
            f"{movie.get('length', 'N/A')} мин"
        ])

    headers = ["№", "Название", "Год", "Рейтинг", "Длина"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))

    # Pagination info
    start_result = (page - 1) * RESULTS_PER_PAGE + 1
    end_result = min(page * RESULTS_PER_PAGE, total_count)
    print(
        f"\n📄 Показано результатов: {start_result}-{end_result} из {total_count}")

    max_pages = (total_count + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
    print(f"📑 Страница: {page}/{max_pages}")


def print_genres_list(genres: List[str]):
    """
    Print list of genres in formatted columns.

    Args:
        genres (List[str]): List of genre names
    """
    if not genres:
        print("❌ Жанры не найдены.")
        return

    # Create 3-column layout
    col_width = 25
    cols = 3

    print("\n🎬 Доступные жанры:\n")
    for i in range(0, len(genres), cols):
        row = genres[i:i + cols]
        formatted_row = [
            f"{j + 1 + i}. {genre:<{col_width}}" for j, genre in enumerate(row)]
        print("  ".join(formatted_row))


def print_year_range(min_year: int, max_year: int):
    """
    Print available year range.

    Args:
        min_year (int): Minimum year in database
        max_year (int): Maximum year in database
    """
    print(f"\n📅 Диапазон годов в базе: {min_year} - {max_year}")


def print_popular_searches(searches: List[Dict]):
    """
    Print most popular searches statistics.

    Args:
        searches (List[Dict]): List of popular searches from MongoDB
    """
    if not searches:
        print("\n❌ Нет данных о популярных запросах.")
        return

    print_subheader("🔥 5 Самых популярных запросов")

    table_data = []
    for idx, search in enumerate(searches, 1):
        try:
            search_id = search.get('_id', {})
            if not search_id:
                continue

            search_type = search_id.get('search_type')
            params = search_id.get('params')

            # Skip if essential fields are missing
            if not search_type or not params:
                continue

            frequency = search.get('frequency', 0)
            last_timestamp = search.get('last_timestamp', 'N/A')

            # Format params
            if search_type == 'keyword':
                params_str = f"Ключевое слово: '{
                    params.get(
                        'keyword', 'N/A')}'"
            else:
                params_str = f"Жанр: {params.get('genre', 'N/A')}, " \
                    f"Годы: {params.get('years_range', 'N/A')}"

            # Format timestamp safely
            timestamp_str = last_timestamp[:10] if isinstance(
                last_timestamp, str) else 'N/A'

            table_data.append([
                idx,
                search_type,
                params_str,
                frequency,
                timestamp_str
            ])
        except Exception:
            # Skip malformed documents
            continue

    if not table_data:
        print("\n❌ Нет корректных данных о популярных запросах.")
        return

    headers = ["№", "Тип", "Параметры", "Частота", "Последний поиск"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def print_latest_searches(searches: List[Dict]):
    """
    Print latest unique searches.

    Args:
        searches (List[Dict]): List of latest searches from MongoDB
    """
    if not searches:
        print("\n❌ Нет данных о последних запросах.")
        return

    print_subheader("⏰ 5 Последних уникальных запросов")

    table_data = []
    for idx, search in enumerate(searches, 1):
        try:
            search_id = search.get('_id', {})
            if not search_id:
                continue

            search_type = search_id.get('search_type')
            params = search_id.get('params')

            # Skip if essential fields are missing
            if not search_type or not params:
                continue

            timestamp = search.get('timestamp', 'N/A')
            results_count = search.get('results_count', 0)

            # Format params
            if search_type == 'keyword':
                params_str = f"Ключевое слово: '{
                    params.get(
                        'keyword', 'N/A')}'"
            else:
                params_str = f"Жанр: {params.get('genre', 'N/A')}, " \
                    f"Годы: {params.get('years_range', 'N/A')}"

            # Format timestamp safely
            timestamp_str = timestamp[:19] if isinstance(
                timestamp, str) else 'N/A'

            table_data.append([
                idx,
                search_type,
                params_str,
                results_count,
                timestamp_str
            ])
        except Exception:
            # Skip malformed documents
            continue

    if not table_data:
        print("\n❌ Нет корректных данных о последних запросах.")
        return

    headers = ["№", "Тип", "Параметры", "Результатов", "Время запроса"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def print_statistics_summary(total_searches: int):
    """
    Print statistics summary.

    Args:
        total_searches (int): Total number of searches
    """
    print_subheader("📊 Статистика")
    print(f"\n✓ Всего выполнено запросов: {total_searches}")
