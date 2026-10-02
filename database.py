#!/usr/bin/env python3
"""
Функции работы с базой данных SQLite
"""

import sqlite3
import os

DB_NAME = 'passwords.db'

def init_database():
    """Инициализация базы данных и создание таблиц при необходимости"""
    conn = sqlite3.connect(DB_NAME)
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

def add_password(title, username, encrypted_password):
    """Добавление новой записи"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO passwords (title, username, password) 
            VALUES (?, ?, ?)
        ''', (title, username, encrypted_password))
        conn.commit()
    except sqlite3.IntegrityError:
        # Если запись с таким названием уже существует, обновляем её
        cursor.execute('''
            UPDATE passwords 
            SET username = ?, password = ?
            WHERE title = ?
        ''', (username, encrypted_password, title))
        conn.commit()
    finally:
        conn.close()

def get_password(title):
    """Получение зашифрованного пароля по названию"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT password FROM passwords WHERE title = ?
    ''', (title,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    return None

def list_passwords():
    """Получение списка всех записей"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT title, username FROM passwords ORDER BY title
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    return results

def delete_password(title):
    """Удаление записи по названию"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM passwords WHERE title = ?
    ''', (title,))
    
    conn.commit()
    conn.close()