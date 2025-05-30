import os
import requests
import json
import random
import time

# === Настройки API ===
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" 
API_KEY = os.getenv("DASHSCOPE_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# === Темы для генерации ===
TOPICS = [
    "Аркания начинает добычу Этерий-кристалла",
    "Сералия ограничивает импорт технологий Мираники",
    "Фредония проводит учения у границ Сералии",
    "Мираника представляет новый тип нейроинтерфейса",
    "Тирания объявляет о частичной мобилизации"
]

# === Генерация текста через API ===
def generate_with_ai(prompt):
    payload = {
        "model": "qwen-plus",
        "input": {
            "prompt": f"Напиши политическую сводку о мире Этерии. Тема: {prompt}"
        },
        "parameters": {
            "temperature": 0.7,
            "top_p": 0.8,
            "max_tokens": 512
        }
    }

    response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()['output']['text']
    else:
        print("Ошибка при обращении к API:", response.text)
        return None

# === Добавление поста в очередь ===
def add_to_queue(post_text):
    with open('posts/queue.txt', 'a', encoding='utf-8') as f:
        f.write(f'''🗞️ Политическая сводка — {post_text.split(" ")[0]}
🔹 {post_text.strip()}
---
''')

# === Основная функция ===
if __name__ == '__main__':
    topic = random.choice(TOPICS)
    print(f"[INFO] Генерация поста по теме: {topic}")
    
    post = generate_with_ai(topic)
    if post:
        add_to_queue(post)
        print("[SUCCESS] Пост добавлен в очередь.")
    else:
        print("[ERROR] Не удалось получить текст от ИИ.")
