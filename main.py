import os
import requests
import time

# Получаем из окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# === Чтение первого поста из очереди ===
def get_next_post():
    with open('posts/queue.txt', 'r', encoding='utf-8') as f:
        content = f.read().strip()

    if '---' in content:
        post, rest = content.split('---', 1)
        post = post.strip()
        with open('posts/queue.txt', 'w', encoding='utf-8') as f:
            f.write(rest.strip())
        return post
    else:
        post = content.strip()
        with open('posts/queue.txt', 'w', encoding='utf-8') as f:
            f.write('')
        return post

# === Отправка поста в Telegram ===
def send_to_telegram(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage' 
    payload = {
        'chat_id': CHANNEL_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    return response.json()

# === Сохранение в архив ===
def archive_post(post):
    os.makedirs('posts/published', exist_ok=True)  # Создаём папку, если её нет
    timestamp = int(time.time())
    filename = f'posts/published/post_{timestamp}.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(post)

# === Основной запуск ===
if __name__ == '__main__':
    post = get_next_post()
    if not post:
        exit(1)
    result = send_to_telegram(post)
    print("Результат отправки:", result)
    archive_post(post)
