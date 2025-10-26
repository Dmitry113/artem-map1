# Artem Map

**Artem Map** — интерактивная карта интересных мест с возможностью добавления и редактирования локаций через админку.
Проект создан на **Django 5**, с использованием **Leaflet** для карты и **CKEditor** для WYSIWYG редактирования описаний.

---

## Основные возможности

- Добавление и редактирование мест (парки, музеи, кафе и др.)
- Краткое и полное описание с HTML-разметкой (редактирование через WYSIWYG)
- Загрузка и сортировка фотографий для каждой локации
- Сортируемый список фотографий через админку
- Категории мест с фильтрацией
- Админка с удобным интерфейсом и превью изображений
- Настройки через переменные окружения (готово к развёртыванию)
- Поддержка локализации (русский язык)

---

## Технологии

- Python 3.12
- Django 5.0.6
- SQLite (по умолчанию) / поддержка других баз через переменные окружения
- CKEditor 5 (WYSIWYG)
- Leaflet.js (карта)
- Django Admin, Django ORM
- Git и GitHub для контроля версий

---

## Установка и запуск

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/<ваш_логин>/artem-map.git
cd artem-map

2. Создайте и активируйте виртуальное окружение:

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / Mac
source .venv/bin/activate

3. Установите зависимости:

pip install -r requirements.txt

4. Создайте файл .env в корне проекта:

SECRET_KEY=ваш_секретный_ключ
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

5. Примените миграции:

python manage.py makemigrations
python manage.py migrate

6. Создайте суперпользователя для админки:

python manage.py createsuperuser

7. Запустите сервер разработки:

python manage.py runserver

8. Откройте браузер:

Карта и фронтенд: http://127.0.0.1:8000/

Админка: http://127.0.0.1:8000/admin/

9. Структура проекта

artem_map/
├── artem_map_project/       # Основной проект Django
├── places/                  # Приложение для мест и фотографий
├── main/                    # Статика, шаблоны
├── media/                   # Загруженные изображения
├── .venv/                   # Виртуальное окружение
├── db.sqlite3               # База данных (по умолчанию)
├── manage.py
└── requirements.txt

10. Особенности

Сортировка фотографий: через drag-and-drop в админке (adminsortable2)

WYSIWYG редактор: CKEditor 5 для полного описания локации

Безопасность: ключи и настройки вынесены в переменные окружения

Мультиязычность: интерфейс на русском языке

Контакты

Автор: Дмитрий Крупин
Email: krdv13@yandex.ru
