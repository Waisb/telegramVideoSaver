import sqlite3
import threading
#Подключение к базу
connection = sqlite3.connect("video.db",check_same_thread=False)
cursor = connection.cursor()
#Создание ячеек и таблицы в случае если ее нет
cursor.execute('''CREATE TABLE IF NOT EXISTS video (
url TEXT PRIMARY_KEY,
filename TEXT NOT NULL)
''')

#Добавление видео в базу данных
def add_video_to_database(url, filename):
    cursor.execute("INSERT INTO video (url,filename) VALUES (?,?)",(url, filename))
    connection.commit()
#Поиск видео в базе данных. Возвращает False если видео нет. Возвращает путь к файлу если видео есть.   
def search_video(url):
    with threading.Lock():
       cursor.execute("SELECT * FROM video WHERE url=(?)", (url,)) 
       result = cursor.fetchone()
       if result is None:
           return False
       if len(result) > 0:
           if result[0] is None:
               return False
           else:
               return result[0]
