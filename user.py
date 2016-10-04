import databasemanager
import partymanager
import usermanager

def check(text):
	printable = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')

	return len(''.join(filter(lambda x: x in printable, text))) == len(text)

class User(object):
	def __init__(self, uid, nickname=None):
		super().__init__()
		self.uid = uid
		self.party = None
		self.nickname = nickname

		self.points = 0

		self.name = '№' + str(uid).replace('-', '9')
		self.state = 'start'

	def get_buttons(self):
		res = [ ('Click!', 'click') ]

		if self.party is None:
			res.append( ('Create party', 'create'))
			res.append( ('Leaderboard', 'leaderboard_users') )
		else:
			res.append( ('Leave party', 'leave'))
			res.append( ('Leaderboard', 'leaderboard_parties') )

		return res

	def leave(self, reply):
		self.party = None

		self.start(reply)
		
	def start(self, reply):
		self.state = 'start'

		msg = 'Hello, {0}!\n\n'.format(self.name)

		if self.party:
			party = partymanager.get_party(self.party)

			party_name = party['name']
			points = party['points']

			party_leader = party['leader']
			party_leader_says = party['slogan']


			msg += 'You assigned to _{0}_ party. It has *{1}* points.\n'.format(party_name, points)
			msg += 'Your party leader @{0} says:\n{1}'.format(party_leader, party_leader_says)

			if str(party_leader) == str(self.nickname):
				msg += '\n\n To join your party user has to enter thoose sentence:\n'
				msg += '```/join___{0}```'.format(party['code_name'])

		else:
			msg += 'You work on yourself. You have *{0}* points!'.format(self.points)

		reply(msg, self.get_buttons())

	def debug_info(self):
		msg = 'uid: ' + str(self.uid) + '\n'
		msg += 'party: ' + str(self.party) + '\n'
		msg += 'nickname: ' + str(self.nickname) + '\n'
		msg += 'points: ' + str(self.points) + '\n'
		msg += 'name: ' + str(self.name) + '\n'

		return msg

	def click(self, reply):
		if self.party:
			points = partymanager.click(self.party)

			reply('Now your party has {0} points!'.format(points), self.get_buttons())
		else:
			self.points += 1

			databasemanager.add_to_leaderboard(self)

			reply('Now you have {0} points!'.format(self.points), self.get_buttons())

	def show_leaderboard(self, reply, name):
		scores = databasemanager.get_leaderboard(name)

		msg = 'First 20 records:\n'

		for i, sc in enumerate(scores):
			if name == 'parties':
				recrd = '{0}. {1}: {3}\n@{2} says: {4}\n'
				party = partymanager.get_party(sc['code_name'])

				msg += recrd.format(i+1, party['name'], party['leader'], party['points'], party['slogan'])
			else:
				usr = usermanager.get_user(sc['uid'])

				if usr.nickname is not None:
					recrd = '{0}. {1} (@{2}): {3}\n'
					msg += recrd.format(i+1, usr.name, usr.nickname, usr.points)
				else:
					recrd = '{0}. {1}: {2}\n'
					msg += recrd.format(i+1, usr.name, usr.points)

		reply(msg, self.get_buttons())


	def newparty(self, reply, text=None):
		if text == None:
			reply('Write the name of the party e. g. Suppa Duppa Party')
			self.state = 'newparty'
		else:
			if check(text):
				res, msg = partymanager.create_party(self, text)

				reply(msg)

				if res:
					self.start(reply)
			else:
				reply('Party name shold contain *only* Latin letters, numbers and space')

	def setname(self, reply, text=None):
		if text is None:
			reply('Write your new name.')
			self.state = 'setname'
		else:
			if check(text) and len(text) > 3 and len(text) < 15:
				self.name = text
				self.start(reply)
			else:
				reply('Unsupported name :(')

	def sayparty(self, reply, text=None):
		if text is None:
			if str(self.party) == str(self.uid):
				reply('What your fiends will see?')
				self.state = 'sayparty'
			else:
				reply('You aren\'t party leader!')
		else:
			if len(text) > 0 and len(text) < 140:
				party = partymanager.get_party(self.party)
				party['slogan'] = text
				databasemanager.set_party(self.party, party)

				self.start(reply)
			else:
				reply('Unsupported text :(')

	def setpartyname(self, reply, text=None):
		if text is None:
			if self.party:
				reply('Write your new party name.')
				self.state = 'setpartyname'
			else:
				reply('You have no party!')
		else:
			if check(text):
				party = partymanager.get_party(self.party)
				party['name'] = text
				databasemanager.set_party(self.party, party)

				self.start(reply)
			else:
				reply('Unsupported name :(')

	def message(self, reply, text):
		if self.state == 'newparty':
			self.newparty(reply, text)
		if self.state == 'setname':
			self.setname(reply, text)
		if self.state == 'setpartyname':
			self.setpartyname(reply, text)
		if self.state == 'sayparty':
			self.sayparty(reply, text)
		elif text.startswith('/join___'):
			party_code = text[len('/join___'):]

			party = partymanager.get_party(party_code)

			if party is None:
				reply('No such party, dude.')
			else:
				self.party = party['code_name']
				reply('You joined _{0}_ party! Be the @{1} with you'.format(party['name'], party['leader']))
				self.start(reply)
		else:
			self.start(reply)