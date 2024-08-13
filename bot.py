
import json
from telegram.ext import Updater, CommandHandler, Dispatcher
import os
from pytz import timezone
import datetime
from dotenv import load_dotenv
import urllib3
from scraper import get_average_value
from scheduler import start_scheduler

load_dotenv()

PORT = int(os.environ.get('PORT', 5000))

TOKEN = os.getenv('BOTAPITOKEN')
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# url = os.getenv('APIURL')
# access_token = os.getenv("APITOKEN")
# http = urllib3.PoolManager()
# r = http.request('GET', url)
# parse_json = json.loads(r.data.decode('utf-8'))

# response = requests.get(url)
# data = response.text
# parse_json = json.loads(data)
# rate = parse_json["data"]["NGN"]["value"]
# float_rate1 = float(rate)
# float_rate = "{:.2F}".format(float_rate1)
# float_rate2 =  round(float_rate1, 2)
# float_rate = float_rate2 - 20


import time

def get_saved_value():
    try:
        with open('/tmp/average_value.json', 'r') as f:
            data = json.load(f)
            if time.time() - data['timestamp'] < 4 * 3600:  # 4 hours
                return data['average']
    except FileNotFoundError:
        pass
    return None


def help(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='/start - Start bot\n' +
        '/help - Show currency list\n' +
        '\n' +
        '/usd - Get current Dollar (USD) rate\n' +
        '/ngnusd - Convert Naira (NGN) to Dollar (USD). Example /ngnusd 1000  \n ' +
        '/usdngn - Convert Dollar (USD) to Naira (NGN). Example /usdngn 10 \n' +
        'For enquiries contact @HaleemG\n'
    )


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello, welcome to dollar to naira rates bot \n "
        'Use /help to show commands list'
    )

def get_usd2(update, context):
    average_value = get_saved_value()
    if average_value is None:
        average_value = get_average_value()
    nigeria_time = timezone('Africa/Lagos')
    dt = datetime.datetime.now( nigeria_time)
    dt_string = dt.strftime("%A, %d-%m-%Y  • %H:%M:%S")
    note = '\U0001f4b5'
    cleaned_rate = '{}\n\t\t\t\t\t\t\t USD-NGN \n\t\t\t\t\t\t\t {} 1 USD => ₦{:.2f}'.format(dt_string, note, average_value)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=cleaned_rate )
    
# def get_usd(update, context):
#     symbol = parse_json['data']['NGN']['code']
#     # hr_high = parse_json["highPrice"]
#     # hr_low = parse_json["lowPrice"]
#     # float_hr_h = float(hr_high)
#     # float_hr_low = float(hr_low)
#     nigeria_time = timezone('Africa/Lagos')
#     #datetime object
#     dt = datetime.datetime.now( nigeria_time)
#     dt_string = dt.strftime("%A, %d-%m-%Y  • %H:%M:%S")
#     print("Current date and time =", dt_string)
#     note = '\U0001f4b5'
#     cleaned_rate = '{}\n\t\t\t\t\t\t\t USD-NGN | {}\n\t\t\t\t\t\t\t {} 1 USD => ₦{:.2f}'.format(dt_string,symbol, note, float_rate)
#     # cleaner_rate = "{}\n\t\t\t\t\t\t\tUSD-NGN | {}\n\t\t\t\t\t\t\tPRICE: ₦{:.2f}\n\t\t\t\t\t\t\t24hr H: ₦{:.2f}\n\t\t\t\t\t\t\t24hr L: ₦{:.2f}\n".format(dt_string,
#     #     symbol, float_rate, float_hr_h, float_hr_low)
#     context.bot.send_message(
#         chat_id=update.effective_chat.id, text=cleaned_rate )


def ngnusdd(update, context):
    # response = requests.get(
    #     'https://api.binance.com/api/v3/ticker/24hr?symbol=USDTNGN')
    # data = response.text
    # parse_json = json.loads(data)
    # rate = parse_json['lastPrice']
    # float_rate = float(rate)

    real = update.message.text.replace('/ngnusd', '')
    real = real.replace(',', '.')
    average_value = get_saved_value()
    if average_value is None:
        average_value = get_average_value()

    real = float(real)
    convert = real/average_value

    update.message.reply_text('₦{} is ${:.3f}' .format(real, convert))


def usdngnn(update, context):
    # response = requests.get(
    #     'https://api.binance.com/api/v3/ticker/24hr?symbol=USDTNGN')
    # data = response.text
    # parse_json = json.loads(data)
    # rate = parse_json['lastPrice']
    # float_rate = float(rate)
    real = update.message.text.replace('/usdngn', '')
    real = real.replace(',', '.')

    real = float(real)
    average_value = get_saved_value()
    if average_value is None:
        average_value = get_average_value()
    convert = real*average_value

    update.message.reply_text('${} is ₦{:.2f}' .format(real, convert))


def convert(update, context):
    input = update.message.text
    input = input.replace("/convert ", "")
    input = str(input).lower()
    inputList = input.split()
    number_to_conv = inputList[0]
    number_to_conv2 = float(number_to_conv)

    name1 = str(inputList[1]).upper()
    name2 = str(inputList[2]).upper()
    name3 = name1.lower()
    name4 = name2.lower()

    if name4 == 'usd':
        update.message.reply_text(ngnusdd(
            number_to_conv2))
    elif name4 == 'ngn':
        update.message.reply_text(usdngnn(
            number_to_conv2))



# def get_dispatcher(bot):
#     dispatcher = Dispatcher(bot, None, workers=0)
#     dispatcher.add_handler(CommandHandler("start", start, run_async=True))
#     dispatcher.add_handler(CommandHandler('help', help, run_async=True))
#     dispatcher.add_handler(CommandHandler("usd", get_usd2, run_async=True))
#     dispatcher.add_handler(CommandHandler("convert", convert, run_async=True))
#     dispatcher.add_handler(CommandHandler("ngnusd", ngnusdd, run_async=True))
#     dispatcher.add_handler(CommandHandler("usdngn", usdngnn, run_async=True))
#     return dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler("usd", get_usd2)) 
dispatcher.add_handler(CommandHandler('ngnusd' , ngnusdd))
dispatcher.add_handler(CommandHandler('usdngn', usdngnn))

if __name__ == '__main__':
    start_scheduler()
    updater.start_polling()
    print("Bot is running. Press Ctrl+C to stop.")
    updater.idle()