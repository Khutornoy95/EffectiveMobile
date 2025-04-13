# Бартерная платформа

## Описание
Платформа для обмена вещами между пользователями с возможностью:
- Создания и управления объявлениями
- Обмена предложениями между пользователями
- Фильтрации и поиска объявлений
- Документированным API

## Технологический стек
- Python 3.10.12
- Django 5.2
- Django REST Framework 3.16
- SQLite
- drf-yasg

## Установка

### 1. Клонирование репозитория

```git clone https://github.com/Khutornoy95/EffectiveMobile.git```
### 2. Создание виртуального окружения

```python -m venv venv```
```source venv/bin/activate```  # Linux/MacOS
```venv\Scripts\activate```     # Windows
### 3. Установка зависимостей

```pip install -r requirements.txt```
### 4. Настройка окружения
 Создайте файл .env в корне проекта и добавьте следующие строки:

```SECRET_KEY=ваш секретный ключ```
```DEBUG=True```
### 5. Применение миграций

```python manage.py makemigrations```
```python manage.py migrate```
### 6. Создание суперпользователя

```python manage.py createsuperuser```
### 7. Запуск сервера

```python manage.py runserver```
Сервер будет доступен по адресу: http://localhost:8000

### 8. Запуск тестов

```python manage.py test ads.tests```
