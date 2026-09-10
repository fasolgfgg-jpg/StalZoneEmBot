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
- 📢 **Channel Notifications** - Posts alerts to [@SZInform](https://t.me/SZInform)
- 🎮 **Player Count** - Includes the current online count from the Steam API
- 🕐 **Timezone Conversion** - Converts UTC timestamps to Moscow time (MSK)
- 📸 **Visual Notifications** - Sends notifications with an emission-themed image
- 🧹 **Message Cleanup** - Removes previous "emission ended" messages
- 🔄 **Continuous Monitoring** - Separate threads for bot commands and emission checks

### Requirements

- Python 3.11+ (the Docker image is based on `python:3.11-slim`)
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

### Running with Docker

```bash
cp .env.example .env        # fill in your credentials
docker compose up -d --build
docker compose logs -f      # follow the logs
docker compose down
```

The image does not contain `.env`: it is excluded by `.dockerignore` and passed to
the container through `env_file`. Logs and `MessageID.ids` live in `./data`, which
is mounted into the container, so they survive a rebuild.

Running the image without Compose works too, but the variables must be passed
explicitly:

```bash
docker build -t stalzone-bot .
docker run -d --name stalzone_bot --env-file .env \
  -v "$PWD/data:/app/data" -v "$PWD/photos:/app/photos" stalzone-bot
```

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
├── Dockerfile           # Container image (python:3.11-slim)
├── docker-compose.yml   # Compose service: volumes and env
├── .dockerignore        # Files excluded from the image (including .env)
├── .env                 # Secrets and settings (not in git, not in the image)
├── .env.example         # Environment variable template
├── .gitignore           # Git ignore rules
├── photos/              # Emission notification image
└── data/                # Runtime data: logs and MessageID.ids (mounted)
```

### Logging

Logs are written to the `data/logs/` directory via the `Debug` module: emission
checks, API responses, message sending, and errors. The directory is mounted from
the host, so logs persist between container restarts.

### Troubleshooting

| Symptom | Cause |
| --- | --- |
| `ConnectTimeout: api.telegram.org` on startup | Telegram is unreachable from your network. Route traffic through a proxy, e.g. `export HTTPS_PROXY=socks5://127.0.0.1:1080`, or set `telebot.apihelper.proxy` in code. |
| Only `Выброс не ожидается` repeating, nothing else | Normal idle state: no emission is scheduled, so the response has no `currentStart` field. The resulting `KeyError` is suppressed; only genuine request failures are logged as errors. |
| Bot exits with `Отсутствуют обязательные переменные окружения` | Some required variables are missing or blank in `.env`. |

### Notes

- The bot must run continuously to catch emissions.
- The Telegram bot needs permission to post to the target channel.
- Emission API endpoint: `https://eapi.stalcraft.net/RU/emission`
- Player count source: Steam API, AppID `1818450`

Official channel: [@SZInform](https://t.me/SZInform)

---

## Русский

Телеграм-бот, который следит за выбросами в STALZONE и уведомляет канал, когда
выброс начинается.

### Возможности

- 🔔 **Детект выброса** — опрос API каждые 25 секунд
- 📢 **Уведомления в канал** — публикация в [@SZInform](https://t.me/SZInform)
- 🎮 **Онлайн игроков** — количество игроков из Steam API
- 🕐 **Конвертация времени** — перевод UTC в московское время (MSK)
- 📸 **Оформление** — отправка уведомления с картинкой выброса
- 🧹 **Очистка** — удаление предыдущих сообщений «выброс закончился»
- 🔄 **Круглосуточная работа** — команды и проверка выброса в отдельных потоках

### Требования

- Python 3.11+ (образ собирается на `python:3.11-slim`)
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

### Запуск через Docker

```bash
cp .env.example .env        # заполните ключи
docker compose up -d --build
docker compose logs -f      # смотреть логи
docker compose down
```

`.env` в образ не попадает: он исключён через `.dockerignore` и передаётся
в контейнер через `env_file`. Логи и `MessageID.ids` лежат в `./data`, который
монтируется в контейнер, поэтому сохраняются при пересборке.

Запуск образа без Compose тоже работает, но переменные нужно передать явно:

```bash
docker build -t stalzone-bot .
docker run -d --name stalzone_bot --env-file .env \
  -v "$PWD/data:/app/data" -v "$PWD/photos:/app/photos" stalzone-bot
```

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
├── Dockerfile           # Образ контейнера (python:3.11-slim)
├── docker-compose.yml   # Сервис Compose: тома и переменные
├── .dockerignore        # Что не попадает в образ (в том числе .env)
├── .env                 # Секреты и настройки (не в git и не в образе)
├── .env.example         # Шаблон переменных окружения
├── .gitignore           # Правила игнорирования
├── photos/              # Картинка для уведомления о выбросе
└── data/                # Данные работы: логи и MessageID.ids (монтируется)
```

### Логи

Логи пишутся в каталог `data/logs/` через модуль `Debug`: проверки выбросов,
ответы API, отправка сообщений и ошибки. Каталог смонтирован с хоста, поэтому
логи сохраняются между перезапусками контейнера.

### Возможные проблемы

| Симптом | Причина |
| --- | --- |
| При старте `ConnectTimeout: api.telegram.org` | Telegram недоступен из вашей сети. Нужен прокси, например `export HTTPS_PROXY=socks5://127.0.0.1:1080`, либо `telebot.apihelper.proxy` в коде. |
| В логе только `Выброс не ожидается` и больше ничего | Нормальное состояние покоя: выброс не назначен, поэтому поля `currentStart` в ответе нет. Возникающий при этом `KeyError` гасится, как ошибки логируются только реальные сбои запроса. |
| Бот завершается с `Отсутствуют обязательные переменные окружения` | В `.env` не хватает каких-то обязательных переменных или они пустые. |

### Примечания

- Чтобы не пропустить выброс, бот должен работать непрерывно.
- У бота должны быть права на публикацию в целевом канале.
- Endpoint API выбросов: `https://eapi.stalcraft.net/RU/emission`
- Источник онлайна: Steam API, AppID `1818450`

Официальный канал: [@SZInform](https://t.me/SZInform)
