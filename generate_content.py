from transformers import pipeline
import os
import requests

# Инициализация генератора с моделью GPT-2 (бесплатная и доступная)
generator = pipeline('text-generation', model='gpt2')

# Генерация текста с начальным промптом
prompt = "Напиши уникальную статью о том, как заработать с помощью бесплатных онлайн инструментов:"
generated = generator(prompt, max_length=200, num_return_sequences=1)
content = generated[0]['generated_text']

# Создаем папку, если не существует
os.makedirs("content", exist_ok=True)

# Сохраняем статью в формате Markdown
with open("content/generated_article.md", "w", encoding="utf-8") as f:
    f.write("---\nlayout: default\ntitle: 'Новая статья'\n---\n\n")
    f.write(content)

# Отправка уведомления через Telegram-бот
try:
    from telegram_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
    # Используем ваш URL сайта
    message = "Новая статья опубликована! Проверьте: https://ekavnoch.github.io/open-source-omni-profit/"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}"
    requests.get(url)
except Exception as e:
    print("Telegram уведомление не отправлено:", e)
