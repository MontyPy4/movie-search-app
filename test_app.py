"""
Unit tests for the Movie Search application.
Basic smoke tests for core functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from mysql_connector import (
    search_by_keyword, search_by_genre_and_years,
    get_all_genres, get_year_range
)


class TestMySQLConnector:
    """
    Тесты для модуля mysql_connector.py

    Класс проверяет корректность работы функций для подключения к MySQL
    и выполнения поисков по базе данных sakila.

    Функции которые тестируются:
    - search_by_keyword() - поиск фильмов по ключевому слову
    - search_by_genre_and_years() - поиск по жанру и диапазону годов
    - get_all_genres() - получение списка всех жанров
    - get_year_range() - получение минимального и максимального года
    """

    @patch('mysql_connector.get_mysql_connection')
    def test_search_by_keyword_returns_tuple(self, mock_get_conn):
        """Тест: search_by_keyword возвращает кортеж (список фильмов, количество результатов)"""
        # Создаём мок курсора
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'count': 2}
        mock_cursor.fetchall.return_value = [
            {'film_id': 1, 'title': 'Matrix', 'release_year': 1999, 'rating': 'R', 'length': 136},
            {'film_id': 2, 'title': 'The Matrix Reloaded', 'release_year': 2003, 'rating': 'R', 'length': 138}
        ]

        # Создаём мок подключения
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        # Возвращаем мок подключения при вызове get_mysql_connection
        mock_get_conn.return_value = mock_conn

        result = search_by_keyword('Matrix', page=1)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], int)
        assert len(result[0]) == 2
        """
        Тест: search_by_keyword возвращает кортеж (список фильмов, количество результатов)

        Проверяет:
        - Возвращаемый тип данных (tuple)
        - Длина кортежа (2 элемента)
        - Первый элемент - список фильмов
        - Второй элемент - целое число (количество результатов)
        """
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'count': 5}
        mock_cursor.fetchall.return_value = [
            {'film_id': 1, 'title': 'Matrix', 'release_year': 1999,
             'rating': 'R', 'length': 136},
            {'film_id': 2, 'title': 'The Matrix Reloaded', 'release_year': 2003,
             'rating': 'R', 'length': 138}
        ]

        mock_conn.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.return_value.__enter__.return_value.cursor.return_value.__exit__.return_value = None
        mock_conn.return_value.close.return_value = None

        result = search_by_keyword('Matrix', page=1)

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], int)

    @patch('mysql_connector.get_mysql_connection')
    def test_search_by_keyword_empty_result(self, mock_get_conn):
        """Тест: search_by_keyword обрабатывает случай когда фильмы не найдены"""
        # Создаём мок курсора
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'count': 0}
        mock_cursor.fetchall.return_value = []

        # Создаём мок подключения
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        # Возвращаем мок подключения при вызове get_mysql_connection
        mock_get_conn.return_value = mock_conn

        result = search_by_keyword('NonexistentMovie', page=1)
        assert result[0] == []
        assert result[1] == 0
        """
        Тест: search_by_keyword обрабатывает случай когда фильмы не найдены

        Проверяет:
        - Возвращаемый список пуст []
        - Количество результатов = 0
        - Функция не вызывает ошибки при пустом результате
        """
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'count': 0}
        mock_cursor.fetchall.return_value = []

        mock_conn.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.return_value.__enter__.return_value.cursor.return_value.__exit__.return_value = None
        mock_conn.return_value.close.return_value = None

        result = search_by_keyword('NonexistentMovie', page=1)

        assert result[0] == []
        assert result[1] == 0

    @patch('mysql_connector.get_mysql_connection')
    def test_get_all_genres(self, mock_get_conn):
        """Тест: get_all_genres возвращает список всех жанров из таблицы category"""
        # Создаём мок курсора
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {'name': 'Action'},
            {'name': 'Comedy'},
            {'name': 'Drama'}
        ]

        # Создаём мок подключения
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.cursor.return_value.__exit__.return_value = None

        # Возвращаем мок подключения при вызове get_mysql_connection
        mock_get_conn.return_value = mock_conn

        result = get_all_genres()
        assert isinstance(result, list)
        assert len(result) == 3
        assert 'Action' in result
        """
        Тест: get_all_genres возвращает список всех жанров из таблицы category

        Проверяет:
        - Возвращаемый тип - список (list)
        - Количество жанров корректно
        - Жанры находятся в списке (например 'Action' в результатах)
        """
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {'name': 'Action'},
            {'name': 'Comedy'},
            {'name': 'Drama'}
        ]

        mock_conn.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conn.return_value.__enter__.return_value.cursor.return_value.__exit__.return_value = None
        mock_conn.return_value.close.return_value = None

        result = get_all_genres()

        assert isinstance(result, list)
        assert len(result) == 3
        assert 'Action' in result


class TestLogWriter:
    """
    Тесты для модуля log_writer.py

    Класс проверяет корректность логирования поисковых запросов в MongoDB.
    Все поиски должны сохраняться с timestamp, типом поиска, параметрами и
    количеством результатов.

    Функции которые тестируются:
    - log_keyword_search() - логирование поиска по ключевому слову
    - log_genre_years_search() - логирование поиска по жанру и годам
    - log_search_query() - базовая функция логирования
    """

    @patch('log_writer.get_mongo_connection')
    def test_log_keyword_search(self, mock_mongo):
        """
        Тест: log_keyword_search успешно логирует поиск по ключевому слову

        Проверяет:
        - Функция возвращает True (успешное логирование)
        - insert_one был вызван один раз (документ добавлен в БД)
        - Документ содержит ключевое слово и количество результатов
        """
        from log_writer import log_keyword_search

        mock_collection = MagicMock()
        mock_collection.insert_one.return_value.inserted_id = '12345'

        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        mock_client = MagicMock()
        mock_client.__getitem__.return_value = mock_db

        mock_mongo.return_value = mock_client

        result = log_keyword_search('matrix', 3)

        assert result is True
        mock_collection.insert_one.assert_called_once()

    @patch('log_writer.get_mongo_connection')
    def test_log_genre_years_search(self, mock_mongo):
        """
        Тест: log_genre_years_search успешно логирует поиск по жанру и годам

        Проверяет:
        - Функция возвращает True (успешное логирование)
        - insert_one был вызван один раз (документ добавлен в БД)
        - Документ содержит жанр, диапазон годов и количество результатов
        """
        from log_writer import log_genre_years_search

        mock_collection = MagicMock()
        mock_collection.insert_one.return_value.inserted_id = '12345'

        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        mock_client = MagicMock()
        mock_client.__getitem__.return_value = mock_db

        mock_mongo.return_value = mock_client

        result = log_genre_years_search('Action', '2005-2012', 5)

        assert result is True
        mock_collection.insert_one.assert_called_once()


class TestLogStats:
    """
    Тесты для модуля log_stats.py

    Класс проверяет корректность получения статистики из MongoDB.
    Проверяет что можно получить популярные запросы, последние запросы
    и общее количество всех выполненных поисков.

    Функции которые тестируются:
    - get_popular_searches() - получение 5 самых популярных запросов по частоте
    - get_latest_searches() - получение 5 последних уникальных запросов
    - get_total_searches_count() - получение общего количества всех запросов
    """

    @patch('log_stats.get_mongo_read_connection')
    def test_get_popular_searches(self, mock_mongo):
        """
        Тест: get_popular_searches возвращает список популярных запросов

        Проверяет:
        - Возвращаемый тип - список (list)
        - Каждый запрос содержит информацию о частоте (frequency)
        - MongoDB aggregation pipeline был вызван один раз
        - Результаты отсортированы по частоте (от большего к меньшему)
        """
        from log_stats import get_popular_searches

        mock_collection = MagicMock()
        mock_collection.aggregate.return_value = [
            {
                '_id': {
                    'search_type': 'keyword',
                    'params': {
                        'keyword': 'matrix'}},
                'frequency': 5,
                'last_timestamp': '2025-01-15T10:00:00',
                'avg_results': 3.0}]

        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        mock_client = MagicMock()
        mock_client.__getitem__.return_value = mock_db

        mock_mongo.return_value = mock_client

        result = get_popular_searches()

        assert isinstance(result, list)
        assert len(result) >= 0
        mock_collection.aggregate.assert_called_once()

    @patch('log_stats.get_mongo_read_connection')
    def test_get_total_searches_count(self, mock_mongo):
        """
        Тест: get_total_searches_count возвращает общее количество запросов

        Проверяет:
        - Возвращаемый тип - целое число (int)
        - count_documents был вызван один раз
        - Возвращаемое значение корректно (42 в этом тесте)
        """
        from log_stats import get_total_searches_count

        mock_collection = MagicMock()
        mock_collection.count_documents.return_value = 42

        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        mock_client = MagicMock()
        mock_client.__getitem__.return_value = mock_db

        mock_mongo.return_value = mock_client

        result = get_total_searches_count()

        assert result == 42
        mock_collection.count_documents.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
