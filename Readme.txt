Fake Tinder Bot

Название бота: FakeTinderBot

Тема бота: Имитация бота для знакомств (Tinder-like)

Авторы: D1n976, Kiry999


🔹 Список команд
Команда	                         Описание
/start	                         Запуск бота, приветствие
Мой профиль	                 Просмотр своего профиля
Настроить анкету	         Изменить данные профиля
Анкеты                           Поиск анкет
Лайк [ID]	  	         Лайкнуть пользователя
Пропустить [ID]	  	         Пропустить пользователя
Начать переписку[ID]	         Начать чат с пользователем
Перейти в бота                   Переход в бота для начала чата с пользоватилем
Остановить переписку[ID]         Остановить чат с пользователем
Получить погоду по списку стран  Ищет погоду по странам
Получить погоду по координатам   Ищет погоду по координатам
Получить кота                    Получить кота по запросу
Назад                            Вернуться назад
/help                            Получить справку по командам
/about                           Информация о боте и авторах
/more                            Получить список опцианальных программ
/roll                            Случайное число


🔹 Usertag бота + ссылка на него
@minifinder2_bot
https://t.me/minifinder2_bot

🔹 Описание / Функционал
Бот имитирует функционал приложения для знакомств (Tinder). Основные возможности:

✅ Профиль пользователя

Регистрация
Редактирование данных (имя, возраст, фото, описание)
Удаление аккаунта

✅ Поиск и взаимодействие

Просмотр анкет других пользователей
Лайки / дизлайки
Взаимные лайки (матчи)

✅ Чат

Общение с пользователями, с которыми есть мэтч
Уведомления о новых сообщениях


🔹 Структура базы данных

create database fake_tinder

CREATE TABLE genres(
ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY ,
genre TEXT UNIQUE
)

CREATE TABLE users(
ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
telegram_id BIGINT NOT NULL UNIQUE,
telegram_user_name TEXT,
user_name TEXT,
genre INT,
genre_like INT,
description TEXT,
photo TEXT,
age INT,
country TEXT,
FOREIGN KEY (genre) REFERENCES genres(ID),
FOREIGN KEY (genre_like) REFERENCES genres(ID)
)

CREATE TABLE selected_users(
user_id INT UNIQUE,
selected_user_id INT,
FOREIGN KEY (user_id) REFERENCES users(ID)
)

CREATE TABLE like_request(
user_id INT,
like_user_id INT,
FOREIGN KEY (user_id) REFERENCES users(ID),
FOREIGN KEY (like_user_id) REFERENCES users(ID)
)
    
CREATE TABLE sessions(
from_user_id INT,
to_user_id INT,
FOREIGN KEY (from_user_id) REFERENCES users(ID),
FOREIGN KEY (to_user_id) REFERENCES users(ID)
)



🔹 Сторонние библиотеки
Библиотека              

python-aiogrom
mysql.connector	   
yaml     
requests	        
Pillow (PIL)	        
datetime	        
logging	                
pandas
matplotlib
fpdf
apscheduler
csv
json
