import telebot
import config
from datetime import date
import pandas as pd
import locale

bot = telebot.TeleBot(config.token)
#Делаем даты Русскими
locale.setlocale(locale.LC_ALL, '')

def bd_info():
    # Сегодняшняя дата
    now = pd.to_datetime(date.today())
    # print('NOW -', now.dayofyear)

    #Скачиваем исходный файл и формируем БД для вывода в телегу
    data = pd.read_csv(config.adress_data, index_col=0, names=["FIO", "BiD"])
    data['BiD'] = pd.to_datetime(data['BiD'], format='%d.%m.%Y')
    #Делаем отдельным столбцом номер дня
    data['DoY'] = list(map(lambda day: day.dayofyear, data['BiD']))
    #Делаем отдельным столбцом если ДР сегодня
    data['Birth_now'] = list(map(lambda x: True if x == now.dayofyear else False, data['DoY']))
    #Делаем отдельным столбцом если юбилей
    data['Yubiley'] = list(map(lambda x: True if (now.year-x.year)%5 == 0 else False, data['BiD']))

    # print(data.head())

    today_celebrate = data[(data["DoY"] >= now.dayofyear) & (data["DoY"] <= now.dayofyear + config.days_in_view)].sort_values(by=['DoY'])
    # print(today_celebrate)

    # Формируем выдачу в телеграм
    telegram_text = f'В ближайшие {config.days_in_view} дней днюшки-уткушки празднуют: \n'

    for index, row in today_celebrate.iterrows():
        #Дата
        if row.Birth_now:
            date_in_verb = "СЕГОДНЯ, " + row.BiD.strftime('%d %B')
        else:
            date_in_verb = row.BiD.strftime('%d %B')
        #Юбилей
        yubiley = " 🥇" if row.Yubiley else ""

        telegram_text += date_in_verb + " - " + row.FIO + yubiley + "\n"
        # print(row)

    print(telegram_text)

    return telegram_text

bd_info()

@bot.message_handler(commands=['DR'])
def birthday(message):
    today_celebrate = bd_info()
    if today_celebrate:
        bot.send_message(message.chat.id, today_celebrate)
    else:
        bot.send_message(message.chat.id, "За обозримом будущем ни у кого днюшки нет.")


# @bot.message_handler(content_types=['text'])
# def lalala(message):
#     bot.send_message(message.chat.id, message.text)

# RUN
bot.polling(none_stop=True)




# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')
#
# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text.lower() == 'привет':
#         bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}!')
#     else:
#         bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')
#
#
# # RUN
# bot.polling(none_stop=True)