"""одуль для анализа логов: статистика популярных и уникальных запросов."""

from typing import List, Dict, Any
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import MONGODB_URL_READ, STATS_LIMIT


#############


def get_mongo_read_connection():
    """РЎРѕР·РґР°С‘С‚ Рё РІРѕР·РІСЂР°С‰Р°РµС‚ РїРѕРґРєР»СЋС‡РµРЅРёРµ Рє MongoDB РґР»СЏ С‡С‚РµРЅРёСЏ СЃС‚Р°С‚РёСЃС‚РёРєРё."""
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
        print(f"вќЊ РћС€РёР±РєР° РїРѕРґРєР»СЋС‡РµРЅРёСЏ Рє MongoDB РґР»СЏ С‡С‚РµРЅРёСЏ: {e}")
        raise


def get_popular_searches() -> List[Dict[str, Any]]:
    """Р’РѕР·РІСЂР°С‰Р°РµС‚ 5 СЃР°РјС‹С… РїРѕРїСѓР»СЏСЂРЅС‹С… РїРѕРёСЃРєРѕРІС‹С… Р·Р°РїСЂРѕСЃРѕРІ РёР· Р»РѕРіРѕРІ MongoDB."""
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
        # РЇРІРЅРѕРµ СѓРєР°Р·Р°РЅРёРµ Р±Р°Р·С‹ РґР°РЅРЅС‹С… Рё РєРѕР»Р»РµРєС†РёРё
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
        print(f"вќЊ РћС€РёР±РєР° РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РїРѕРїСѓР»СЏСЂРЅС‹С… Р·Р°РїСЂРѕСЃРѕРІ: {e}")
        return []


def get_latest_searches() -> List[Dict[str, Any]]:
    """Р’РѕР·РІСЂР°С‰Р°РµС‚ 5 РїРѕСЃР»РµРґРЅРёС… СѓРЅРёРєР°Р»СЊРЅС‹С… РїРѕРёСЃРєРѕРІС‹С… Р·Р°РїСЂРѕСЃРѕРІ РёР· Р»РѕРіРѕРІ MongoDB."""
    """
    Get latest unique searches (top 5, most recent first).

    MongoDB Query:
    Find all unique search combinations, sorted by timestamp descending, limit 5

    Returns:
        List[Dict]: List of latest unique searches
    """
    try:
        client = get_mongo_read_connection()
        # РЇРІРЅРѕРµ СѓРєР°Р·Р°РЅРёРµ Р±Р°Р·С‹ РґР°РЅРЅС‹С… Рё РєРѕР»Р»РµРєС†РёРё
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
        print(f"вќЊ РћС€РёР±РєР° РїСЂРё РїРѕР»СѓС‡РµРЅРёРё РїРѕСЃР»РµРґРЅРёС… Р·Р°РїСЂРѕСЃРѕРІ: {e}")
        return []


def get_total_searches_count() -> int:
    """Р’РѕР·РІСЂР°С‰Р°РµС‚ РѕР±С‰РµРµ РєРѕР»РёС‡РµСЃС‚РІРѕ РїРѕРёСЃРєРѕРІС‹С… Р·Р°РїСЂРѕСЃРѕРІ РёР· Р»РѕРіРѕРІ MongoDB."""
    """
    Get total number of searches in the collection.

    Returns:
        int: Total count of search documents
    """
    try:
        client = get_mongo_read_connection()
        # РЇРІРЅРѕРµ СѓРєР°Р·Р°РЅРёРµ Р±Р°Р·С‹ РґР°РЅРЅС‹С… Рё РєРѕР»Р»РµРєС†РёРё
        db = client["ich_edit"]
        collection = db["final_project_010825_daryna_abalmasova"]

        count = collection.count_documents({})
        client.close()

        return count
    except PyMongoError as e:
        print(f"вќЊ РћС€РёР±РєР° РїСЂРё РїРѕРґСЃС‡С‘С‚Рµ Р·Р°РїСЂРѕСЃРѕРІ: {e}")
        return 0
