#!/usr/bin/env python3
"""
Вспомогательные функции
"""

import string
import secrets

def generate_password(length=16):
    """Генерирует случайный пароль"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))