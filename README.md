## The purpose of the project:
The code was written for educational purposes

# 📄Overview
## [@WeatherBot](https://t.me/WeatherHa1seZz_Bot)

The **WeatherBot** is a Python-based Telegram bot that provides weather forecasts and daily weather updates for a chosen city using the OpenWeather API.
All interactions are logged into JSON files.

**Libraries used:** pyTelegramBotAPI, requests, schedule, zoneinfo, pathlib, json

## 🔧️Functions
- Getting the weather forecast on request.
- Automatic distribution of the weather forecast **for a given city**.
- Logging of all user messages in JSON format (by day and by user).


## 📂Project Structure

```sh
TelegramWeatherBot/
│
├── bot/                         # Core logic of the Telegram bot
│   ├── __init__.py              # Marks the folder as a Python package
│   ├── main.py                  # Entry point — runs the Telegram bot
│   ├── bot_handlers.py          # Command and message handlers
│   ├── auto_weather.py          # Automatic weather notifications (e.g., scheduled)
│
├── utils/                       # Utility modules
│   ├── __init__.py              # Marks the folder as a Python package
│   ├── logger.py                # Bot activity logging
│   ├── json_utils.py            # JSON handling (read/write, parsing)
│   ├── weather.py               # Weather API integration (requests & data processing)
│
├── config/                      # Configuration and settings
│   ├── __init__.py              # Marks the folder as a Python package
│   └── config.py                # Bot token, API keys, parameters
│
├── requirements.txt             # Project dependencies (Python libraries)
├── README.md                    # Project documentation
├── LICENSE                      # Project license
└── .gitignore                   # Git ignore rules (venv, logs, etc.)
```

## ⚙️ Requirements

- Python 3.8 or higher
- Internet connection
- A valid OpenWeather API Key
- A valid Telegram Bot Token (from @BotFather)
- Installed project dependencies (see `requirements.txt`)



* * *

## 📃LICENSE
This project is licensed under the MIT License - see the [**LICENSE**](https://github.com/Ha1seZz/Alberta-Seniors-Housing-Directory-Parser/blob/main/LICENSE) file for details.

## ⚠️Problems
If you have any problems while running the bot, you can create a new issue on GitHub or write to Telegram [**@Ha1seZz**](https://t.me/Ha1seZz) with a detailed problem.