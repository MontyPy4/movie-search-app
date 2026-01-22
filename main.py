"""Главный модуль: запуск приложения, меню, взаимодействие с пользователем."""

import sys
import os

# Установить кодировку для консоли
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

from typing import Optional
import msvcrt

from mysql_connector import (
    get_all_genres, get_year_range, search_by_keyword,
    search_by_genre_and_years
)
from log_writer import log_keyword_search, log_genre_years_search
from log_stats import (
    get_popular_searches, get_latest_searches, get_total_searches_count
)
from formatter import (
    print_header, print_subheader, print_movies_table, print_genres_list,
    print_year_range, print_popular_searches, print_latest_searches,
    print_statistics_summary
)

from config import RESULTS_PER_PAGE
from utils import log_function_call


@log_function_call
def search_keyword_menu():
    """
    Menu for keyword search with pagination support.
    """
    print_subheader("🔍 Поиск по ключевому слову")
    
    keyword = input("\nВведите ключевое слово для поиска: ").strip()
    
    if not keyword:
        print("❌ Пожалуйста, введите хотя бы одно слово.")
        return
    
    page = 1
    while True:
        movies, total_count = search_by_keyword(keyword, page)
        
        if page == 1:
            # Log only first page
            log_keyword_search(keyword, total_count)
        
        print_movies_table(movies, page, total_count)
        
        if total_count == 0:
            break
        
        max_pages = (total_count + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
        
        # Navigation instructions
        print("\n" + "─" * 60)
        print("Навигация:")
        if page < max_pages:
            print("  → (стрелка вправо)  - следующая страница")
        if page > 1:
            print("  ← (стрелка влево)   - предыдущая страница")
        print("  ↓ (стрелка вниз)    - вернуться в главное меню")
        print("─" * 60)
        print("\n⌨️  Нажмите стрелку на клавиатуре...")
        
        # Wait for arrow key
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                
                # Arrow keys send two bytes: 224 (0xe0) or 0 (0x00) followed by direction code
                if key in (b'\xe0', b'\x00'):  # Special key prefix
                    key = msvcrt.getch()
                    
                    if key == b'M':  # Right arrow (0x4D)
                        if page < max_pages:
                            page += 1
                            break
                        else:
                            print("\n❌ Это последняя страница.")
                    
                    elif key == b'K':  # Left arrow (0x4B)
                        if page > 1:
                            page -= 1
                            break
                        else:
                            print("\n❌ Это первая страница.")
                    
                    elif key == b'P':  # Down arrow (0x50)
                        print("\n↩️  Возврат в главное меню...")
                        return
                
                elif key == b'\r':  # Enter key - also exit
                    print("\n↩️  Возврат в главное меню...")
                    return


@log_function_call
def search_genre_years_menu():
    """
    Menu for genre and year range search with pagination support.
    """
    print_subheader("🎬 Поиск по жанру и диапазону лет")
    
    # Get and display genres
    genres = get_all_genres()
    if not genres:
        print("❌ Не удалось загрузить список жанров.")
        return
    
    print_genres_list(genres)
    
    # Get user's genre choice
    while True:
        genre_choice = input("\nВведите номер жанра или название: ").strip()
        
        try:
            genre_idx = int(genre_choice) - 1
            if 0 <= genre_idx < len(genres):
                selected_genre = genres[genre_idx]
                break
            else:
                print("❌ Пожалуйста, выберите корректный номер.")
        except ValueError:
            # Assume user entered genre name
            if genre_choice in genres:
                selected_genre = genre_choice
                break
            else:
                print("❌ Жанр не найден. Пожалуйста, выберите из списка.")
    
    # Get year range
    min_year, max_year = get_year_range()
    print_year_range(min_year, max_year)
    
    while True:
        try:
            start_year = int(input(f"\nВведите начальный год ({min_year}-{max_year}): ").strip())
            end_year = int(input(f"Введите конечный год ({min_year}-{max_year}): ").strip())
            
            if not (min_year <= start_year <= max_year and min_year <= end_year <= max_year):
                print("❌ Годы должны быть в рамках доступного диапазона.")
                continue
            
            if start_year > end_year:
                print("❌ Начальный год должен быть меньше или равен конечному.")
                continue
            
            break
        except ValueError:
            print("❌ Пожалуйста, введите корректные числовые значения.")
    
    # Search with pagination
    page = 1
    while True:
        movies, total_count = search_by_genre_and_years(
            selected_genre, start_year, end_year, page
        )
        
        if page == 1:
            # Log only first page
            years_range = f"{start_year}-{end_year}"
            log_genre_years_search(selected_genre, years_range, total_count)
        
        print_movies_table(movies, page, total_count)
        
        if total_count == 0:
            break
        
        max_pages = (total_count + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
        
        # Navigation instructions
        print("\n" + "─" * 60)
        print("Навигация:")
        if page < max_pages:
            print("  → (стрелка вправо)  - следующая страница")
        if page > 1:
            print("  ← (стрелка влево)   - предыдущая страница")
        print("  ↓ (стрелка вниз)    - вернуться в главное меню")
        print("─" * 60)
        print("\n⌨️  Нажмите стрелку на клавиатуре...")
        
        # Wait for arrow key
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                
                # Arrow keys send two bytes: 224 (0xe0) or 0 (0x00) followed by direction code
                if key in (b'\xe0', b'\x00'):  # Special key prefix
                    key = msvcrt.getch()
                    
                    if key == b'M':  # Right arrow (0x4D)
                        if page < max_pages:
                            page += 1
                            break
                        else:
                            print("\n❌ Это последняя страница.")
                    
                    elif key == b'K':  # Left arrow (0x4B)
                        if page > 1:
                            page -= 1
                            break
                        else:
                            print("\n❌ Это первая страница.")
                    
                    elif key == b'P':  # Down arrow (0x50)
                        print("\n↩️  Возврат в главное меню...")
                        return
                
                elif key == b'\r':  # Enter key - also exit
                    print("\n↩️  Возврат в главное меню...")
                    return


@log_function_call
def view_statistics_menu():
    """
    Menu for viewing search statistics.
    """
    print_subheader("📊 Просмотр статистики")
    
    print("\n1. 5 самых популярных запросов (по частоте)")
    print("2. 5 последних уникальных запросов")
    print("3. Назад в главное меню")
    
    while True:
        choice = input("\nВыберите опцию (1-3): ").strip()
        
        if choice == '1':
            searches = get_popular_searches()
            print_popular_searches(searches)
            break
        elif choice == '2':
            searches = get_latest_searches()
            print_latest_searches(searches)
            break
        elif choice == '3':
            break
        else:
            print("❌ Пожалуйста, выберите корректный номер опции.")
    
    # Show statistics summary
    total_searches = get_total_searches_count()
    print_statistics_summary(total_searches)


@log_function_call
def display_main_menu():
    """
    Display main menu and handle user choice.
    
    Returns:
        bool: False if user wants to exit, True otherwise
    """
    print_header("🎥 ПРИЛОЖЕНИЕ ДЛЯ ПОИСКА ФИЛЬМОВ")
    
    print("\n1. Поиск по ключевому слову")
    print("2. Поиск по жанру и диапазону лет")
    print("3. Просмотр статистики запросов")
    print("4. Выход")
    
    while True:
        choice = input("\nВыберите опцию (1-4): ").strip()
        
        if choice == '1':
            try:
                search_keyword_menu()
            except Exception as e:
                print(f"❌ Ошибка при поиске: {e}")
            return True
        
        elif choice == '2':
            try:
                search_genre_years_menu()
            except Exception as e:
                print(f"❌ Ошибка при поиске: {e}")
            return True
        
        elif choice == '3':
            try:
                view_statistics_menu()
            except Exception as e:
                print(f"❌ Ошибка при получении статистики: {e}")
            return True
        
        elif choice == '4':
            return False
        
        else:
            print("❌ Пожалуйста, выберите корректный номер опции (1-4).")


@log_function_call
def main():
    """
    Main application loop.
    """
    try:
        while True:
            if not display_main_menu():
                print("\n✓ Спасибо за использование приложения! До свидания! 👋")
                break
    except KeyboardInterrupt:
        print("\n\n✓ Приложение прервано пользователем. До свидания! 👋")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
