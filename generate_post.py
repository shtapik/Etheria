import os
import random
from dashscope import Generation
import dashscope
import json

# === Настройки API ===
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")  # Берём из GitHub Secrets

# === Темы для генерации ===
TOPICS = [
    "конфликт за Этерий-кристалл между Арканией и Тиранией",
    "протесты в университетах Сералии против цензуры",
    "Фредония проводит учения у границы с Сералией",
    "Мираника представляет новый нейроинтерфейс",
    "Тирания объявляет о частичной мобилизации"
]

# === Генерация текста от ИИ ===
def generate_with_qwen(topic):
    generation = Generation(model="qwen-plus")
    full_prompt = f"Напиши политическую сводку о мире Этерии. Тема: {topic}"
    response = generation.call(
        prompt=full_prompt,
        temperature=0.7,
        top_p=0.8,
        max_tokens=4096
    )
    return response.output.text.strip()

# === Добавление поста в очередь ===
def add_to_queue(post_text, country_name):
    formatted_post = f'''🗞️ Политическая сводка — {country_name}
🔹 {post_text}
'''
    with open('posts/queue.txt', 'a', encoding='utf-8') as f:
        f.write(formatted_post + '\n---\n')

if __name__ == '__main__':
    selected_topic = random.choice(TOPICS)
    print(f"[INFO] Генерация поста по теме: {selected_topic}")

    try:
        post = generate_with_qwen(selected_topic)
        country_name = selected_topic.split(" ")[0]
        add_to_queue(post, country_name)
        print("[SUCCESS] Пост добавлен в очередь.")
    except Exception as e:
        print("[ERROR] Не удалось получить текст от ИИ:", str(e))
