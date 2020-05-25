import logging
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import API_KEY


logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

planets = {name : f'ephem.{name}()' for _0, _1, name in ephem._libastro.builtin_planets()}

def greet_user(update, context):
    print('Start is calling')
    update.message.reply_text('Who summons me')

def talk_to_me(update, context):
    print(f'Message:  {update.message.text}')
    update.message.reply_text(update.message.text)

def constellation(update, context):
    planet = update.message.text.split(' ')[1].lower().capitalize()
    print(planet)
    if planet in planets:
        planet = eval(planets[planet])
        planet.compute()
        const = ephem.constellation(planet)
        update.message.reply_text(f'{planet.name} сейчас в созведии {const}')
    else:
        update.message.reply_text('Я такой планеты не знаю.')


def main():
    mybot = Updater(API_KEY,use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start',greet_user))
    dp.add_handler(CommandHandler('planet',constellation))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Bot is started!')

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()