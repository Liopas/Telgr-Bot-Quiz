from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F

from quiz_service import new_quiz, get_user_data, update_quiz_index, update_quiz_stat, get_question, get_stat
from quiz_data import quiz_data

def register_handlers(dp: Dispatcher, bot):
    
    @dp.callback_query(lambda c: c.data.startswith(('right', 'wrong')))
    async def handle_answer(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        
        status, user_answer = callback.data.split(":", 1)  # разделяем статус и текст ответа

        # Убираем кнопки после ответа
        await callback.bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=callback.message.message_id,
            reply_markup=None
        )

        await callback.message.answer(f"🧩 Ваш ответ: {user_answer}")

        # Получаем данные квиза
        current_question_index, correct_answers = await get_user_data(user_id)

        # Проверяем правильность ответа
        if status == "right_answer":
            await callback.message.answer("✅ Верно!")
            correct_answers += 1
            await update_quiz_stat(user_id, correct_answers)
        else:
            correct_option = quiz_data[current_question_index]['correct_option']
            correct_text = quiz_data[current_question_index]['options'][correct_option]
            await callback.message.answer(f"❌ Неправильно. Правильный ответ: {correct_text}")

        # Переходим к следующему вопросу
        current_question_index += 1
        await update_quiz_index(user_id, current_question_index)

        if current_question_index < len(quiz_data):
            await get_question(callback.message, user_id)
        else:
            await callback.message.answer("🏁 Это был последний вопрос. Квиз завершен! 🏁")
            text = await get_stat(user_id)
            await bot.send_message(chat_id=user_id, text=text)

    # Хэндлер на команду /start
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        builder = ReplyKeyboardBuilder()
        builder.add(types.KeyboardButton(text="Начать игру"))
        await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

    # Хэндлер на команду /stat
    @dp.message(Command("stat"))
    async def cmd_stat(message: types.Message):
        user_id = message.from_user.id
        stat_text = await get_stat(user_id)
        await message.answer(f"-- Статистика --\n{stat_text}")

    # Хэндлер на команду /quiz
    @dp.message(F.text=="Начать игру")
    @dp.message(Command("quiz"))
    async def cmd_quiz(message: types.Message):
        await message.answer(f"Давайте начнем квиз!")
        await new_quiz(message)