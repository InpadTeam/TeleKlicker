import os
import glob
import pickle
import random
import config
from user import User
		
def get_fname(uid):
	return config.USERS_PATH + '/{0}.usr'.format(uid)

def save_user(usr):
	if usr is None:
		return
		
	with open(get_fname(usr.uid), 'wb') as outfile:
		pickle.dump(usr, outfile)

def new_user(uid, reply, nickname=None):
	usr = get_user(uid)

	if usr is None:
		usr = User(uid)
		if nickname is not None:
			usr.nickname = nickname
		usr.start(reply)
	else:
		usr.nickname = nickname
		usr.start(reply)

	save_user(usr)

def get_telegram_users():
	for f in glob.glob(config.USERS_PATH + '/*.usr'):
		uid = os.path.basename(f)[:-4]

		if not uid.startswith('vk'):
			yield uid

def delete(uid):
	if os.path.exists(get_fname(uid)):
		os.remove(get_fname(uid))

def get_user(uid):
	if os.path.exists(get_fname(uid)):
		usr = None

		with open(get_fname(uid), 'rb') as outfile:
			usr = pickle.load(outfile)

		return usr
	else:
		return None

def message(uid, reply, text):
	usr = get_user(uid)

	if not usr:
		reply('Что-то пошло не так. Попробуй /start')
	else:
		usr.message(reply, text)
		save_user(usr)

def newparty(uid, reply):
	usr = get_user(uid)

	if not usr:
		reply('Что-то пошло не так. Попробуй /start')
	else:
		usr.newparty(reply)
		save_user(usr)

def leave(uid, reply):
	usr = get_user(uid)

	if not usr:
		reply('Что-то пошло не так. Попробуй /start')
	else:
		usr.leave(reply)
		save_user(usr)

def click(uid, reply):
	usr = get_user(uid)

	if not usr:
		reply('Что-то пошло не так. Попробуй /start')
	else:
		usr.click(reply)
		save_user(usr)

def leaderboard(uid, reply, lb):
	usr = get_user(uid)

	if not usr:
		reply('Что-то пошло не так. Попробуй /start')
	else:
		usr.show_leaderboard(reply, lb)
		save_user(usr)

def debug_info(uid):
	usr = get_user(uid)

	if not usr:
		return 'Что-то пошло не так. Попробуй /start'
	else:
		return usr.debug_info()
