"""Конфигурация проекта.

Все секреты и настройки читаются из переменных окружения.
Локально значения берутся из файла `.env` в корне проекта (шаблон — `.env.example`),
в продакшене — из реального окружения (shell, Docker, systemd, CI).

Приоритет: реальные переменные окружения важнее значений из `.env`.
"""

import os

try:
    from dotenv import load_dotenv
except ImportError:  # python-dotenv не установлен — работаем только на системных переменных
    load_dotenv = None


if load_dotenv is not None:
    load_dotenv()


class ConfigError(RuntimeError):
    """Выбрасывается, если обязательная переменная окружения не задана."""


class Config:
    """Доступ к переменным окружения с валидацией и кэшированием."""

    # Переменные без которых бот работать не может
    REQUIRED = ("TG_CLIENT_TOKEN", "CLIENT_SECRET", "CLIENT_ID")

    _cache = {}

    @classmethod
    def get(cls, name, default=None):
        """Возвращает значение переменной окружения.

        Пустое значение обязательной переменной (из REQUIRED) считается ошибкой,
        если не передан `default`.
        """
        if name in cls._cache:
            return cls._cache[name]

        value = (os.getenv(name) or "").strip()
        if not value:
            if default is None and name in cls.REQUIRED:
                raise ConfigError(
                    f"Не задана обязательная переменная окружения {name}. "
                    f"Скопируйте .env.example в .env и заполните его."
                )
            return default

        cls._cache[name] = value
        return value

    @classmethod
    def get_int(cls, name, default):
        """То же, что get(), но приводит значение к int."""
        raw = cls.get(name, default=str(default))
        try:
            return int(raw)
        except (TypeError, ValueError):
            raise ConfigError(
                f"Переменная окружения {name} должна быть целым числом, получено: {raw!r}"
            )

    @classmethod
    def validate(cls):
        """Проверяет, что все обязательные переменные заданы.

        Вызывается при старте, чтобы упасть сразу и с понятным сообщением,
        а не в середине работы бота.
        """
        missing = [name for name in cls.REQUIRED if not (os.getenv(name) or "").strip()]
        if missing:
            raise ConfigError(
                "Отсутствуют обязательные переменные окружения: "
                + ", ".join(missing)
                + "\nСкопируйте .env.example в .env и заполните значения."
            )
        return True
