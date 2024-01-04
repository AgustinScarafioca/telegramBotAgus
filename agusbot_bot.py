from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pymongo import MongoClient
import random
import logging
import io
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN : Final = os.getenv('TOKEN')
BOT_USERNAME : Final = os.getenv('BOT_USERNAME')
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Hola! Como estas?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Por favor elegi un comando')

async def pfa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Hay olor a gorra')
        
async def edu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Edu crotooooooo')

async def thomi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Thomi pedazo de tranzaaaa')

async def mica_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Mica, no rompas nada por favor')



#Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    if 'hola' in processed:
        return 'Todo bien?'
    
    if 'como estas' in processed:
        return 'Todo bien'
    
    if 'no' in processed:
        return 'Mortal kompa, bien ahi'
    
    if 'si' in processed:
        return 'Jugo Juan Roman Tristelme'
    
    if 'me encanta python' in processed:
        return 'Mortal compa, bien ahi'
    
    return 'No te entendi. Disculpa, no soy de por aca. Capaz algun dia entienda tu idioma de crotooo'

#Messages

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text: 
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else: 
            return
    else: response: str = handle_response(text)
    
    print('Bot', response)
    await update.message.reply_text(response)


#mongo commands

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'webstorage'
MONGO_COLLECTION = 'monos'

client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]

# Command to get a random photo from MongoDB
async def santi_random_photo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get a random photo from MongoDB
    bson_data = get_random_mongo_photo()

    # Convert BSON data to a file-like object
    photo_file = io.BytesIO(bson_data)

    # Send the photo as a response
    await update.message.reply_photo(photo=photo_file, caption='Moñoooo')


def get_random_mongo_photo():
    # Use the aggregation pipeline to get a random document
    pipeline = [{'$sample': {'size': 1}}]
    random_document = collection.aggregate(pipeline).next()
    
    return random_document['data']


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    
    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('pfa', pfa_command))
    app.add_handler(CommandHandler('edu', edu_command))
    app.add_handler(CommandHandler('thomi', thomi_command))
    app.add_handler(CommandHandler('mica', mica_command))
    app.add_handler(CommandHandler('santi', santi_random_photo_command))
    
    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    #Error 
    app.add_error_handler(error)
    
    #polls the bot
    print('Polling...')
    app.run_polling(poll_interval = 3)



