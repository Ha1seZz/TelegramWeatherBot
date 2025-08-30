from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import json
import re


class Logger:
    def __init__(self, subfolder: str = None):
        if subfolder is None:
            subfolder = ""
        self.LOGS_DIR = Path(f"logs/{subfolder}")
        self.KZ_TZ = ZoneInfo("Asia/Aqtobe")  # Часовой пояс Казахстана
        # Создаём папку (и подпапки) для логов, если её нет
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    def _get_log_file(self, message) -> Path:
        """
        Готовит и возвращает Path
        """
        # Имя файла на текущий день: username - YYYY-MM-DD.json
        now_kz = datetime.fromtimestamp(message.date, self.KZ_TZ)  # Время по КЗ
        username = message.from_user.username or message.from_user.first_name
        safe_username = re.sub(r'[^a-zA-Z0-9а-яА-Я._-]', '_', username)
        filename = f"{safe_username} - {now_kz.strftime('%Y-%m-%d.json')}"
        filepath = self.LOGS_DIR / filename
        return filepath, now_kz

    def _serialize_message(self, message, timestamp: datetime) -> dict:
        """
        Готовит и возвращает dict для записи
        """
        message_dict = (
            message.json if hasattr(message, "json") else message.__dict__
        )
        return {
            "timestamp": timestamp.isoformat(timespec="seconds"),
            "message": message_dict
        }

    def log_message(self, message):
        """
        Логирует объект message в отдельный JSON-файл.
        """
        filepath, now_kz = self._get_log_file(message)

        try:
            logs = json.loads(filepath.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []

        logs.append(self._serialize_message(message, now_kz))

        filepath.write_text(
            json.dumps(logs, ensure_ascii=False, indent=4),
            encoding="utf-8"
        )
