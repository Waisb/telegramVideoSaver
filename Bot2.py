from pytube import YouTube #22 оптимальный формат 
from pytube import exceptions as youtubeExceptions
import telebot
import re
import uuid
import database
import os

botKey = "7257106830:AAEBEzCXf_yZtZqfhMQaFdNN_59uhvdGXe8"
Bot = telebot.TeleBot(botKey, threaded=True, num_threads=3)

@Bot.message_handler(commands = ["start"]) #Пользователь запустил бота
def command_start(message):
    Bot.send_message(message.chat.id, "Сохранялка видео с ютуба.")
    
@Bot.message_handler(content_types=['text'])
def work_with_text(message):
    #проверка есть ли ютуб в ссылке
    if re.search("youtube", message.text):
       try: #Проверка все ли ок с видео
           yt = YouTube(message.text) 
           already_saved = database.search_video(message.text)
           if already_saved: #Проверка есть ли видео в базе
               print(f"Информация: видео уже есть {message.text}")
               Bot.reply_to(message, "Этот ролик уже есть.")
           else:#Видео нет. И видео проверено. Скачиваем.
               print(f"Информация: видео скачивается {message.text}")
               stream = yt.streams.get_by_itag(22) #22 это id задачи на mp4
               
               video_path = f"Videos/{uuid.uuid4()}.mp4" #Путь до видео
               if not os.path.exists("Videos"): #Создать папку видеос если ее нет
                   os.makedirs("Videos")
               stream.download(filename=video_path,) #скачивание
               Bot.reply_to(message, f"Видео сохранено\nПуть: {video_path}") #ответ пользователю что видео сохранено
               database.add_video_to_database(message.text, video_path) #Добавление видео в базу
               print(f"Информация: видео сохранено {video_path}")
               
       except youtubeExceptions.RegexMatchError: #Библиотеке не понравилась ссылка (ошибка или видео нет)
           print(f"Ошибка: ссылка не на ютуб видео {message.text}")
           Bot.reply_to(message, "Это не ссылка на ролик или ссылка с ошибкой.")
       except Exception as error: #Общая ошибка при скачивании.
           print(f"Ошибка: не удалось сохранить видео {message.text}\n{str(error)}")
           Bot.reply_to(message, f"Не удалось сохранить видео :(\n{str(error)}")

    else:#Слово ютуб не найдено. Это не ссылка на ютуб
        Bot.reply_to(message, "Это не ссылка на ютуб")


Bot.infinity_polling(skip_pending=True)