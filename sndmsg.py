import logging
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from pyrogram import Client
import logging
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

# Your API credentials for Pyrogram (Replace with actual values)
API_ID = "25432811"  # Replace with your api_id
API_HASH = "76ccba0da25c56fec0667084db89b6e6"  # Replace with your api_hash

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Pyrogram client для работы с участниками
app = Client("my_bot", bot_token=API_TOKEN, api_id=API_ID, api_hash=API_HASH)


# Функция для создания главного меню с кнопками (разделение на три ряда)
def get_main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)  # Указываем два столбца в ряду
    # Добавляем кнопки
    keyboard.add(
        InlineKeyboardButton(
            "Оповестить подписчиков Начало Торгов", callback_data="notify_all"
        ),
        InlineKeyboardButton("Оповестить подписчиков в лс", callback_data="notifpod"),
    )
    keyboard.add(
        InlineKeyboardButton("Кругляш с кнопкой", callback_data="addvid"),
    )
    keyboard.add(
        InlineKeyboardButton(
            "Получить список участников", callback_data="get_all_chambers"
        ),
    )
    return keyboard


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
async def send_message_to_channel(
    message_text: str, keyboard: InlineKeyboardMarkup = None
):
    try:
        # Отправка сообщения в канал с возможной клавиатурой
        await bot.send_message(
            CHANNEL_ID,
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard,
        )
        logging.info(f"Сообщение отправлено в канал {CHANNEL_ID}")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения в канал: {e}")


# Функция для отправки сообщений подписчикам в личные сообщения
async def send_message_to_users(message_text: str):
    try:
        # Получаем список всех участников канала
        members = await bot.get_chat_members(
            CHANNEL_ID, 0, 200
        )  # Получаем первые 200 участников
        for member in members:
            # Проверка, является ли пользователь подписчиком
            if member.status in [
                "member",
                "administrator",
                "creator",
            ]:  # проверяем активных участников
                try:
                    # Отправка личного сообщения
                    await bot.send_message(
                        member.user.id,
                        message_text,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                    logging.info(f"Сообщение отправлено пользователю {member.user.id}")
                except Exception as e:
                    logging.error(
                        f"Ошибка при отправке сообщения пользователю {member.user.id}: {e}"
                    )
    except Exception as e:
        logging.error(f"Ошибка при получении участников канала: {e}")


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
            "Начинаем Торги! Вся инфа в Випке! Кто еще не с нами залетай в Випку!"
        )
        await send_message_to_channel(notification_text)

        # Оповещаем пользователей по их ID
        await send_message_to_users(notification_text)

        # Ответ на нажатие кнопки
        await callback_query.answer("Все мамонты оповещены!")

    except Exception as e:
        await callback_query.answer(f"Произошла ошибка при отправке оповещения: {e}")


# Обработчик нажатия на кнопку "Добавить стори с кнопкой"
@dp.callback_query_handler(lambda c: c.data == "notifpod")
async def notifpod(callback_query: types.CallbackQuery):
    # Проверка, является ли пользователь администратором
    if callback_query.from_user.id != ADMIN_USER_ID:
        await callback_query.answer("У вас нет прав для использования этой функции.")
        return

    try:
        # Создание сообщения и кнопки с информацией
        notification_text = (
            "💯 ⚜️ Ты что еще не в випке? ⚜️💯\n\n"
            "Не хочешь заработать и улучшить свою жизнь?\n"
            "Залетай к нам и поднимай вместе с нами !\n"
            "У нас : \n"
            "➖ Ежедневная торговля в команде\n"
            "➖ Помощь 24/7\n"
            "➖ Персональное наставничество\n\n"
            "‼️ НЕ ПРОМОРГАЙ ВОЗМОЖНОСТЬ ЗАРАБОТАТЬ СЕБЕ НА ЖИЗНЬ ‼️\n\n"
        )

        # Создание инлайн кнопки с дополнительной информацией
        info_button = InlineKeyboardButton(
            "НЕ УПУСТИ СВОЙ ШАНС", url="https://t.me/tradesrngoffical"
        )
        keyboard = InlineKeyboardMarkup().add(info_button)

        # Отправка сообщения с кнопкой в канал
        await send_message_to_channel(notification_text, keyboard)

        # Ответ на нажатие кнопки
        await callback_query.answer("Стори добавлена и отправлена в канал!")

    except Exception as e:
        await callback_query.answer(f"Произошла ошибка: {e}")


# Обработчик нажатия на кнопку "Добавить стори с кнопкой"
@dp.callback_query_handler(lambda c: c.data == "addvid")
async def addvid(callback_query: types.CallbackQuery):
    # Проверка, является ли пользователь администратором
    if callback_query.from_user.id != ADMIN_USER_ID:
        await callback_query.answer("У вас нет прав для использования этой функции.")
        return

    try:
        # Отправляем сообщение с просьбой записать видео
        await callback_query.message.answer(
            "Пожалуйста, запишите ваше сообщение на видео и отправьте его сюда."
        )

        # Ожидаем видео от пользователя
        @dp.message_handler(content_types=types.ContentType.VIDEO_NOTE)
        async def handle_video(message: types.Message):
            # Получаем данные о видео
            video = message.video_note
            # Создание кнопки с информацией
            info_button = InlineKeyboardButton(
                "ВСТУПИТЬ В КОМАНДУ✅", url="https://t.me/tradesrngoffical"
            )
            keyboard = InlineKeyboardMarkup().add(info_button)

            # Формируем сообщение с видео и кнопкой
            await message.answer_video(video.file_id, reply_markup=keyboard)

            # Отправляем сообщение в нужную группу (замените group_id на актуальный)
            group_id = "@asdtest41w"
            await dp.bot.send_video(group_id, video.file_id, reply_markup=keyboard)

            # Подтверждаем пользователю, что видео отправлено
            await message.answer(
                "Ваше видео было успешно отправлено в группу с кнопкой!"
            )

    except Exception as e:
        await callback_query.answer(f"Произошла ошибка: {str(e)}")


# Обработчик нажатия на кнопку "Получить список участников"
@dp.callback_query_handler(lambda c: c.data == "get_all_chambers")
async def get_all_chambers(callback_query: types.CallbackQuery):
    # Проверка, является ли пользователь администратором
    if callback_query.from_user.id != ADMIN_USER_ID:
        await callback_query.answer("У вас нет прав для использования этой функции.")
        return

    try:
        # Получаем всех участников канала с помощью Pyrogram
        members = []
        async for member in app.get_chat_members(CHANNEL_ID):
            members.append(f"{member.user.id} - {member.user.username}")

        # Отправляем список участников в чат
        members_list = "\n".join(members)
        await callback_query.message.answer(
            f"Список участников канала:\n\n{members_list}"
        )

    except Exception as e:
        await callback_query.answer(
            f"Произошла ошибка при получении списка участников: {e}"
        )


# Функция запуска бота
async def on_start():
    # Запускаем Pyrogram client в фоновом режиме
    await app.start()

    # Запускаем бота с помощью aiogram
    await dp.start_polling()

if __name__ == "__main__":
    # Запускаем основную асинхронную функцию
    app.run(on_start())