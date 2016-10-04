import config
import logging

import usermanager
import partymanager

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, InlineQueryHandler

from uuid import uuid4

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def reply(bot, message, text, markup=None, edit_id=None):
	def send(text, reply_markup=None):
		if edit_id is not None:
			bot.editMessageText(text=text,
								chat_id=message.chat_id,
								message_id=edit_id,
								reply_markup=reply_markup)
		else:
			message.reply_text(text, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)

	if markup:
		keyboard = [ [ InlineKeyboardButton(opt[0], callback_data=opt[1]) ] for opt in markup]
		reply_markup = InlineKeyboardMarkup(keyboard)

		send(text, reply_markup=reply_markup)
	else:
		send(text)

def generate_reply(bot, message, edit_id=None):
	def gen_rep(text, markup=None):
		reply(bot, message, text, markup, edit_id)

	return gen_rep

def start(bot, update):
	uid = update.message.chat_id
	nickname = None

	try:
		nickname = bot.getChat(uid)['username']
	except:
		pass
	usermanager.new_user(uid, generate_reply(bot, update.message), nickname)

def debug(bot, update):
	inf = usermanager.debug_info(update.message.chat_id)
	bot.sendMessage(update.message.chat_id, text=inf)

def button(bot, update):
	query = update.callback_query

	if query.data == 'click':
		usermanager.click(query.message.chat_id, generate_reply(bot, query.message, query.message.message_id))
	elif query.data == 'create':
		usermanager.newparty(query.message.chat_id, generate_reply(bot, query.message))
	elif query.data == 'leave':
		usermanager.leave(query.message.chat_id, generate_reply(bot, query.message, query.message.message_id))
	elif query.data.startswith('leaderboard'):
		lb = query.data.split('_')[1]
		usermanager.leaderboard(query.message.chat_id, generate_reply(bot, query.message, query.message.message_id), lb)

def newparty(bot, update):
	usermanager.newparty(update.message.chat_id, generate_reply(bot, update.message))

def setname(bot, update):
	usermanager.setname(update.message.chat_id, generate_reply(bot, update.message))

def setpartyname(bot, update):
	usermanager.setpartyname(update.message.chat_id, generate_reply(bot, update.message))

def sayparty(bot, update):
	usermanager.sayparty(update.message.chat_id, generate_reply(bot, update.message))

def share(bot, update):
	usr = usermanager.get_user(update.message.chat_id)
	party = partymanager.get_party(usr.party)

	if party is None:
		update.message.reply_text("No party for you!")
	else:
		keyboard = [ [ InlineKeyboardButton("Share!", switch_inline_query='') ] ]
		reply_markup = InlineKeyboardMarkup(keyboard)

		update.message.reply_text("Let's share our cool party!", reply_markup=reply_markup)

def inlinequery(bot, update):
	query = update.inline_query.query
	results = list()

	share_msg = 'Common and click some buttons:\n@klickertestbot'

	results.append(InlineQueryResultArticle(id=uuid4(),
											title="Share the bot",
											description='Shares our cool game to others',
											input_message_content=InputTextMessageContent(share_msg)))

	usr = usermanager.get_user(update.inline_query.from_user.id)
	party = partymanager.get_party(usr.party)

	if party is not None:
		results.append(InlineQueryResultArticle(id=uuid4(),
												title="Share the bot",
												description='Enter our party!',
												input_message_content=InputTextMessageContent('/join___' + str(party['code_name'])) ))

	update.inline_query.answer(results)

def msg(bot, update):
	usermanager.message(update.message.chat_id, generate_reply(bot, update.message), update.message.text)

def error(bot, update, error):
	logging.warning('Update "%s" caused error "%s"' % (update, error))


logging.info('1...')
# Create the Updater and pass it your bot's token.
updater = Updater(config.TOKEN)

logging.info('2...')

updater.dispatcher.add_handler(CommandHandler('setpartyname', setpartyname))
updater.dispatcher.add_handler(CommandHandler('newparty', newparty))
updater.dispatcher.add_handler(CommandHandler('sayparty', sayparty))
updater.dispatcher.add_handler(CommandHandler('setname', setname))
updater.dispatcher.add_handler(CommandHandler('share', share))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('debug', debug))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(MessageHandler(False, msg))
updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))
updater.dispatcher.add_error_handler(error)

logging.info('3...')

# Start the Bot
updater.start_polling()

# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT

logging.info('4...')

updater.idle()