#!/usr/bin/env python3
"""
Функции шифрования паролей с использованием Fernet
"""

import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

KEY_FILE = '.key'

def generate_key_file():
    """Генерирует и сохраняет ключ шифрования в файл"""
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    """Загружает ключ шифрования из файла"""
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("Файл ключа не найден. Запустите программу для создания ключа.")
    
    with open(KEY_FILE, 'rb') as key_file:
        key = key_file.read()
    return key

def encrypt_password(password, fernet):
    """Шифрует пароль"""
    return fernet.encrypt(password.encode())

def decrypt_password(encrypted_password, fernet):
    """Расшифровывает пароль"""
    return fernet.decrypt(encrypted_password).decode()