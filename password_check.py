"""
ДЗ №11: Часть 1: Создание декоратора для проверки сложности пароля и функции регистрации пользователей.

Библиотеки:
- typing
Из библиотеки typing импортируем: Callable, List для корректного отображения типов и работы кода
- mypy - библиотека для проверки типов

Для проверки пароля используется цикл for и функция any(), точнее not any(), в результате которой, если во время проверки хотя бы один элемент не соответсвует условию, выводится ошибка raise ValueError (по каждому случаю)
"""
from typing import *
import mypy
import csv

# Список специальных символов
spec_symbols: List[str] = ['!', '@', '#', '`', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '<', '>', '?', '/', '|', '.', ':', ';', '[', ']', '{', '}', '"']


def password_checker(func: Callable[[str], None]) -> Callable[[str], None]: # Функция декоратора
    """Декоратор для проверки сложности пароля."""
    def wrapper(password: str) -> None:  
        """Функция-обёртка для проверки пароля."""
        # Проверка на длину пароля
        if len(password) < 8:
            raise ValueError('Пароль должен содержать не менее 8 символов')
        # Проверка на наличие хотя бы одной цифры
        if not any(char.isdigit() for char in password):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        # Проверка на наличие хотя бы одной заглавной буквы
        if not any(char.isupper() for char in password):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        # Проверка на наличие хотя бы одной строчной буквы
        if not any(char.islower() for char in password):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        # Проверка на наличие хотя бы одного спец символа
        if not any(char in spec_symbols for char in password):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ')

        func(password)  # Вызов оригинальной функции, только если все проверки пройдены

    return wrapper


@password_checker
def register_user(password: str) -> None:  
    """Функция для регистрации пользователя."""
    print('Пароль успешно зарегистрирован')

# проверка, запрос пароля у пользователя
password: str = input('Введите пароль для первого задания: ')
register_user(password)





"""
Часть 2: В этом задании вы создадите два декоратора для проверки пользовательских данных перед их сохранением в CSV файл. Один декоратор будет проверять сложность пароля, а второй — корректность имени пользователя.

import csv: библиотека для работы с csv файлами , куда будут записываться данные пользователя в случае удачной регистрации
"""

def password_validator(length: int = 8, uppercase: int = 1, lowercase: int = 1, special_chars: int = 1) -> Callable:
    """
    Декоратор для валидации паролей.

    Args:
        length: Минимальная длина пароля.
        uppercase: Минимальное количество букв верхнего регистра.
        lowercase: Минимальное количество букв нижнего регистра.
        special_chars: Минимальное количество спецсимволов.

    Returns:
        Декорированная функция.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(password: str):
            if len(password) < length:
                raise ValueError(f"Пароль слишком короткий. Минимум {length} символов.")
            if sum(1 for c in password if c.isupper()) < uppercase:
                raise ValueError(f"Пароль должен содержать минимум {uppercase} заглавных букв.")
            if sum(1 for c in password if c.islower()) < lowercase:
                raise ValueError(f"Пароль должен содержать минимум {lowercase} строчных букв.")
            if sum(1 for c in password if c in spec_symbols) < special_chars:
                raise ValueError(f"Пароль должен содержать минимум {special_chars} специальных символов.")
            return func(password)
        return wrapper
    return decorator


def username_validator(func: Callable) -> Callable:
    """
    Декоратор для валидации имени пользователя.

    Args:
        func: Функция, которую нужно декорировать.

    Returns:
        Декорированная функция.
    """
    def wrapper(username: str):
        if " " in username:
            raise ValueError("Имя пользователя не должно содержать пробелы.")
        return func(username)
    return wrapper


@password_validator(length=8, uppercase=1, lowercase=1, special_chars=1)
@username_validator
def register_user(username: str, password: str):
    """
    Функция для регистрации нового пользователя.

    Args:
        username: Имя пользователя.
        password: Пароль пользователя.

    Raises:
        ValueError: Если пароль или юзернейм не соответствует заданным условиям.
    """
    with open("users.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([username, password])
        print(f"Пользователь {username} успешно зарегистрирован.")