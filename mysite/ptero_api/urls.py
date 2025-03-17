from django.urls import path
from .views import list_files_view, download_file

urlpatterns = [
    path("", list_files_view, name="list_files_view"),
    path("download/<path:file_path>/", download_file, name="download_file"),
]
