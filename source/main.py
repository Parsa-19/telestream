import logging
import time

import requests
import asyncio
import json
import xml.etree.ElementTree as ET

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import *


TOKEN = '8087760670:AAFn0pzO8LsttESIZ73W_Aa26TjZGQmq088'
BOT_USERNAME = '@telePlusStreamCheckBot'

logger = logging.getLogger()
logging.basicConfig(
    filename = '../logs/log.txt',
    encoding = 'utf-8',
    level = logging.INFO
    )

class StreamPlus(object):
    
    def __init__(self):
        self.api_url = self.set_api_url('plus') # plus1 is exmaple
        self.api_header = {"Authorization": "Basic cm9vdDo3ODBAYW1yMTIz"}

    def parse_xml(self, response):
        root = ET.fromstring(response.text)
        bytesinrate = None
        
        for description in root.iter('BytesInRate'):    
            bytesinrate = description.text
    
        return bytesinrate

    def request_api(self):
        return requests.get(self.api_url, headers = self.api_header)

    def set_api_url(self, plus_indicator):
        plus_nums = {
            'plus': '',
            'plus2': '2',
            'plus3': '3'
        }
        requested_num = plus_nums[plus_indicator] # requested_num will be 1 or 2 or 3 according to plus_indicator
        self.api_url = f'http://185.236.36.132:8087/v2/servers/Wowza%20Streaming%20Engine/vhosts/_defaultVHost_/applications/plus/instances/_definst_/incomingstreams/plus{requested_num}.stream/monitoring/current' 

    def check_BytesInRate(self, bytesinrate): # indicates that the stream is up and working or not by 40 000
        return True if bytesinrate > 40000 else False

    def extract_info_from_xml_response(self, response):
        bytesinrate = self.parse_xml(response)
        is_streaming = self.check_BytesInRate(bytesinrate)
        return is_streaming






# plus = StreamPlus()
# plus.set_api_url(plus) # query.data is one of [plus1, plus2, plus3]
# response = plus.request_api()
# stream_info = plus.extract_info_from_xml_response(response)

# bot

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Plus 1", callback_data="plus"),
            InlineKeyboardButton("Plus 2", callback_data="plus2"),
        ],
        [InlineKeyboardButton("Plus 3", callback_data="plus3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('''
hey there! this is TELESTREAM_BOT!
you can check streaming nodes and their statuses for:
[plus1, plus2 and plus3].
click on the plus you need stream status for righ now.
        ''', reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('peace of a cake.. \njust start the bot whenever you need plus1-3 statuses and click on its button')


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    plus = StreamPlus()
    print(type(query.data) + '   ' + query.data)
    plus.set_api_url(query.data) # query.data is one of [plus1, plus2, plus3]
    response = plus.request_api()
    stream_info = plus.extract_info_from_xml_response(response)
    
    await query.edit_message_text(text=stream_info)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} cause error: {context.error}')




if __name__ == '__main__':
<<<<<<< HEAD
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # button
    app.add_handler(CallbackQueryHandler(button))

    # errors
    app.add_error_handler(error)

    # Run the bot until the user presses Ctrl-C
    app.run_polling(allowed_updates=Update.ALL_TYPES)
=======
	main()
>>>>>>> fab7acf198163fab3f2cc031035d941c6de91e69
