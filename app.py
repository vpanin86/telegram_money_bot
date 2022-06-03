import telebot
from database import keys
from token_for_bot import TOKEN
from extensions import APIException, MoneyConverter

bot = telebot.TeleBot(TOKEN)

#вывод приветственного сообщения
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

#вывод доступного списка валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message,text)

#вывод курса валют
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    try: #проверка количества аргументов ввода пользователя
        values = message.text.split(' ')
        if len(values) > 3:
            raise APIException('Слишком много параметров/')
        elif len(values) < 3:
            raise APIException('Слишком мало параметров/')
        quote, base, amount = values #конвертируемая валюта, валюта в единицах которой конвертируют, количество
        total_base = MoneyConverter.get_price(quote, base, amount)
        total_base = total_base * float(amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling() #запуск бота
