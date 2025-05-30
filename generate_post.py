import os
import requests
import json
import random

# === Настройки ===
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions" 
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": os.getenv("SITE_URL", "https://example.com"),   # опционально
    "X-Title": os.getenv("SITE_NAME", "Etheria News")             # опционально
}

# === Темы для генерации постов ===
TOPICS = [
    "Аркания начинает добычу Этерий-кристалла",
    "Сералия блокирует технологии Мираники",
    "Фредония проводит учения у границ Сералии",
    "Мираника представляет новый нейроинтерфейс",
    "Тирания объявляет о частичной мобилизации"
]

# === Генерация текста через OpenRouter ===
def generate_with_openrouter(prompt):
    payload = {
        "model": "qwen/qwen3-235b-a22b:free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "top_p": 0.8,
        "max_tokens": 4096
    }

    response = requests.post(OPENROUTER_API_URL, headers=HEADERS, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Ошибка при обращении к OpenRouter:", response.text)
        return None

# === Добавление поста в очередь ===
def add_to_queue(post_text, country_name):
    formatted_post = f'''🗞️ Политическая сводка — {country_name}
🔹 {post_text.strip()}
'''
    with open('posts/queue.txt', 'a', encoding='utf-8') as f:
        f.write(formatted_post + '\n---\n')

# === Основная функция ===
if __name__ == '__main__':
    selected_topic = random.choice(TOPICS)
    print(f"[INFO] Генерация поста по теме: {selected_topic}")

    prompt = f"Напиши политическую сводку о мире Этерии на основе этой темы: {selected_topic}. Формат: 🗞️ Политическая сводка — [Страна], 🔹 Краткий анализ, 📌 Международная реакция"

    post = generate_with_openrouter(prompt)
    if post:
        country_name = selected_topic.split(" ")[0]
        add_to_queue(post, country_name)
        print("[SUCCESS] Пост добавлен в очередь.")
    else:
        print("[ERROR] Не удалось получить ответ от ИИ.")
