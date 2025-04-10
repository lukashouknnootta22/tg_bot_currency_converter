import telebot
from converter import ClientCurrency
import json

with open("config.json", "r") as file:
	config = json.load(file)
	token = config["TOKEN"]
	api_key = config["API_KEY"]

bot = telebot.TeleBot(token)
client = ClientCurrency(api_key)


class APIException(Exception):
	
	def __init__(self, text: str = "User error"):
		self.text = text

class Commands():

	@staticmethod
	def send_help(message):
		bot.delete_message(message.chat.id, message.message_id)
		text = ("This telegram bot is used to convert currencies in real time, using freecurrencyapi-python.\n\n"
		"To see the list of currencies available for conversion, click the 'Currencies' button or the command - /values\n\n"
		"Request format: <name of the currency whose price you want to know> <name of the currency in which you want to know the price of the first currency> <amount of the first currency>.")
		bot.send_message(message.chat.id, text=text)

	@staticmethod
	def send_values(message):
		bot.delete_message(message.chat.id, message.message_id)
		text = f"List of available currencies for conversion:\n\n{client.get_values()}"
		bot.send_message(message.chat.id, text=text)

@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message):

	markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(telebot.types.KeyboardButton("Help"))
	markup.add(telebot.types.KeyboardButton("Currencies"))

	bot.delete_message(message.chat.id, message.message_id)
	bot.send_message(message.chat.id, text="Welcome to the telegram bot for currency conversion.", reply_markup=markup)

@bot.message_handler(commands=["help"])
def command_help(message: telebot.types.Message):
	Commands.send_help(message)

@bot.message_handler(func=lambda message: message.text == "Help")
def button_help(message: telebot.types.Message):
	Commands.send_help(message)

@bot.message_handler(commands=["values"])
def command_values(message: telebot.types.Message):
	Commands.send_values(message)

@bot.message_handler(func=lambda message: message.text == "Currencies")
def button_currencies(message: telebot.types.Message):
	Commands.send_values(message)

@bot.message_handler(content_types=["text", ])
def currency_conversion(message: telebot.types.Message):
	try:
		values = message.text.split(" ")
		if len(values) != 3:
			raise(APIException("Please enter exactly three parameters: source currency, target currency, and amount."))
		source, target, amount = values
		awalaible_currencies = client.get_values().split(" ")

		if source not in awalaible_currencies:
			raise APIException(f"Problem with {f_value}. Please enter the currency code correctly")

		if target not in awalaible_currencies:
			raise APIException(f"Problem with {s_value}. Please enter the currency code correctly")

		amount = float(amount)
				
	except APIException as e:
		bot.send_message(message.chat.id, text=e.text)

	else:
		rate = client.get_exchange_currency_rates(source, target)
		bot.send_message(message.chat.id, text=f"The current {amount} {source} to {target} exchange rate is - {rate * amount}")
	
bot.polling()