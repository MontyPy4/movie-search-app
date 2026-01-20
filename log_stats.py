"""
MongoDB log statistics module for retrieving search analytics.
Provides functions to get most popular and latest search queries.
"""
"""Модуль для анализа логов: статистика популярных и уникальных запросов из MongoDB."""

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import List, Dict, Any
from config import MONGODB_URL_READ, MONGODB_DATABASE, MONGODB_COLLECTION, STATS_LIMIT

#############
def get_mongo_read_connection():
    """Создаёт и возвращает подключение к MongoDB для чтения статистики."""
    """
    Establish and return a MongoDB connection for reading.
    
    Returns:
        MongoClient: Active MongoDB client
        
    Raises:
        PyMongoError: If connection fails
    """
    try:
        client = MongoClient(MONGODB_URL_READ, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ismaster')
        return client
    except PyMongoError as e:
        print(f"❌ Ошибка подключения к MongoDB для чтения: {e}")
        raise


def get_popular_searches() -> List[Dict[str, Any]]:
    """Возвращает 5 самых популярных поисковых запросов из логов MongoDB."""
    """
    Get most popular searches by frequency (top 5).
    
    MongoDB Aggregation Pipeline:
    1. Group by search_type and params, count occurrences
    2. Sort by count descending
    3. Limit to STATS_LIMIT results
    
    Returns:
        List[Dict]: List of popular searches with frequency info
    """
    try:
        client = get_mongo_read_connection()
        # Явное указание базы данных и коллекции
        db = client["ich_edit"]
        collection = db["final_project_010825_daryna_abalmasova"]
        
        pipeline = [
            # Filter out documents with None search_type
            {
                "$match": {
                    "search_type": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": {
                        "search_type": "$search_type",
                        "params": "$params"
                    },
                    "frequency": {"$sum": 1},
                    "last_timestamp": {"$max": "$timestamp"},
                    "avg_results": {"$avg": "$results_count"}
                }
            },
            {"$sort": {"frequency": -1}},
            {"$limit": STATS_LIMIT}
        ]
        
        results = list(collection.aggregate(pipeline))
        client.close()
        
        return results
    except PyMongoError as e:
        print(f"❌ Ошибка при получении популярных запросов: {e}")
        return []


def get_latest_searches() -> List[Dict[str, Any]]:
    """Возвращает 5 последних уникальных поисковых запросов из логов MongoDB."""
    """
    Get latest unique searches (top 5, most recent first).
    
    MongoDB Query:
    Find all unique search combinations, sorted by timestamp descending, limit 5
    
    Returns:
        List[Dict]: List of latest unique searches
    """
    try:
        client = get_mongo_read_connection()
        # Явное указание базы данных и коллекции
        db = client["ich_edit"]
        collection = db["final_project_010825_daryna_abalmasova"]
        
        # Get unique search combinations with latest timestamp
        pipeline = [
            # Filter out documents with None search_type
            {
                "$match": {
                    "search_type": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": {
                        "search_type": "$search_type",
                        "params": "$params"
                    },
                    "timestamp": {"$max": "$timestamp"},
                    "results_count": {"$first": "$results_count"}
                }
            },
            {"$sort": {"timestamp": -1}},
            {"$limit": STATS_LIMIT}
        ]
        
        results = list(collection.aggregate(pipeline))
        client.close()
        
        return results
    except PyMongoError as e:
        print(f"❌ Ошибка при получении последних запросов: {e}")
        return []


def get_total_searches_count() -> int:
    """Возвращает общее количество поисковых запросов из логов MongoDB."""
    """
    Get total number of searches in the collection.
    
    Returns:
        int: Total count of search documents
    """
    try:
        client = get_mongo_read_connection()
        # Явное указание базы данных и коллекции
        db = client["ich_edit"]
        collection = db["final_project_010825_daryna_abalmasova"]
        
        count = collection.count_documents({})
        client.close()
        
        return count
    except PyMongoError as e:
        print(f"❌ Ошибка при подсчёте запросов: {e}")
        return 0
