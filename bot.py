
import json
from telegram.ext import Updater, CommandHandler, Dispatcher
import os
from pytz import timezone
import datetime
from dotenv import load_dotenv
import urllib3
load_dotenv()

PORT = int(os.environ.get('PORT', 443))
TOKEN = os.getenv('BOTAPITOKEN')
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

url = os.getenv('APIURL')
access_token = os.getenv("APITOKEN")
http = urllib3.PoolManager()
r = http.request('GET', url)
parse_json = json.loads(r.data.decode('utf-8'))

# response = requests.get(url)
# data = response.text
# parse_json = json.loads(data)
rate = parse_json["lastPrice"]
float_rate = float(rate)


# def help(update, context):
#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text='/start - Start bot\n' +
#         '/help - Show currency list\n' +
#         '\n' +
#         '/usd - Get current Dollar (USD) rate\n' +
#         '/convert - Convert Naira (NGN) to Dollar (USD) or Dollar (USD) to Naira (NGN)\n ' +
#         'Example - /convert 1000 usd ngn OR /convert 1000 ngn usd \n ' +
#         'For enquiries contact @HaleemG\n'
#     )
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


def get_usd(update, context):
    symbol = parse_json['symbol']
    hr_high = parse_json["highPrice"]
    hr_low = parse_json["lowPrice"]
    float_hr_h = float(hr_high)
    float_hr_low = float(hr_low)
    nigeria_time = timezone('Africa/Lagos')
    #datetime object
    dt = datetime.datetime.now( nigeria_time)
    dt_string = dt.strftime("Date: %A %d/%m/%Y  time: %H:%M:%S")
    print("Current date and time =", dt_string)
    
    cleaner_rate = "{}\n\t\t\t\t\t\t\tUSD-NGN | {}\n\t\t\t\t\t\t\tPRICE: ₦{:.2f}\n\t\t\t\t\t\t\t24hr H: ₦{:.2f}\n\t\t\t\t\t\t\t24hr L: ₦{:.2f}\n".format(dt_string,
        symbol, float_rate, float_hr_h, float_hr_low)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=cleaner_rate)


def ngnusd(real):

    real = float(real)
    convert = real/float_rate
    rate = '₦{:,} is ${:,.3f}' .format(real, convert)
    return rate


def usdngn(real):

    real = float(real)
    convert = real*float_rate

    rate = ('${:,} is ₦{:,.2f}' .format(real, convert))
    return rate


def ngnusdd(update, context):
    # response = requests.get(
    #     'https://api.binance.com/api/v3/ticker/24hr?symbol=USDTNGN')
    # data = response.text
    # parse_json = json.loads(data)
    # rate = parse_json['lastPrice']
    # float_rate = float(rate)
    real = update.message.text.replace('/ngnusd', '')
    real = real.replace(',', '.')

    real = float(real)
    convert = real/float_rate

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
    convert = real*float_rate

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
        update.message.reply_text(ngnusd(
            number_to_conv2))
    elif name4 == 'ngn':
        update.message.reply_text(usdngn(
            number_to_conv2))


def get_dispatcher(bot):
    """Create and return dispatcher instances"""
    dispatcher = Dispatcher(bot, None, workers=0)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler("usd", get_usd))
    dispatcher.add_handler(CommandHandler("convert", convert))
    dispatcher.add_handler(CommandHandler("ngnusd", ngnusdd))
    dispatcher.add_handler(CommandHandler("usdngn", usdngnn))
    return dispatcher
# updater.start_polling()
# updater.idle()


# updater.start_webhook(listen="0.0.0.0",
#                           port=int(PORT),
#                           url_path=TOKEN)
# updater.bot.setWebhook('http://localhost:3000' + TOKEN)
