from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import json


LOGS_DIR = Path("telegram_weather_bot") / "logs"

# Часовой пояс Казахстана
KZ_TZ = ZoneInfo("Asia/Aqtobe")


def log_message(message):
    """
    Логирует объект message в отдельный JSON-файл.
    """
    # Создаём папку для логов, если её нет
    LOGS_DIR.mkdir(exist_ok=True)

    # Имя файла на текущий день: username - YYYY-MM-DD.json
    now_kz = datetime.fromtimestamp(message.date, KZ_TZ)  # Время по КЗ
    username = message.from_user.username or message.from_user.first_name
    filename = f"{username} - {now_kz.strftime('%Y-%m-%d.json')}"
    filepath = LOGS_DIR / filename

    # Telegram message → dict
    message_dict = message.json if hasattr(message, "json") else message.__dict__

    # Если файла нет — создаём с пустым списком
    if not filepath.exists():
        logs = []
    else:
        # Иначе читаем существующие логи
        try:
            logs = json.loads(filepath.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            logs = []
    
    # Добавляем новый лог
    logs.append({
        "timestamp": now_kz.isoformat(timespec="seconds"),  # Время по КЗ
        "message": message_dict
    })
    
    # Перезаписываем файл
    filepath.write_text(
        json.dumps(logs, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )
