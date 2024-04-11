import telebot
import os
from PIL import Image

bot = telebot.TeleBot("5103664061:AAHPLP_Td4YJerWv3PPsyw9pefMab8ytKyg")

@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    # Отримуємо файл фото
    photo_file = message.photo[-1]

    # Зберігаємо файл у тимчасову папку
    file_path = os.path.join("temp", f"{photo_file.file_id}.jpg")
    bot.download_file(photo_file.file_id, file_path)

    # Відкриваємо зображення за допомогою бібліотеки PIL
    image = Image.open(file_path)

    # Перетворюємо розмір зображення на 512x512 px
    resized_image = image.resize((512, 512))

    # Визначаємо шлях для збереження перетвореного зображення
    output_path = f"{photo_file.file_id}.png"

    # Зберігаємо перетворене зображення у форматі .png
    resized_image.save(output_path, "PNG")

    # Відправляємо перетворене зображення назад у чат
    with open(output_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo)

    # Видаляємо тимчасовий файл та перетворене зображення
    os.remove(file_path)
    os.remove(output_path)

bot.polling()
