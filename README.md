# STALZONE Emission Monitor Bot

[English](#english) | [Русский](#русский)

> **About the game name:** the game was previously called STALCRAFT: X and was renamed
> to **STALZONE** in June 2026. The emission API still lives on the old domain
> (`eapi.stalcraft.net`), and the Steam AppID is unchanged, so technical references
> to "StalCraft" remain valid.

---

## English

A Telegram bot that monitors emission events in STALZONE and notifies a Telegram
channel when one starts.

### Features

- 🔔 **Emission Detection** - Polls the emission API every 25 seconds
- 📢 **Channel Notifications** - Posts alerts to [@InformSCX](https://t.me/InformSCX)
- 🎮 **Player Count** - Includes the current online count from the Steam API
- 🕐 **Timezone Conversion** - Converts UTC timestamps to Moscow time (MSK)
- 📸 **Visual Notifications** - Sends notifications with an emission-themed image
- 🧹 **Message Cleanup** - Removes previous "emission ended" messages
- 🔄 **Continuous Monitoring** - Separate threads for bot commands and emission checks

### Requirements

- Python 3.12+ (the code uses f-strings with nested quotes, PEP 701)
- Telegram bot token
- Emission API credentials (Client ID and Client Secret)
- Reachable `api.telegram.org` (see [Troubleshooting](#troubleshooting))

Dependencies are listed in `requirements.txt`: `pyTelegramBotAPI`, `requests`,
`python-dotenv`.

### Installation

```bash
git clone https://github.com/fasolgfgg-jpg/StalZoneEmBot.git
cd StalZoneEmBot
pip install -r requirements.txt
cp .env.example .env
```

Then fill in `.env` with your credentials.

### Configuration

All secrets are read from environment variables (see `Config.py`). Locally they are
loaded from the `.env` file in the project root; in production they can be supplied
as real environment variables (Docker, systemd, CI). Real environment variables take
priority over values from `.env`.

**Required**

| Variable | Description |
| --- | --- |
| `TG_CLIENT_TOKEN` | Telegram Bot API token (obtain from [@BotFather](https://t.me/BotFather)) |
| `CLIENT_SECRET` | Emission API Client Secret |
| `CLIENT_ID` | Emission API Client ID |

**Optional**

| Variable | Default | Description |
| --- | --- | --- |
| `STEAM_API_KEY` | _empty_ | Steam Web API key for player count requests |

If a required variable is missing, the bot exits on startup with a message listing
what needs to be set.

To obtain API credentials, register an application on
[eapi.stalcraft.net](https://eapi.stalcraft.net/) and add the issued Client ID and
Client Secret to `.env`.

### Usage

```bash
python Main.py
```

The bot starts polling for Telegram commands and begins monitoring the emission API
in a background thread.

**Commands:** `/start`, `/help`

### How It Works

1. The `check()` function runs in a separate thread and polls the emission API every
   25 seconds.
2. While no emission is scheduled, the response contains only `previousStart` and
   `previousEnd`. When an emission is scheduled, a `currentStart` field appears with
   the start time.
3. Once the current UTC time is within ±30 seconds of `currentStart`, the bot sends
   a notification: photo, start and end time in MSK, and the current player count.
4. Four minutes later it posts "emission ended" and deletes the previous ended
   message to keep the channel tidy.

### Project Structure

```
StalZoneEmBot/
├── Main.py              # Entry point: bot commands and emission checker
├── Tools.py             # API requests and access to credentials
├── Config.py            # Environment variable loading and validation
├── Debug.py             # Logging utilities
├── GetOnline.py         # Steam player count fetcher
├── requirements.txt     # Dependencies
├── .env                 # Secrets and settings (not committed)
├── .env.example         # Environment variable template
├── .gitignore           # Git ignore rules
├── photo.png            # Emission notification image
├── photo1.png           # Alternative notification image
├── MessageID.ids        # Message IDs for cleanup
└── name.nlf             # Current log file name
```

### Logging

Logs are written to the `Logs/` directory via the `Debug` module: emission checks,
API responses, message sending, and errors.

### Troubleshooting

| Symptom | Cause |
| --- | --- |
| `ConnectTimeout: api.telegram.org` on startup | Telegram is unreachable from your network. Route traffic through a proxy, e.g. `export HTTPS_PROXY=socks5://127.0.0.1:1080`, or set `telebot.apihelper.proxy` in code. |
| `Ошибка при попытке выполнить запрос 'currentStart'` repeating | Normal idle state: no emission is scheduled, so the response has no `currentStart` field. |
| Bot exits with `Отсутствуют обязательные переменные окружения` | Some required variables are missing or blank in `.env`. |

### Notes

- The bot must run continuously to catch emissions.
- The Telegram bot needs permission to post to the target channel.
- Emission API endpoint: `https://eapi.stalcraft.net/RU/emission`
- Player count source: Steam API, AppID `1818450`

Official channel: [@InformSCX](https://t.me/InformSCX)

---

## Русский

Телеграм-бот, который следит за выбросами в STALZONE и уведомляет канал, когда
выброс начинается.

### Возможности

- 🔔 **Детект выброса** — опрос API каждые 25 секунд
- 📢 **Уведомления в канал** — публикация в [@InformSCX](https://t.me/InformSCX)
- 🎮 **Онлайн игроков** — количество игроков из Steam API
- 🕐 **Конвертация времени** — перевод UTC в московское время (MSK)
- 📸 **Оформление** — отправка уведомления с картинкой выброса
- 🧹 **Очистка** — удаление предыдущих сообщений «выброс закончился»
- 🔄 **Круглосуточная работа** — команды и проверка выброса в отдельных потоках

### Требования

- Python 3.12+ (в коде используются f-строки с вложенными кавычками, PEP 701)
- Токен телеграм-бота
- Ключи API выбросов (Client ID и Client Secret)
- Доступность `api.telegram.org` (см. [Возможные проблемы](#возможные-проблемы))

Зависимости перечислены в `requirements.txt`: `pyTelegramBotAPI`, `requests`,
`python-dotenv`.

### Установка

```bash
git clone https://github.com/fasolgfgg-jpg/StalZoneEmBot.git
cd StalZoneEmBot
pip install -r requirements.txt
cp .env.example .env
```

После этого заполните `.env` своими ключами.

### Настройка

Все секреты читаются из переменных окружения (см. `Config.py`). Локально значения
берутся из файла `.env` в корне проекта, в продакшене их можно передать как обычные
переменные окружения (Docker, systemd, CI). Реальные переменные окружения важнее
значений из `.env`.

**Обязательные**

| Переменная | Описание |
| --- | --- |
| `TG_CLIENT_TOKEN` | Токен телеграм-бота (выдаёт [@BotFather](https://t.me/BotFather)) |
| `CLIENT_SECRET` | Client Secret API выбросов |
| `CLIENT_ID` | Client ID API выбросов |

**Необязательные**

| Переменная | По умолчанию | Описание |
| --- | --- | --- |
| `STEAM_API_KEY` | _пусто_ | Ключ Steam Web API для запроса онлайна |

Если обязательная переменная не задана, бот завершается при старте и выводит
список того, чего не хватает.

Чтобы получить ключи API, зарегистрируйте приложение на
[eapi.stalcraft.net](https://eapi.stalcraft.net/) и внесите выданные Client ID и
Client Secret в `.env`.

### Запуск

```bash
python Main.py
```

Бот начинает опрашивать команды Telegram и в отдельном потоке запускает проверку
выбросов.

**Команды:** `/start`, `/help`

### Как это работает

1. Функция `check()` работает в отдельном потоке и опрашивает API выбросов каждые
   25 секунд.
2. Пока выброс не назначен, в ответе есть только `previousStart` и `previousEnd`.
   Когда выброс назначен, в ответе появляется поле `currentStart` со временем начала.
3. Как только текущее время UTC попадает в окно ±30 секунд от `currentStart`, бот
   отправляет уведомление: картинку, время начала и конца по Москве и текущий онлайн.
4. Через четыре минуты публикуется сообщение «выброс закончился», а предыдущее
   такое сообщение удаляется, чтобы не засорять канал.

### Структура проекта

```
StalZoneEmBot/
├── Main.py              # Точка входа: команды бота и проверка выбросов
├── Tools.py             # Запросы к API и доступ к ключам
├── Config.py            # Загрузка и проверка переменных окружения
├── Debug.py             # Логирование
├── GetOnline.py         # Онлайн игроков через Steam
├── requirements.txt     # Зависимости
├── .env                 # Секреты и настройки (не в git)
├── .env.example         # Шаблон переменных окружения
├── .gitignore           # Правила игнорирования
├── photo.png            # Картинка для уведомления о выбросе
├── photo1.png           # Запасная картинка
├── MessageID.ids        # ID сообщений для очистки
└── name.nlf             # Имя текущего файла лога
```

### Логи

Логи пишутся в каталог `Logs/` через модуль `Debug`: проверки выбросов, ответы API,
отправка сообщений и ошибки.

### Возможные проблемы

| Симптом | Причина |
| --- | --- |
| При старте `ConnectTimeout: api.telegram.org` | Telegram недоступен из вашей сети. Нужен прокси, например `export HTTPS_PROXY=socks5://127.0.0.1:1080`, либо `telebot.apihelper.proxy` в коде. |
| Постоянно повторяется `Ошибка при попытке выполнить запрос 'currentStart'` | Нормальное состояние покоя: выброс не назначен, поэтому поля `currentStart` в ответе нет. |
| Бот завершается с `Отсутствуют обязательные переменные окружения` | В `.env` не хватает каких-то обязательных переменных или они пустые. |

### Примечания

- Чтобы не пропустить выброс, бот должен работать непрерывно.
- У бота должны быть права на публикацию в целевом канале.
- Endpoint API выбросов: `https://eapi.stalcraft.net/RU/emission`
- Источник онлайна: Steam API, AppID `1818450`

Официальный канал: [@InformSCX](https://t.me/InformSCX)
