from typing import Any, Union
from pathlib import Path
import json


class JsonUtils:
    def __init__(self, filename: str):
        self.filename = filename

    def read_json(self) -> Union[dict, list, None]:
        """Читает JSON-файл, возвращает данные или None, если файл пустой/не найден."""
        file_path = Path(self.filename)

        # Проверяем, существует ли файл
        if not file_path.exists():
            return None

        try:
            # Читаем содержимое файла в кодировке UTF-8
            with file_path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # Возвращаем None, если файл пустой или повреждён
            return None

    def write_json(self, data) -> None:
        """Записывает данные в JSON-файл, создавая папки при необходимости."""
        file_path = Path(self.filename)

        # Создаём родительские папки, если их нет
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Записываем данные в UTF-8 с отступами и без ASCII-экранирования
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
