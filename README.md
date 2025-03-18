# Простенький сайт реализованный на фреймворке Django

## Описание
Этот проект позволяет просматривать файлы на сервере Pterodactyl и скачивать их через Django с помощью библиотеки Pydactyl

## Установка и запуск
### 1. Клонирование репозитория
```bash
git clone https://github.com/newyearoldme/PterodactylSite
cd mysite
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
В файл `.env` нужно добавить
```py
PTERO_API_KEY=your_api_key
PTERO_PANEL_URL=your_url
PTERO_SERVER_ID=your_server_id
SECRET_KEY=your_django_secret_key
```
### 4. Непосредственно сам запуск
Находясь в папке `mysite`, необходимо ввести:
```py
python manage.py runserver
```
И перейти по адрессу `http://127.0.0.1:8000/`

Не судите строго люди добрые :pray: 
