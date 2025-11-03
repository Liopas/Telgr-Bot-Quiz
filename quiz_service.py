import aiosqlite

from quiz_keyboard import generate_options_keyboard
from quiz_data import quiz_data
from config import DB_NAME

async def get_question(message, user_id):
    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index, _ = await get_user_data(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    correct_answers = 0
    await update_quiz_index(user_id, current_question_index)
    await update_quiz_stat(user_id, correct_answers)
    await get_question(message, user_id)

async def get_user_data(user_id):
    # Подключаемся к базе данных
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute(
            'SELECT question_index, correct_answers FROM quiz_state WHERE user_id = ?', (user_id, )) as cursor:
            result = await cursor.fetchone()
            if result is not None:
                question_index, correct_answers = result
                return question_index, correct_answers
            else:
                return 0, 0  # Если пользователя нет, возвращаем 0 и 0

async def get_stat(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT correct_answers FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            result = await cursor.fetchone()
            nums = len(quiz_data)
            if result is None:
                return "У вас пока нет статистики."
            if result[0] > 0:
                return f"Ваш результат: {result[0]} из {nums} — {result[0] / nums * 100:.0f}% правильных ответов."
            return f"У вас нет правильных ответов. Вопросов: {nums}" 

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO quiz_state (user_id, question_index)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET question_index=excluded.question_index
        ''', (user_id, index))
        await db.commit()

async def update_quiz_stat(user_id, c_answer):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO quiz_state (user_id, correct_answers)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET correct_answers=excluded.correct_answers
        ''', (user_id, c_answer))
        await db.commit()