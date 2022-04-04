import telebot
from extensions import keys, TOKEN
from utils import CryptoConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f"Привет, {message.chat.username}, чтобы воспользоваться нашим ботом \
введите команду в формате: имя валюты> \
<в какую валюту перевести> <количество переводимой валюты>\
Увидеть список всех возможных валют для конвертации можно введя команду /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise APIException('Неверное число параметров')
        qoute, base, amount = values
        qoute, base, amount = qoute.lower(), base.lower(), amount.lower()
        total_base = CryptoConverter.get_price(qoute, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {qoute} в {base} -  {total_base}'
        bot.send_message(message.chat.id, text)
bot.polling()
