from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from urllib.parse import unquote
from pydactyl import PterodactylClient
import logging

logger = logging.getLogger(__name__)

# Инициализируем API-клиент
api = PterodactylClient(settings.PTERO_PANEL_URL, settings.PTERO_API_KEY)

# Базовая директория
BASE_DIRECTORY = "bin/Content.Server/data/Maps/development"


def list_files_view(request):
    """Обрабатывает запрос на просмотр файлов в директории"""
    directory = request.GET.get("directory", BASE_DIRECTORY) or BASE_DIRECTORY
    print(f"DEBUG: directory перед API-запросом = {directory} ({type(directory)})")  # Отладка

    try:
        files_data = api.client.servers.files.list_files(settings.PTERO_SERVER_ID, directory)
        logger.info("Ответ API: %s", files_data)

        if not files_data.get("data"):
            return render(request, "ptero_api/index.html", {
                "files": [],
                "current_directory": directory,
                "parent_directory": get_parent_directory(directory),
                "error": "Файлы не найдены или произошла ошибка"
            })

        file_list = [
            {
                "name": f["attributes"]["name"],
                "size": f["attributes"]["size"],
                "modified_at": f["attributes"]["modified_at"],
                "is_file": f["attributes"]["is_file"],
                "path": f"{directory.rstrip('/')}/{f['attributes']['name']}",
            }
            for f in files_data["data"]
        ]

        return render(request, "ptero_api/index.html", {
            "files": file_list,
            "current_directory": directory,
            "parent_directory": get_parent_directory(directory),
        })

    except Exception as e:
        logger.error("Ошибка при получении списка файлов: %s", str(e))
        return render(request, "ptero_api/index.html", {
            "files": [],
            "current_directory": directory,
            "parent_directory": get_parent_directory(directory),
            "error": f"Ошибка: {str(e)}"
        })


def get_parent_directory(directory: str) -> str:
    """Определяет родительскую директорию (безопасно)"""
    if directory == BASE_DIRECTORY:
        return None
    parent_directory = "/".join(directory.rstrip("/").split("/")[:-1]) or BASE_DIRECTORY
    return parent_directory


def download_file(request, file_path):
    """Обрабатывает скачивание файла"""
    try:
        file_path = unquote(file_path)

        if not file_path.startswith(BASE_DIRECTORY):
            raise ValueError("Недопустимый путь к файлу")

        download_url = api.client.servers.files.download_file(settings.PTERO_SERVER_ID, file_path)
        logger.info("Ссылка на скачивание: %s", download_url)

        return HttpResponseRedirect(download_url)

    except Exception as e:
        logger.error("Ошибка скачивания файла: %s", str(e))
        return HttpResponseRedirect(reverse("file_list"))
