import logging
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

# Токен вашего бота
API_TOKEN = "7735642608:AAG1HgbLkfOsj8EmnLY2IYaOCwCEEd-9Zbs"

# ID вашего канала (например, @your_channel)
CHANNEL_ID = "@asdtest41w"

# Ваш ID в Telegram, который будет использоваться для проверки прав администратора
ADMIN_USER_ID = 1046944985

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Функция для создания меню с кнопками
def get_main_menu():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Оповестить подписчиков", callback_data="notify_all"),
        InlineKeyboardButton("Добавить стори с кнопкой", callback_data="add_post"),
    )


# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    # Проверка на администратора
    if message.from_user.id == ADMIN_USER_ID:
        # Отправляем приветственное сообщение с кнопками
        keyboard = get_main_menu()
        await message.answer(
            "Добро пожаловать в бот канала! Вы можете получить историю или оповестить подписчиков.",
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            "Добро пожаловать в бот канала! Вы можете получить историю."
        )


# Функция для отправки сообщения в канал
async def send_message_to_channel(message_text: str, keyboard: InlineKeyboardMarkup = None):
    try:
        # Отправка сообщения в канал с возможной клавиатурой
        await bot.send_message(CHANNEL_ID, message_text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
        logging.info(f"Сообщение отправлено в канал {CHANNEL_ID}")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения в канал: {e}")


# Обработчик нажатия на кнопку "Оповестить подписчиков"
@dp.callback_query_handler(lambda c: c.data == "notify_all")
async def process_notify_all(callback_query: types.CallbackQuery):
    # Проверка, является ли пользователь администратором
    if callback_query.from_user.id != ADMIN_USER_ID:
        await callback_query.answer("У вас нет прав для использования этой функции.")
        return

    try:
        # Оповещаем всех подписчиков канала
        notification_text = (
            "Сюда давай я сказал ✅  @d4815162342d <- Сольет ваши бабки кста ! "
        )
        await send_message_to_channel(notification_text)

        # Ответ на нажатие кнопки
        await callback_query.answer("Все мамонты оповещены!")

    except Exception as e:
        await callback_query.answer(f"Произошла ошибка при отправке оповещения: {e}")


# Обработчик нажатия на кнопку "Добавить стори с кнопкой"
@dp.callback_query_handler(lambda c: c.data == "add_post")
async def add_post(callback_query: types.CallbackQuery):
    # Проверка, является ли пользователь администратором
    if callback_query.from_user.id != ADMIN_USER_ID:
        await callback_query.answer("У вас нет прав для использования этой функции.")
        return

    try:
        # Создание сообщения и кнопки с информацией
        notification_text = (
            "💯 ⚜️ Приветствую, хочу вам показать этого трейдера, который показывает результат, а не болтает ⚜️💯\n\n"
            "Почему он?\n"
            "➖ Обучающий материал\n"
            "➖ Ежедневная торговля в команде\n"
            "➖ Помощь 24/7\n"
            "➖ Персональное наставничество\n\n"
            "‼️ НЕ УПУСТИ ШАНС ЗАРАБОТАТЬ СЕБЕ НА ЖИЗНЬ ‼️\n\n"
            "‼️ Вступай ➡️➡️  https://t.me/+us5nSbOSiMo2YmUy ⬅️⬅️"
        )
        
        # Создание инлайн кнопки с дополнительной информацией
        info_button = InlineKeyboardButton("НЕ УПУСТИ ШАНС В -> VIP", url="https://t.me/+us5nSbOSiMo2YmUy")
        keyboard = InlineKeyboardMarkup().add(info_button)

        # Отправка сообщения с кнопкой в канал
        await send_message_to_channel(notification_text, keyboard)

        # Ответ на нажатие кнопки
        await callback_query.answer("Стори добавлена и отправлена в канал!")

    except Exception as e:
        await callback_query.answer(f"Произошла ошибка: {e}")


# Функция запуска бота
async def on_start():
    # Запускаем бота с обработкой поллинга
    await dp.start_polling()


if __name__ == "__main__":
    # Используем executor для корректного старта бота
    executor.start_polling(dp, skip_updates=True)