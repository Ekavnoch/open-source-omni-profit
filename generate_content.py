from transformers import pipeline
import os
import requests
import sys

# 1. Инициализация генератора модели GPT-2
try:
    generator = pipeline('text-generation', model='gpt2')
except Exception as e:
    print("Ошибка при инициализации генератора:", e)
    sys.exit(1)

# 2. Генерация текста с начальным промптом
try:
    prompt = "Напиши уникальную статью о том, как заработать с помощью бесплатных онлайн инструментов:"
    generated = generator(prompt, max_length=200, num_return_sequences=1)
    if not generated or len(generated) == 0:
        raise ValueError("Генерация не вернула результатов")
    content = generated[0]['generated_text']
except Exception as e:
    print("Ошибка при генерации текста:", e)
    sys.exit(1)

# 3. Сохранение сгенерированного контента в файл Markdown
try:
    os.makedirs("content", exist_ok=True)
    with open("content/generated_article.md", "w", encoding="utf-8") as f:
        f.write("---\nlayout: default\ntitle: 'Новая статья'\n---\n\n")
        f.write(content)
except Exception as e:
    print("Ошибка при сохранении сгенерированного контента:", e)
    sys.exit(1)

# 4. Отправка уведомления через Telegram-бот
try:
    from telegram_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
    message = "Новая статья опубликована! Проверьте: https://ekavnoch.github.io/open-source-omni-profit/"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Ошибка при отправке уведомления Telegram. Статус код:", response.status_code)
except Exception as e:
    print("Telegram уведомление не отправлено:", e)

print("Скрипт завершён успешно")
