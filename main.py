import os
import requests
import random
import time

# === Получаем данные из окружения ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# === Пример функции получения текста (заменяй на запросы ко мне) ===
def generate_news():
    return '''🗞️ **Политическая сводка — Аркания**
🔹 Королева Элис IV объявила о начале добычи **Этерий-кристалла** в новых районах.
📌 Это вызвало обеспокоенность у соседей, особенно у Тирании, которая заявила, что "не позволит эксплуатировать ресурсы силой".'''

# === Отправка в Telegram ===
def send_to_telegram(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage' 
    payload = {
        'chat_id': CHANNEL_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    return response.json()

# === Чтение из файла очереди постов ===
def get_next_post():
    with open('posts/queue.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines:
        return None
    first_line = lines[0].strip()
    with open('posts/queue.txt', 'w', encoding='utf-8') as f:
        f.writelines(lines[1:])
    return first_line

# === Сохранение в архив ===
def archive_post(post):
    timestamp = int(time.time())
    filename = f'posts/published/post_{timestamp}.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(post)

# === Основная логика ===
if __name__ == '__main__':
    post = get_next_post()
    if not post:
        print("Очередь постов пуста.")
        exit(1)

    result = send_to_telegram(post)
    print("Результат отправки:", result)

    archive_post(post)