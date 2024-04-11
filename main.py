import telebot
import os
from PIL import Image

bot = telebot.TeleBot("5103664061:AAHPLP_Td4YJerWv3PPsyw9pefMab8ytKyg")

@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    # Отримуємо файл фото
    file_info = bot.get_file(message.photo[-1].file_id)
    # Завантаження фото
    downloaded_file = bot.download_file(file_info.file_path)
    # Збереження фото на сервері або обробка його
    # Наприклад, збереження фото під унікальним іменем
    filename = f'photo_{file_info.file_id}.png'
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Відкриваємо зображення за допомогою бібліотеки PIL
    image = Image.open(filename)

    # Перетворюємо розмір зображення на 512x512 px
    resized_image = image.resize((512, 512))

    # Визначаємо шлях для збереження перетвореного зображення
    output_path = "1"+filename

    # Зберігаємо перетворене зображення у форматі .png
    resized_image.save(output_path, "png")

    # Відправляємо перетворене зображення назад у чат
    with open(output_path, "rb") as photo:
        bot.send_document(message.chat.id, photo)

    # Видаляємо тимчасовий файл та перетворене зображення
    os.remove(filename)
    os.remove(output_path)

bot.polling()
