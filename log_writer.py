"""Модуль для записи логов поисковых запросов пользователя в MongoDB."""

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
from datetime import datetime
from typing import Dict, Any
from config import MONGODB_URL_EDIT, MONGODB_DATABASE, MONGODB_COLLECTION


def get_mongo_connection():
    """Создаёт и возвращает подключение к MongoDB для записи логов."""
    """
    Establish and return a MongoDB connection for writing.
    
    Returns:
        MongoClient: Active MongoDB client
        
    Raises:
        PyMongoError: If connection fails
    """
    try:
        client = MongoClient(MONGODB_URL_EDIT, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ismaster')
        return client
    except (ServerSelectionTimeoutError, PyMongoError) as e:
        print(f"❌ Ошибка подключения к MongoDB: {e}")
        raise


def log_search_query(
    search_type: str,
    params: Dict[str, Any],
    results_count: int
) -> bool:
    """Записывает поисковый запрос пользователя в MongoDB."""
    """
    Log a search query to MongoDB.
    
    Document structure:
    {
        "timestamp": "2025-05-01T15:34:00",
        "search_type": "keyword" or "genre__years_range",
        "params": {...},
        "results_count": int
    }
    
    Args:
        search_type (str): 'keyword' or 'genre__years_range'
        params (Dict): Search parameters (keyword, genre, years_range)
        results_count (int): Number of results found
        
    Returns:
        bool: True if logging succeeded, False otherwise
    """
    try:
        client = get_mongo_connection()
        # Явное указание базы данных и коллекции
        db = client["ich_edit"]
        collection = db["final_project_010825_daryna_abalmasova"]
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "search_type": search_type,
            "params": params,
            "results_count": results_count
        }
        
        result = collection.insert_one(log_entry)
        client.close()
        
        return result.inserted_id is not None
    except PyMongoError as e:
        print(f"❌ Ошибка при записи в MongoDB: {e}")
        return False


def log_keyword_search(keyword: str, results_count: int) -> bool:
    """Логирует поиск по ключевому слову в MongoDB."""
    """
    Log a keyword search query.
    
    Args:
        keyword (str): Search keyword
        results_count (int): Number of results found
        
    Returns:
        bool: Success status
    """
    params = {"keyword": keyword}
    return log_search_query("keyword", params, results_count)


def log_genre_years_search(
    genre: str,
    years_range: str,
    results_count: int
) -> bool:
    """Логирует поиск по жанру и диапазону лет в MongoDB."""
    """
    Log a genre and year range search query.
    
    Args:
        genre (str): Genre name
        years_range (str): Format: "YYYY-YYYY" (e.g., "2001-2010")
        results_count (int): Number of results found
        
    Returns:
        bool: Success status
    """
    params = {"genre": genre, "years_range": years_range}
    return log_search_query("genre__years_range", params, results_count)
