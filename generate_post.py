import os
import requests
import json

# === Настройки API ===
QWEN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" 
QWEN_API_KEY = os.getenv("QWEN_API_KEY")  # Берём из Secrets
HEADERS = {
    "Authorization": f"Bearer {QWEN_API_KEY}",
    "Content-Type": "application/json"
}

# === Темы для генерации ===
TOPICS = [
    "Конфликт за Этерий-кристалл между Арканией и Тиранией",
    "Протесты в университетах Сералии против цензуры",
    "Фредония начинает военную операцию у границы с Сералией",
    "Мираника запускает новый тип нейроинтерфейса на основе Нейропласта",
    "Аркания предлагает международное соглашение по климату"
]

# === Генерация текста от ИИ ===
def generate_with_qwen(topic):
    payload = {
        "model": "qwen-plus",
        "input": {
            "prompt": f"Напиши политическую сводку о мире Этерии. Тема: {topic}"
        },
        "parameters": {
            "temperature": 0.7,
            "top_p": 0.8,
            "max_tokens": 300
        }
    }

    response = requests.post(QWEN_API_URL, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()['output']['text']
    else:
        print("Ошибка при обращении к API:", response.text)
        return None

# === Добавление поста в очередь ===
def add_to_queue(post):
    with open('posts/queue.txt', 'a', encoding='utf-8') as f:
        f.write(f'''🗞️ Политическая сводка — {post.split(" ")[0]}
🔹 {post.strip()}
---
''')

# === Основная функция ===
if __name__ == '__main__':
    import random
    topic = random.choice(TOPICS)
    print(f"[INFO] Генерация поста по теме: {topic}")
    
    post_text = generate_with_qwen(topic)
    if post_text:
        add_to_queue(post_text)
        print("[SUCCESS] Пост добавлен в очередь.")
    else:
        print("[ERROR] Не удалось получить текст от ИИ.")
