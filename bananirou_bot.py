from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN : Final = '6761280751:AAH-vaukYzkAnFsXOzNToeXFa0SDY2wID_g'
BOT_USERNAME : Final = '@bananirou_bot'

#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Hola! Como estas?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Por favor elegi un comando')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Hola! Como estas?')

#Responses

def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    if 'Hello' in processed:
        return 'Todo bien'
    
    if 'Como estas' in processed:
        return 'Todo bien'
    
    if 'me encanta python' in processed:
        return 'Mortal compa, bien ahi'
    
    return 'No te entendi. Disculpa, no soy de por aca'

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
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    
    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    
    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    #Error 
    app.add_error_handler(error)
    
    #polls the bot
    print('Polling...')
    app.run_polling(poll_interval = 3)