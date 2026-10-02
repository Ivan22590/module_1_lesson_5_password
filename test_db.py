#!/usr/bin/env python3
"""
Тестирование работы с базой данных
"""

import sqlite3
import os

# Инициализируем базу данных
def init_database():
    """Инициализация базы данных и создание таблиц при необходимости"""
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    
    # Создание таблицы для хранения мастер-пароля и соли
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            master_hash TEXT NOT NULL,
            salt BLOB NOT NULL
        )
    ''')
    
    # Создание таблицы для хранения паролей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password BLOB NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Тестирование
if __name__ == "__main__":
    init_database()
    
    # Проверим содержимое таблицы settings
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM settings")
    result = cursor.fetchall()
    print("Содержимое таблицы settings:", result)
    
    cursor.execute("SELECT * FROM passwords")
    result = cursor.fetchall()
    print("Содержимое таблицы passwords:", result)
    
    conn.close()