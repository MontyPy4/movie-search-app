#!/usr/bin/env python3
"""
Quick start script for Movie Search Application.
Проверяет все зависимости и готовит приложение к запуску.
"""

import sys
import os
import subprocess
from pathlib import Path


class Colors:
    """ANSI color codes for console output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print colored header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print_header("🐍 Проверка версии Python")

    version = sys.version_info
    print_info(
        f"Текущая версия: Python {
            version.major}.{
            version.minor}.{
                version.micro}")

    if version.major >= 3 and version.minor >= 8:
        print_success("Версия Python совместима")
        return True
    else:
        print_error(
            f"Требуется Python 3.8 или выше (установлена {
                version.major}.{
                version.minor})")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    print_header("📦 Проверка зависимостей Python")

    required = {
        'pymysql': 'PyMySQL (MySQL connector)',
        'pymongo': 'PyMongo (MongoDB connector)',
        'dotenv': 'Python-dotenv (environment variables)',
        'tabulate': 'Tabulate (table formatting)',
    }

    missing = []

    for package, description in required.items():
        try:
            __import__(package)
            print_success(f"{description} установлен")
        except ImportError:
            print_error(f"{description} НЕ установлен")
            missing.append(package)

    if missing:
        print_warning(f"\nУстановите отсутствующие пакеты:")
        print(f"{Colors.YELLOW}pip install {' '.join(missing)}{Colors.END}")
        return False

    return True


def check_env_file():
    """Check if .env file exists."""
    print_header("🔐 Проверка конфигурации")

    env_file = Path('.env')
    env_example = Path('.env.example')

    if env_file.exists():
        print_success(".env файл найден")
        return True
    elif env_example.exists():
        print_warning(".env файл не найден")
        print_info("Создаю .env на основе .env.example...")

        try:
            with open(env_example, 'r', encoding='utf-8') as src:
                content = src.read()
            with open(env_file, 'w', encoding='utf-8') as dst:
                dst.write(content)
            print_success(".env создан")
            print_warning(
                "Отредактируйте .env и добавьте ваши учетные данные!")
            return False
        except Exception as e:
            print_error(f"Ошибка при создании .env: {e}")
            return False
    else:
        print_error(".env и .env.example файлы не найдены")
        return False


def check_database_connections():
    """Check database connections."""
    print_header("💾 Проверка подключений к БД")

    # Test MySQL
    try:
        from mysql_connector import get_mysql_connection
        conn = get_mysql_connection()
        conn.close()
        print_success("MySQL подключение успешно")
        mysql_ok = True
    except Exception as e:
        print_error(f"MySQL подключение не удалось: {str(e)[:80]}")
        mysql_ok = False

    # Test MongoDB (Read)
    try:
        from log_stats import get_mongo_read_connection
        conn = get_mongo_read_connection()
        conn.close()
        print_success("MongoDB (read) подключение успешно")
        mongo_read_ok = True
    except Exception as e:
        print_error(f"MongoDB (read) подключение не удалось: {str(e)[:80]}")
        mongo_read_ok = False

    # Test MongoDB (Write)
    try:
        from log_writer import get_mongo_connection
        conn = get_mongo_connection()
        conn.close()
        print_success("MongoDB (write) подключение успешно")
        mongo_write_ok = True
    except Exception as e:
        print_error(f"MongoDB (write) подключение не удалось: {str(e)[:80]}")
        mongo_write_ok = False

    return mysql_ok and mongo_read_ok and mongo_write_ok


def run_smoke_tests():
    """Run basic smoke tests."""
    print_header("🧪 Запуск smoke тестов")

    try:
        # Test imports
        print_info("Проверка импортов...")
        from mysql_connector import search_by_keyword
        from log_writer import log_keyword_search
        from log_stats import get_popular_searches
        from formatter import print_header as fmt_header
        from main import search_keyword_menu
        print_success("Все импорты успешны")

        # Test configuration
        print_info("Проверка конфигурации...")
        from config import RESULTS_PER_PAGE, STATS_LIMIT
        print_success(
            f"Конфигурация загружена (результатов на странице: {RESULTS_PER_PAGE})")

        return True
    except Exception as e:
        print_error(f"Smoke тесты не пройдены: {e}")
        return False


def show_next_steps():
    """Show next steps for user."""
    print_header("🚀 Следующие шаги")

    print("1. Если видите ошибки выше - исправьте их перед запуском")
    print("2. Убедитесь что .env содержит правильные учетные данные")
    print("3. Запустите приложение:")
    print(f"\n   {Colors.BOLD}python main.py{Colors.END}\n")
    print("Документация:")
    print(f"   - {Colors.BOLD}README.md{Colors.END} - описание проекта")
    print(
        f"   - {Colors.BOLD}INSTALL.md{Colors.END} - подробная инструкция установки")
    print(f"   - {Colors.BOLD}GIT_GUIDE.md{Colors.END} - инструкции для GitHub")
    print(f"   - {Colors.BOLD}PRESENTATION.md{Colors.END} - презентация проекта")
    print(f"   - {Colors.BOLD}examples.py{Colors.END} - примеры использования")


def main():
    """Main quick start routine."""
    print_header("🎬 Movie Search Application - Quick Start")

    checks = [
        ("Python версия", check_python_version),
        ("Зависимости", check_dependencies),
        (".env конфигурация", check_env_file),
    ]

    all_passed = True
    for name, check_func in checks:
        if not check_func():
            all_passed = False

    if all_passed:
        print_info("Базовые проверки пройдены. Проверяю подключения к БД...")
        if not check_database_connections():
            print_warning(
                "Некоторые подключения не удались. Проверьте конфигурацию.")

    if all_passed:
        if run_smoke_tests():
            print_header("✅ Все проверки пройдены!")
        else:
            print_warning("Smoke тесты выявили проблемы")
    else:
        print_header("⚠️ Необходимо исправить проблемы выше")

    show_next_steps()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nОтмена пользователем. До свидания! 👋")
        sys.exit(0)
    except Exception as e:
        print_error(f"Неожиданная ошибка: {e}")
        sys.exit(1)
