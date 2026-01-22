"""Модуль для поиска фильмов в базе MySQL: ключевые слова, жанры, годы, пагинация."""

import pymysql
from typing import List, Dict, Tuple
from config import (
    MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE,
    MYSQL_PORT, RESULTS_PER_PAGE
)


def get_mysql_connection():
    """
    Establish and return a MySQL connection.

    Returns:
        pymysql.Connection: Active MySQL connection

    Raises:
        pymysql.MySQLError: If connection fails
    """
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"❌ Ошибка подключения к MySQL: {e}")
        raise


def get_all_genres() -> List[str]:
    """
    Fetch all unique genres from the database.

    SQL Query:
    SELECT DISTINCT name FROM category ORDER BY name

    Returns:
        List[str]: List of genre names
    """
    try:
        conn = get_mysql_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT name
                FROM category
                ORDER BY name
            """)
            genres = [row['name'] for row in cursor.fetchall()]
        conn.close()
        return genres
    except pymysql.MySQLError as e:
        print(f"❌ Ошибка при получении жанров: {e}")
        return []


def get_year_range() -> Tuple[int, int]:
    """
    Fetch minimum and maximum release years from database.

    SQL Query:
    SELECT MIN(release_year) as min_year, MAX(release_year) as max_year FROM film

    Returns:
        Tuple[int, int]: (min_year, max_year)
    """
    try:
        conn = get_mysql_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    MIN(release_year) as min_year,
                    MAX(release_year) as max_year
                FROM film
            """)
            result = cursor.fetchone()
        conn.close()

        min_year = result['min_year'] or 2000
        max_year = result['max_year'] or 2024
        return (min_year, max_year)
    except pymysql.MySQLError as e:
        print(f"❌ Ошибка при получении диапазона годов: {e}")
        return (2000, 2024)


def search_by_keyword(keyword: str, page: int = 1) -> Tuple[List[Dict], int]:
    """
    Search movies by keyword (title).

    SQL Query:
    SELECT f.title, f.release_year, f.rating, f.length
    FROM film f
    WHERE f.title LIKE %keyword%
    ORDER BY f.title
    LIMIT results_per_page OFFSET (page-1)*results_per_page

    Args:
        keyword (str): Search keyword
        page (int): Page number (1-based)

    Returns:
        Tuple[List[Dict], int]: (movies list, total count)
    """
    try:
        conn = get_mysql_connection()
        with conn.cursor() as cursor:
            # Get total count
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM film
                WHERE title LIKE %s
            """, (f"%{keyword}%",))
            total_count = cursor.fetchone()['count']

            # Get paginated results
            offset = (page - 1) * RESULTS_PER_PAGE
            cursor.execute("""
                SELECT
                    film_id,
                    title,
                    release_year,
                    rating,
                    length
                FROM film
                WHERE title LIKE %s
                ORDER BY title
                LIMIT %s OFFSET %s
            """, (f"%{keyword}%", RESULTS_PER_PAGE, offset))

            movies = cursor.fetchall()
        conn.close()

        return (movies, total_count)
    except pymysql.MySQLError as e:
        print(f"❌ Ошибка при поиске по ключевому слову: {e}")
        return ([], 0)


def search_by_genre_and_years(
    genre: str,
    start_year: int,
    end_year: int,
    page: int = 1
) -> Tuple[List[Dict], int]:
    """
    Search movies by genre and year range.

    SQL Query:
    SELECT DISTINCT f.title, f.release_year, f.rating, f.length
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = genre AND f.release_year BETWEEN start_year AND end_year
    ORDER BY f.release_year DESC, f.title
    LIMIT results_per_page OFFSET (page-1)*results_per_page

    Args:
        genre (str): Genre name
        start_year (int): Start year (inclusive)
        end_year (int): End year (inclusive)
        page (int): Page number (1-based)

    Returns:
        Tuple[List[Dict], int]: (movies list, total count)
    """
    try:
        conn = get_mysql_connection()
        with conn.cursor() as cursor:
            # Get total count
            cursor.execute("""
                SELECT COUNT(DISTINCT f.film_id) as count
                FROM film f
                JOIN film_category fc ON f.film_id = fc.film_id
                JOIN category c ON fc.category_id = c.category_id
                WHERE c.name = %s
                AND f.release_year BETWEEN %s AND %s
            """, (genre, start_year, end_year))
            total_count = cursor.fetchone()['count']

            # Get paginated results
            offset = (page - 1) * RESULTS_PER_PAGE
            cursor.execute("""
                SELECT DISTINCT
                    f.film_id,
                    f.title,
                    f.release_year,
                    f.rating,
                    f.length
                FROM film f
                JOIN film_category fc ON f.film_id = fc.film_id
                JOIN category c ON fc.category_id = c.category_id
                WHERE c.name = %s
                AND f.release_year BETWEEN %s AND %s
                ORDER BY f.release_year DESC, f.title
                LIMIT %s OFFSET %s
            """, (genre, start_year, end_year, RESULTS_PER_PAGE, offset))

            movies = cursor.fetchall()
        conn.close()

        return (movies, total_count)
    except pymysql.MySQLError as e:
        print(f"❌ Ошибка при поиске по жанру и годам: {e}")
        return ([], 0)
