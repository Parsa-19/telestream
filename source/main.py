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
        self.api_url = ''
        self.api_header = {"Authorization": "Basic cm9vdDo3ODBAYW1yMTIz"}

    def parse_xml(self, xml_node, xml_string):
        root = ET.fromstring(xml_string)
        return root.findall(xml_node)[0].text # returns value of the node

    def check_BytesInRate(self, bytesinrate): # indicates that the stream is up and working or not by 40 000
        return True if bytesinrate > 40000 else False
    
    def set_api_url(self, plus_indicator):
        plus_nums = {
            'plus': '',
            'plus2': '2',
            'plus3': '3'
        }
        requested_num = plus_nums[plus_indicator] # requested_num will be 1 or 2 or 3 according to plus_indicator
        self.api_url = f'http://185.236.36.132:8087/v2/servers/Wowza%20Streaming%20Engine/vhosts/_defaultVHost_/applications/plus/instances/_definst_/incomingstreams/plus{requested_num}.stream/monitoring/current'

    def request_api(self):
        return requests.get(self.api_url, headers=self.api_header)

    def extract_bytesIn_from_xml_response(self, response):
        bytesIn = self.parse_xml('BytesIn', response.text)
        bytesIn = int(bytesIn)
        is_streaming = self.check_BytesInRate(bytesIn)
        return (is_streaming, bytesIn)






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
[plus, plus2, plus3].
click on the plus you need to see if it is working or not.
[ asnwer is wheather True/False ]
        ''', reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('start the bot.. \nclick the button to see if its running a stream by True or stream is not working by False.')


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    plus = StreamPlus()
    plus.set_api_url(query.data) # query.data is one of [plus, plus2, plus3]
    response = plus.request_api()
    stream_info = plus.extract_bytesIn_from_xml_response(response)
    
    is_streaming = stream_info[0]
    bytesIn = stream_info[1]
    
    final_answer = f'''{query.data} running stream = {is_streaming} \nAPI response bytesIn = {bytesIn}'''
    await query.edit_message_text(text=final_answer)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update}\n\n----------\n cause error:\n {context.error}')





if __name__ == '__main__':
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



    # # functionality test
    # plus = StreamPlus()
    # plus.set_api_url('plus')
    # response = plus.request_api()
    # stream_info = plus.extract_bytesIn_from_xml_response(response)



