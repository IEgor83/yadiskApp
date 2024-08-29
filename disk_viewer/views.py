from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
import requests
from typing import List, Dict, Any

def get_files_list(public_key: str) -> List[Dict[str, Any]]:
    """
    Получает список файлов и папок с Яндекс.Диска по публичному ключу.
    :param public_key: Публичный ключ Яндекс.Диска.
    :return: Список файлов и папок.
    """
    url = f"https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('_embedded', {}).get('items', [])
    return []


def categorize_files(files: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Категоризирует файлы по их MIME-типам.
    :param files: Список файлов и папок.
    :return: Словарь, где ключ — MIME-тип, а значение — список файлов этого типа.
    """
    categorized_files = {}
    for file in files:
        obj_type = file.get('type', 'unknown')
        mime_type = file.get('mime_type', 'unknown') if obj_type == "file" else "dir"
        if mime_type not in categorized_files:
            categorized_files[mime_type] = []
        categorized_files[mime_type].append(file)
    return categorized_files


def index(request):
    """
    Обрабатывает ввод публичного ключа и отображает список файлов и папок.
    """
    public_key = request.POST.get('public_key', '')
    files = get_files_list(public_key) if public_key else []
    categorized_files = categorize_files(files)
    return render(request, 'index.html', {
        'files': files,
        'categorized_files': categorized_files,
        'public_key': public_key
    })
