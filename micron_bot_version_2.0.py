from flask import Flask, request
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup



#Начало для сервер
host = '7416ae1d8072.ngrok.io'
bot = telebot.TeleBot('1880721297:AAHg5RoKgNK6jgim7H3nieu-JB89LdH_NO8')
bot.set_webhook(url=host)
app = Flask(__name__)


@app.route('/', methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok"
#Конец для сервера

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id,
		'Дарова, я тут бота запилил, заценишь?',
		reply_markup = keyboard())

@bot.message_handler(content_types=['text'])
def change(message):
	global id_pars
	if message.text == masscom[0]:
		id_pars = 'section_id=93&q='
		bot.send_message(message.chat.id,lettermodel,reply_markup = keyboard_cancel())
		bot.register_next_step_handler(message, answer)
	elif message.text == masscom[1]:
		id_pars = 'section_id=95&q='
		bot.send_message(message.chat.id,lettermodel, reply_markup = keyboard_cancel())
		bot.register_next_step_handler(message, answer)
	elif message.text == masscom[2]:
		id_pars = '&q=защитное+стекло+'
		bot.send_message(message.chat.id,lettermodel,reply_markup = keyboard_cancel())
		bot.register_next_step_handler(message, answer)
	elif message.text == masscom[3]:
		bot.send_message(message.chat.id, '1. Модель можно узнать в настройках телефона, для этого зайдите в настройки и найди раздел "Об устройстве" \n 2.Если в настройки зайти нет возможности, осмотрите заднюю крышку телефона на наличие модели \n 3. Приходите в наш сервис по адресу Ватутина 27, вход с фасада здания, мы сами определим модель',reply_markup = keyboard())
	elif message.text == masscom[4]:
		bot.send_message(message.chat.id,'Напишите свои улучшения по работе бота')
		bot.register_next_step_handler(message, record)
	elif message.text == masscom[5]:
		bot.send_message(message.chat.id,letterhelp)
	else:
		bot.send_message(message.chat.id, 'Упс, возможно вы случайно. Я в это верю...')

def check_correct(message):
	findtex = -1
	for i in dictname:
			if i.lower().find(message.text.lower()) >= 0:
				findtex += 2
	return findtex


def help_model(message):
	bot.send_message(message.chat.id, '1. Модель можно узнать в настройках телефона, для этого зайдите в настройки и найди раздел "Об устройстве" \n 2.Если в настройки зайти нет возможности, осмотрите заднюю крышку телефона на наличие модели \n 3. Приходите в наш сервис по адресу Ватутина 27, вход с фасада здания, мы сами определим модель')

def keyboard():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
	btn1 = types.KeyboardButton(masscom[0])
	btn2 = types.KeyboardButton(masscom[1])
	btn3 = types.KeyboardButton(masscom[2])
	btn4 = types.KeyboardButton(masscom[3])
	btn5 = types.KeyboardButton(masscom[4])
	btn6 = types.KeyboardButton(masscom[5])
	markup.add(btn1)
	markup.add(btn2)
	markup.add(btn3)
	markup.add(btn4)
	markup.add(btn5)
	markup.add(btn6)
	return markup

def keyboard_cancel():
	markup_cancel = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
	button =  types.KeyboardButton(masscom[6])
	markup_cancel.add(button)
	return markup_cancel

def send_telegram(text: str):
    token = "1880721297:AAHg5RoKgNK6jgim7H3nieu-JB89LdH_NO8"
    url = "https://api.telegram.org/bot"
    channel_id = "@testbot_mic"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")

def Parcer(url):
	dictname = dict()
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')
	name = soup.find_all('a', class_="dark_link")
	price = soup.find_all('span', class_="price_value")
	for j in range(len(price)):
		for i in range(len(price)):
			dictname[name[i].text] = [price[i]]	

	return dictname 



def answer(message):
	global new_url
	timer = 0 # Обнуление переменных 
	model = '' # Обнуление переменных 
	info = '' # Обнуление переменных 
	counter = 1
	if message.text == 'Отмена':
		bot.send_message(message.chat.id,'Выберите команду',reply_markup = keyboard())
	elif message.text == masscom[3]:
		help_model(message)
		bot.send_message(message.chat.id,'Введите модель телефона или нажмите отмена',reply_markup = keyboard_cancel())
		bot.register_next_step_handler(message,answer)
	else:
		for i in range(len(masscom)):
			if message.text == masscom[i]:
				timer += 1
		if timer > 0:
			bot.send_message(message.chat.id, 'Это не модель телефона\n\nКнопки для обращения к боту не являются моделью телефона,если вы не знаете модель телефона,выберите функцию "Справка о модели телефона"\n\n Введите пожалуйста корректную модель телефона или нажмите отмена',reply_markup = keyboard_cancel())
			bot.register_next_step_handler(message, answer)
		else:
			for i in range(len(message.text)):
				if message.text[i] == ' ':
					model += '+'
				else: 
					model += message.text[i]
			new_url = def_url + id_pars + model + '&how=r'
			global dictname
			dictname = Parcer(new_url)
			findtext = check_correct(message)
			if dictname == {} or findtext == -1:
				bot.send_message(message.chat.id, 'Извините, но такой запчасти на данную модель нет,проверьте корректность введёных данных и попробуйте снова,либо же нажмите отмена',reply_markup = keyboard_cancel())
				bot.register_next_step_handler(message, answer)
			else:
				for i in dictname:
					if i.lower().find(message.text.lower()) >= 0:
						info += str(counter) + '. ' + i + '\n\n'
						counter += 1
				info += 'Отправьте в чат номер запчасти, цену на замену которой вы бы хотели узнать либо нажмите отмена'
				bot.send_message(message.chat.id, info, reply_markup = keyboard_cancel())
				bot.register_next_step_handler(message, orient_price)

def orient_price(message):
	check = 0
	if message.text != 'Отмена':
		for i in range(len(dictname)):
			if message.text == str(i + 1):
				check += 1
				break
		if check == 1:
			or_price = ['skip']
			counter = 1
			for i in dictname:
				or_price.append(i + ' (' + dictname.get(i)[0].text.replace(" ", "") + "Рублей)\n\n")
				counter += 1
			send_orientir = str(or_price[int(message.text)])
			send_telegram(send_orientir)
			bot.send_message(message.chat.id, or_price[int(message.text)] + 'Для просмотра других цен, введите цифру или нажмите отмена',reply_markup = keyboard_cancel())
			bot.register_next_step_handler(message, orient_price)
		else:
			bot.send_message(message.chat.id, "Введите корректную цифру или нажмите отмена",reply_markup = keyboard_cancel())
			bot.register_next_step_handler(message, orient_price)				
	else:
		bot.send_message(message.chat.id,'Выберите команду',reply_markup = keyboard())


def record(message):
	my_file = open("C:/Pythonprogramm/Project/Micron/idea.txt", "a")
	my_file.write(message.chat.username + ' || ' + message.text + ' |\n')
	my_file.close()
	bot.send_message(message.chat.id,"Благодарю за помощь!",reply_markup = keyboard())

if __name__ == "__main__":
	masscom = ['Дисплей','Аккумулятор','Защитное стекло','Справка о модели телефона','Ваши предложения','Справка','Отмена']
	lettermodel = 'Введите модель телефона или нажмите отмена'
	letterhelp = ' 1. Для корректной работы бота, после выбора замены желаемой запчасти вводите корректные данные модели, пример:\na50 - некорректно \nA50 - корректно\n2.При указание модели телефона можно так же указывать бренд телефона, пример:\nSamsung A50 - где Samsung является брендом\n3.Указанные цены являются ценами за замену выбранной вами запчасти,для выявление точной неисправности производиться дополнительная диагностика, в следствие которой могут быть выявлены дополнительные неисправности(как пример не работающая камера при разбитие дисплея) \n4. В предъявленную цену входит стоимость запчасти и стоимость работы(т.е. самой замены запчасти)'
	new_url = ''
	id_pars = ''
	def_url = "https://novosibirsk.moba.ru/catalog/?"
	app.run()

