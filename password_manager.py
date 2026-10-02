#!/usr/bin/env python3
"""
CLI-приложение для хранения паролей с шифрованием
"""

import sys
import os
import hashlib
import sqlite3
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import string
import secrets

# Импортируем модули
from database import init_database, add_password, get_password, list_passwords, delete_password
from encryption import encrypt_password, decrypt_password, generate_key_file, load_key

def get_master_password():
    """Запрашивает мастер-пароль у пользователя"""
    return getpass.getpass("Введите мастер-пароль: ")

def verify_master_password(password):
    """Проверяет мастер-пароль"""
    # Получаем хэш из базы данных
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT master_hash, salt FROM settings LIMIT 1")
    result = cursor.fetchone()
    
    if result is None:
        # Первый запуск - сохраняем хэш
        salt = os.urandom(16)
        master_hash = hashlib.sha256(password.encode() + salt).hexdigest()
        cursor.execute("INSERT INTO settings (master_hash, salt) VALUES (?, ?)", 
                      (master_hash, salt))
        conn.commit()
        conn.close()
        return True
    
    stored_hash, stored_salt = result
    # Проверяем введенный пароль
    password_hash = hashlib.sha256(password.encode() + stored_salt).hexdigest()
    
    conn.close()
    return password_hash == stored_hash

def generate_password(length=16):
    """Генерирует случайный пароль"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def display_menu():
    """Отображает меню команд"""
    print("\n=== МЕНЮ ===")
    print("1. Добавить запись")
    print("2. Получить пароль")
    print("3. Показать список записей")
    print("4. Удалить запись")
    print("5. Создать новый пароль")
    print("6. Выход")
    print("=" * 20)

def get_user_choice():
    """Получает выбор пользователя"""
    while True:
        try:
            choice = int(input("Выберите действие (1-6): "))
            if 1 <= choice <= 6:
                return choice
            else:
                print("Пожалуйста, выберите число от 1 до 6")
        except ValueError:
            print("Пожалуйста, введите число")

def add_record(fernet):
    """Добавление новой записи"""
    try:
        title = input("Название/откуда: ").strip()
        if not title:
            print("Название не может быть пустым")
            return
            
        username = input("Логин: ").strip()
        if not username:
            print("Логин не может быть пустым")
            return
            
        password = input("Пароль: ").strip()
        if not password:
            print("Пароль не может быть пустым")
            return
        
        encrypted_password = encrypt_password(password, fernet)
        add_password(title, username, encrypted_password)
        print(f"Запись '{title}' успешно добавлена!")
        
    except Exception as e:
        print(f"Ошибка при добавлении записи: {e}")

def get_password_record(fernet):
    """Получение пароля по названию"""
    try:
        title = input("Название записи: ").strip()
        if not title:
            print("Название не может быть пустым")
            return
            
        encrypted_password = get_password(title)
        if encrypted_password:
            password = decrypt_password(encrypted_password, fernet)
            print(f"Пароль для '{title}': {password}")
        else:
            print(f"Запись '{title}' не найдена")
    except Exception as e:
        print(f"Ошибка при получении пароля: {e}")

def list_records():
    """Показать список всех записей"""
    passwords = list_passwords()
    if passwords:
        print("\nСохраненные записи:")
        for i, (title, username) in enumerate(passwords, 1):
            print(f"  {i}. {title} ({username})")
    else:
        print("Нет сохраненных записей")

def delete_record():
    """Удаление записи по названию"""
    try:
        title = input("Название записи для удаления: ").strip()
        if not title:
            print("Название не может быть пустым")
            return
            
        delete_password(title)
        print(f"Запись '{title}' удалена")
    except Exception as e:
        print(f"Ошибка при удалении записи: {e}")

def main():
    """Основная функция CLI"""
    # Инициализируем базу данных
    init_database()
    
    # Загружаем ключ шифрования
    try:
        key = load_key()
        fernet = Fernet(key)
    except FileNotFoundError:
        # Если ключа нет, создаем его
        key = generate_key_file()
        fernet = Fernet(key)
    
    # Проверяем мастер-пароль
    master_password = get_master_password()
    if not verify_master_password(master_password):
        print("Неверный мастер-пароль!")
        sys.exit(1)
    
    print("Добро пожаловать в менеджер паролей!")
    
    # Основной цикл программы
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == 1:
            add_record(fernet)
        elif choice == 2:
            get_password_record(fernet)
        elif choice == 3:
            list_records()
        elif choice == 4:
            delete_record()
        elif choice == 5:
            password = generate_password()
            print(f"Сгенерированный пароль: {password}")
        elif choice == 6:
            print("До свидания!")
            break

if __name__ == "__main__":
    main()