import os
import requests
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()


def send_telegram_message(file_path: str):
    """
    Читает текст из файла и отправляет его в Telegram через бота.
    """
    # Получаем конфиги
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Простая валидация конфигов
    if not bot_token or not chat_id:
        print("❌ Ошибка: Не найдены TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID в .env файле.")
        return

    try:
        # Читаем сообщение
        if not os.path.exists(file_path):
            print(f"❌ Ошибка: Файл '{file_path}' не найден.")
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            message_text = f.read().strip()

        if not message_text:
            print("⚠️ Файл пуст, отправка отменена.")
            return

        # Формируем запрос
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"  # Можно убрать, если текст содержит спецсимволы
        }

        print(f"Отправка сообщения из '{file_path}'...")

        # Отправляем (timeout важен, чтобы скрипт не висел вечно)
        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            print("✅ Сообщение успешно отправлено!")
        elif response.status_code == 400 and "chat not found" in response.text:
            print(f"❌ Ошибка: Чат не найден (400).")
            print("💡 Подсказка: Вы написали боту /start? Бот не может писать первым.")
            print(f"Ваш Chat ID в настройках: {chat_id}")
        elif response.status_code == 401:
            print(f"❌ Ошибка авторизации (401). Проверьте токен бота.")
        else:
            print(f"❌ Ошибка API Telegram: {response.status_code}")
            print(f"Ответ сервера: {response.text}")

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    # Имя файла с сообщением (должен лежать рядом)
    input_file = "message.txt"
    send_telegram_message(input_file)