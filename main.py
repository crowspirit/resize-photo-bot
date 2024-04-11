import os
from PIL import Image
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot_token = "5103664061:AAHPLP_Td4YJerWv3PPsyw9pefMab8ytKyg"
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def process_photo(message: types.Message):
    # Отримуємо об'єкт з фотографією
    photo = message.photo[-1]
    
    # Отримуємо об'єкт файлу за його ідентифікатором
    file = await bot.get_file(photo.file_id)
    
    # Зберігаємо файл у тимчасову папку
    file_path = os.path.join("temp", f"{photo.file_id}.jpg")
    await file.download(destination=file_path)
    
    # Відкриваємо зображення за допомогою бібліотеки PIL
    image = Image.open(file_path)
    
    # Перетворюємо розмір зображення на 512x512 px
    resized_image = image.resize((512, 512))
    
    # Визначаємо шлях для збереження перетвореного зображення
    output_path = (f"{photo.file_id}.png")
    
    # Зберігаємо перетворене зображення у форматі .png
    resized_image.save(output_path, "PNG")
    
    # Відправляємо перетворене зображення назад у чат
    with open(output_path, "rb") as photo_file:
        await message.reply_document(photo_file)
    
    # Видаляємо тимчасовий файл та перетворене зображення
    os.remove(file_path)
    os.remove(output_path)


async def main():
    # Запускаємо бота
    await dp.start_polling()


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
