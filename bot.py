import json

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import start, get_section, unknown

with open('config.json', encoding='utf-8') as config_file:
    config_data = json.loads(config_file.read())

telegram_bot_token = config_data.get('TELEGRAM_BOT_TOKEN')
if telegram_bot_token is None:
    print("Set telegram bot token in 'config.json' file")
    exit(1)

bot_updater = Updater(token=telegram_bot_token)

dispatcher = bot_updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('get_s', get_section, pass_args=True))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))

if __name__ == '__main__':
    bot_updater.start_polling()
