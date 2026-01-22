#!/usr/bin/env python3
"""
Script to verify that search queries are logged to MongoDB
"""

import sys
import os

if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

from pymongo import MongoClient
from datetime import datetime

# MongoDB connection parameters
MONGODB_URL = 'mongodb://ich_editor:verystrongpassword@mongo.itcareerhub.de/?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich_edit'
DATABASE = 'ich_edit'
COLLECTION = 'final_project_010825_daryna_abalmasova'

print("=" * 80)
print("ПРОВЕРКА ЛОГИРОВАНИЯ ЗАПРОСОВ В MONGODB")
print("=" * 80)

try:
    # Подключиться к MongoDB
    print("\n1️⃣  Подключение к MongoDB...")
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    client.admin.command('ismaster')
    print("✅ Подключение успешно!")

    # Получить БД и коллекцию
    print(
        f"\n2️⃣  Получение доступа к БД '{DATABASE}' и коллекции '{COLLECTION}'...")
    db = client[DATABASE]
    collection = db[COLLECTION]
    print("✅ Доступ получен!")

    # Посчитать документы
    print("\n3️⃣  Подсчёт документов...")
    total_count = collection.count_documents({})
    print(f"✅ Всего документов в коллекции: {total_count}")

    # Показать последние 5 документов
    if total_count > 0:
        print("\n4️⃣  Последние 5 логов запросов:")
        print("-" * 80)

        # Получить последние 5 документов
        latest_docs = list(collection.find().sort("_id", -1).limit(5))

        for idx, doc in enumerate(latest_docs, 1):
            print(f"\n📄 Документ {idx}:")
            print(f"   ID: {doc.get('_id')}")
            print(f"   Тип запроса: {doc.get('search_type')}")
            print(f"   Параметры: {doc.get('params')}")
            print(f"   Результатов: {doc.get('results_count')}")
            print(f"   Время: {doc.get('timestamp')}")

        # Статистика по типам запросов
        print("\n5️⃣  Статистика по типам запросов:")
        print("-" * 80)

        pipeline = [
            {"$group": {"_id": "$search_type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]

        stats = list(collection.aggregate(pipeline))
        for stat in stats:
            search_type = stat['_id'] if stat['_id'] else 'NULL'
            count = stat['count']
            print(f"   • {search_type}: {count} запрос(ов)")

        # Примеры конкретных запросов
        print("\n6️⃣  Примеры запросов по типам:")
        print("-" * 80)

        # Поиск по ключевому слову
        keyword_docs = list(collection.find(
            {"search_type": "keyword"}).limit(2))
        if keyword_docs:
            print(
                f"\n   🔍 Поиски по ключевому слову ({
                    len(keyword_docs)} примеров):")
            for doc in keyword_docs:
                print(
                    f"      • {
                        doc.get(
                            'params',
                            {}).get('keyword')} → {
                        doc.get('results_count')} результатов")

        # Поиск по жанру и годам
        genre_docs = list(collection.find(
            {"search_type": "genre__years_range"}).limit(2))
        if genre_docs:
            print(
                f"\n   🎬 Поиски по жанру и годам ({
                    len(genre_docs)} примеров):")
            for doc in genre_docs:
                params = doc.get('params', {})
                genre = params.get('genre', 'N/A')
                years = params.get('years_range', 'N/A')
                print(
                    f"      • {genre} ({years}) → {
                        doc.get('results_count')} результатов")

    else:
        print("❌ В коллекции нет документов. Выполните поиск в приложении.")
        print("\nЧтобы добавить логи:")
        print("   1. Запустите приложение: python main.py")
        print("   2. Выполните поиск по ключевому слову или жанру")
        print("   3. Запрос будет залогирован в MongoDB")
        print("   4. Запустите этот скрипт снова")

    # Проверка структуры документа
    print("\n7️⃣  Структура документа (первый пример):")
    print("-" * 80)
    sample_doc = collection.find_one()
    if sample_doc:
        # Просто вывести в виде текста
        print(f"   _id: {sample_doc.get('_id')}")
        print(f"   timestamp: {sample_doc.get('timestamp')}")
        print(f"   search_type: {sample_doc.get('search_type')}")
        print(f"   params: {sample_doc.get('params')}")
        print(f"   results_count: {sample_doc.get('results_count')}")

    client.close()

    print("\n" + "=" * 80)
    print("✅ ПРОВЕРКА ЗАВЕРШЕНА УСПЕШНО!")
    print("=" * 80 + "\n")

except Exception as e:
    print(f"\n❌ ОШИБКА: {e}")
    print("\nПроверьте:")
    print("   1. Интернет соединение")
    print("   2. Верны ли credentials (логин/пароль)")
    print("   3. Доступен ли сервер mongo.itcareerhub.de")
    print("\nДля подключения используйте:")
    print(f"   URL: {MONGODB_URL}")
    print(f"   БД: {DATABASE}")
    print(f"   Коллекция: {COLLECTION}")
    sys.exit(1)
