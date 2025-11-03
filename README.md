# Telegram Bot Quiz
Telegram-бот для проведения викторин.  
Реализован на Python.  
Библиотеки: asyncio, aiosqlite, aiogram, logging.
## Команды
/start - регистрация и приветствие

/quiz - начать новую викторину

/stat - просмотр статистики пользователя
## Архитектура проекта
bot.py - точка входа, инициализация и запуск бота

config.py/template_config.py - конфигурационные параметры

handlers.py - обработчики команд и callback'ов

quiz_data.py - данные викторины (вопросы, варианты ответов)

quiz_keyboard.py - генератор инлайн-клавиатур

quiz_service.py - бизнес-логика викторины
