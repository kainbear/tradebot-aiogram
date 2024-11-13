import logging
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

# Токен вашего бота
API_TOKEN = '7735642608:AAG1HgbLkfOsj8EmnLY2IYaOCwCEEd-9Zbs'

# ID вашего канала (например, @your_channel)
CHANNEL_ID = '@asdtest41w'

# Ваш ID в Telegram, который будет использоваться для проверки прав администратора
ADMIN_USER_ID = 1046944985

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Функция для создания меню с кнопками
def get_main_menu():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Получить историю", callback_data="get_history"),
        InlineKeyboardButton("Оповестить подписчиков", callback_data="notify_all")
    )

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    # Проверка на администратора
    if message.from_user.id == ADMIN_USER_ID:
        # Отправляем приветственное сообщение с кнопками
        keyboard = get_main_menu()
        await message.answer("Добро пожаловать в бот канала! Вы можете получить историю или оповестить подписчиков.", reply_markup=keyboard)
    else:
        await message.answer("Добро пожаловать в бот канала! Вы можете получить историю.")

# Функция для отправки сообщения в канал
async def send_message_to_channel(message_text: str):
    try:
        # Отправка сообщения в канал
        await bot.send_message(CHANNEL_ID, message_text, parse_mode=ParseMode.MARKDOWN)
        logging.info(f"Сообщение отправлено в канал {CHANNEL_ID}")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения в канал: {e}")

# Обработчик нажатия на кнопку "Получить историю"
@dp.callback_query_handler(lambda c: c.data == "get_history")
async def process_callback_get_history(callback_query: types.CallbackQuery):
    try:
        # Пример истории
        story_text = (
            f"Вот ваша история, {callback_query.from_user.username}:\n\n"
            "В один прекрасный день, бот решил рассказать историю.\n"
            "Это была история о том, как бот помогает пользователям!"
        )

        # Отправляем историю пользователю
        await bot.send_message(callback_query.from_user.id, story_text, parse_mode=ParseMode.MARKDOWN)

        # Ответ на нажатие кнопки
        await callback_query.answer("История выложена!")

        # Уведомление через 5 секунд
        await asyncio.sleep(5)  # Пауза в 5 секунд
        await bot.send_message(callback_query.from_user.id, "Уведомление через 5 секунд: Вы нажали на кнопку для получения истории.", parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await callback_query.answer(f"Произошла ошибка: {e}")

# Обработчик нажатия на кнопку "Оповестить подписчиков"
@dp.callback_query_handler(lambda c: c.data == "notify_all")
async def process_notify_all(callback_query: types.CallbackQuery):
    # Проверка, является ли пользователь администратором
    if callback_query.from_user.id != ADMIN_USER_ID:
        await callback_query.answer("У вас нет прав для использования этой функции.")
        return

    try:
        # Оповещаем всех подписчиков канала
        notification_text = ("Внимание! Друзья, всех приветствую 👋 Скоро приступим к торговле ✅ ")
        await send_message_to_channel(notification_text)

        # Ответ на нажатие кнопки
        await callback_query.answer("Все подписчики оповещены!")

    except Exception as e:
        await callback_query.answer(f"Произошла ошибка при отправке оповещения: {e}")

# Функция запуска бота
async def on_start():
    # Запускаем бота с обработкой поллинга
    await dp.start_polling()

if __name__ == '__main__':
    # Используем executor для корректного старта бота
    executor.start_polling(dp, skip_updates=True)