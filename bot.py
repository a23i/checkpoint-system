#!/usr/bin/env python3
import telebot
import parser
from telebot import types
from telebot import apihelper
import cv_controller as cvc
import subprocess
from tokens import TOKEN, proxydata, admins

bot = telebot.TeleBot(TOKEN)

# Setting proxy
apihelper.proxy = {'https':'socks5h://{}:{}@{}:{}'.format(proxydata['username'],proxydata['pass'],proxydata['ip'],proxydata['port'])}

# Camera vars
fo = cvc.FaceOperator()
camera_running = False
process = None

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    global camera_running
    global process

    clockworker = subprocess.Popen(['python', 'clockworker.py'])

    if not camera_running:
    # Start camera handler subprocess
        print('[INFO] Camera handler subproccess is running...')
        print('>>>>>> Face detection active')
        process = subprocess.Popen(['python','camera_handler.py'])

        camera_running = True

    itr = message.chat.id
    # Check if user is admin
    if itr in admins:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Прошедшие сотрудники', 'Узнать по фамилии', 'Добавить', 'Удалить', 'База сотрудников']])
        bot.send_message(message.chat.id, 'Здраствуйте!',reply_markup=keyboard)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Прошедшие сотрудники', 'Узнать по фамилии']])
        bot.send_message(message.chat.id, 'Здравствуйте!')
        bot.send_message(message.chat.id, 'Для получения необходимой информации используйте клавиатуру.',reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def name(message):
    global camera_running
    global process

    itr = message.chat.id
    if itr in admins:
        if message.text == 'Прошедшие сотрудники':
            names = fo.get_current_names()
            outstring = 'Все прошедшие сотрудники:\n'

            for name in names:
                outstring = outstring + name + '\n'
            bot.send_message(message.chat.id, outstring)

        elif message.text == 'Узнать по фамилии':
            bot.send_message(message.chat.id, 'Введите фамилию сотрудника через спец символ ?, например: \n?Смольянинова\n')
        elif message.text[0] == '?':
            name = message.text;
            name = name.replace('?','')
            names = fo.get_current_names()
            if name in names:
                bot.send_message(message.chat.id, 'Сотрудник '+name+' на месте!')
            else:
                bot.send_message(message.chat.id, 'Сотрудника '+name+' нет!')
        elif 'Добавить' == message.text:
            bot.send_message(message.chat.id, 'Чтобы добавить, начни писать с +, например: +Марков 1 1\n Не забывай, первая цифра - логи\n Вторая видео')
        elif message.text[0] == '+':
            name = message.text;
            name = name.replace('+','')
            parts = [i for i in name.split()]

            # Terminate camera handling
            process.terminate()
            print('[INFO] >Camera handler subproccess terminating for a while...')
            print('>>>>>> Face detection inactive')

            try:
                fo.add_face(parts[0],int(parts[1]),int(parts[2]))
            except IndexError:
                fo.add_face(parts[0],1,0)
            bot.send_message(message.chat.id, 'succesfull')

            # Back to camera handling
            print('[INFO] Camera handler subproccess is running...')
            print('>>>>>> Face detection active')
            process = subprocess.Popen(['python','camera_handler.py'])
            camera_running = True

        elif 'Удалить' == message.text:
            bot.send_message(message.chat.id, 'Чтобы удалить, начни писать с -, например: -Марков')
        elif message.text[0] == '-':
            name = message.text;
            name = name.replace('-','')

            # Terminate camera handling
            process.terminate()
            print('[INFO] >Camera handler subproccess terminating for a while...')
            print('>>>>>> Face detection inactive')

            res, _ = fo.del_face(name)

            # Back to camera handling
            print('[INFO] Camera handler subproccess is running...')
            print('>>>>>> Face detection active')
            process = subprocess.Popen(['python','camera_handler.py'])
            camera_running = True

            if res:
                bot.send_message(message.chat.id, '\''+name+'\' успешно удалено!')
            else:
                bot.send_message(message.chat.id, '\''+name+'\' не найдено.')

        elif 'База сотрудников' == message.text:
            lnames = fo.get_names()
            outstring = ''

            for i in lnames:
                outstring = outstring + i + '\n'
            if outstring == '':
                outstring = 'Empty'
            bot.send_message(message.chat.id, outstring)
        else:
            bot.send_message(message.chat.id, 'Такой команды нет')

    else:
        if message.text == 'Прошедшие сотрудники':
            names = fo.get_current_names()
            outstring = 'Все прошедшие сотрудники:\n'

            for name in names:
                outstring = outstring + name + '\n'
            bot.send_message(message.chat.id, outstring)
        elif message.text == 'Узнать по фамилии':
            bot.send_message(message.chat.id, 'Введите фамилию сотрудника через спец символ ?, например: \n?Смольянинова\n')
        elif(message.text[0] == '?'):
            name = message.text;
            name = name.replace('?','')
            names = fo.get_current_names()
            if name in names:
                bot.send_message(message.chat.id, 'Сотрудник '+name+' на месте!')
            else:
                bot.send_message(message.chat.id, 'Сотрудника '+name+' нет!')
        else:
            bot.send_message(message.chat.id, 'Такой команды нет')

if __name__ == "__main__":
    bot.polling()
