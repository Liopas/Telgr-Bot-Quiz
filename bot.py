from aiogram import Bot, Dispatcher
import asyncio, logging, aiosqlite

from config import API_TOKEN, DB_NAME
from handlers import register_handlers

import nest_asyncio
nest_asyncio.apply()

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Диспетчер
dp = Dispatcher()

# Объект бота
bot = Bot(token=API_TOKEN)

async def create_table():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, correct_answers INTEGER)''')
        # Сохраняем изменения
        await db.commit()

# Запуск процесса поллинга новых апдейтов
async def main():
    await create_table() # создание таблицы базы данных
    register_handlers(dp, bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())