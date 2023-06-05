import telebot
from telebot import types
from glob import glob as glob
import PyPDF2

API_Token = "5934104027:AAFTabSWA4zS1Wqm7xqMgVWBGeQaJ3SSqAM"
bot = telebot.TeleBot(API_Token)

base_path = "D:\Desktop\Программы Питон\поиск файлов бот\data"
paths = glob(base_path + '/*.pdf*')
pdf_list = []
for f in paths:
    pdf_list.append(PyPDF2.PdfReader(f, 'rb'))

def func1(message):
    text = message.text4
    matches = 0
    g = 0
    for i in range(len(paths)):
        if text.upper() in paths[i]:
            if text.upper() == paths[i][49:len(paths[i])-4]:
                bot.send_message(message.chat.id, text='Полное совпадение по названию:')
                bot.send_document(message.chat.id, document=open(paths[i], 'rb'))
            else:
                if g == 0: bot.send_message(message.chat.id, text = 'Пересечение по названию:')
                g = 1
                bot.send_document(message.chat.id, document = open(paths[i], 'rb'))
            matches = 1
    if matches != 1:
        bot.send_message(message.chat.id, text = 'Совпадений нет, попробуйте ещё раз!')
        bot.send_message(message.chat.id, text='Введите название файла')
        bot.register_next_step_handler(message, func1)

def func2(message):
    text = message.text
    draft_path = 'D:\Desktop\Программы Питон\поиск файлов бот\drafts'
    c = 0
    pages_list = []
    bot.send_message(message.chat.id, text = 'Обработка запроса (Это может занять время)')
    for i in range(len(pdf_list)):
        d_c = 0
        for j in range(len(pdf_list[i].pages)):
            if text in pdf_list[i].pages[j].extract_text():
                d_c = d_c + 1
                c = c + 1
                bot.send_message(message.chat.id, text = f'Совпадение № {c}')
                if d_c == 1:
                    bot.send_document(message.chat.id,document = open(paths[i], 'rb'))
                pdf_new = PyPDF2.PdfWriter()
                pdf_new.add_page(pdf_list[i].pages[j])
                comand_1 = f'''pdf_new.write('D:\Desktop\Программы Питон\поиск файлов бот\drafts\page_{c}.pdf')'''
                exec(comand_1)
                comand_2 = f'''bot.send_document(message.chat.id, document = open('D:\Desktop\Программы Питон\поиск файлов бот\drafts\page_{c}.pdf', 'rb'))'''
                exec(comand_2)
    if c == 0:
        bot.send_message(message.chat.id, text = 'Совпадений не найдено, попробуёте ещё раз')
        bot.send_message(message.chat.id, text='Введите ключевую фразу')
        bot.register_next_step_handler(message, func2)
    bot.send_message(message.chat.id, text = 'Обработка завершена')



@bot.message_handler(commands = ['start', 'help', 'back'])
def send_welcome(message):
    bot.send_message(chat_id = message.chat.id, text = 'Приветсвую! Тут должен быть велкомный текст, но этож надо придумывать. Кароче на кнопки потыкайте')
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('Поиск по названию файла')
    btn2 = types.KeyboardButton('Поиск по содержанию')
    btn3 = types.KeyboardButton('/инструкция')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,text = 'Тыкайте:',  reply_markup=markup)

@bot.message_handler(commands = ['инструкция'])
def send_instruction(message):
    video = open('D:\Desktop\Программы Питон\поиск файлов бот\data\инструкция.MP4', 'rb')
    bot.send_video(message.chat.id, video = video)
@bot.message_handler(content_types = ['text'])
def answ(message):
    if message.text == 'Поиск по названию файла':
        bot.send_message(message.chat.id, text = 'Введите название файла')
        bot.register_next_step_handler(message, func1)
    if message.text == 'Поиск по содержанию':
        bot.send_message(message.chat.id, text = 'Как это работает? Я ищу вашу ключевую фразу в своих базах данных. Если я нахожу что-то, я скидываю вам номер сопадения, файл с совпадением и страницу на которой совпадение найдено. P.S. Если я скинул только страницу - значит в файле несколько страниц с совпадениями')
        bot.send_message(message.chat.id, text = 'Введите ключевую фразу')
        bot.register_next_step_handler(message, func2)

bot.infinity_polling()