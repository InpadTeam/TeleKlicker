import pymongo

from bson.code import Code

from collections import Counter

from mongothon import Schema
from mongothon import create_model
from mongothon.validators import one_of

USERS_TABLE = 'users'
PARTIES_TABLE = 'parties'

TABLES = [ PARTIES_TABLE, USERS_TABLE ]

score_schema = Schema({
		'uid': { 'type': str },
		'code_name': {'type': str },
		'score': {'type': object, 'required': True},
		'leaderboard': {'type': str, 'validates': one_of(*TABLES)}
	})

def get_model(db):
	Scores = create_model(score_schema, db['scores'])

	@Scores.class_method
	def get_leaderboard(cls, leaderboard, count=10):
		def sort_by_score(doc):
			return doc['score']

		cursor = cls.find({"leaderboard": leaderboard})
		sorted = cursor.sort('score', pymongo.DESCENDING)
		res = list(sorted.limit(count))

		return res[:count]

	@Scores.class_method
	def add_to_leaderboard(cls, item, leaderboard_name='users'):
		if leaderboard_name == USERS_TABLE:
			doc = {
				'uid': item.uid,
				'score': item.points,
				'leaderboard': USERS_TABLE,
			}
			try:
				old_record = cls.find_one({'uid': ittem.uid})
				old_record.update(doc)
				old_record.save()
			except:
				new_record = Scores(doc)
				new_record.save()
		else:
			doc = {
				'code_name': item['code_name'],
				'score': item['points'],
				'leaderboard': PARTIES_TABLE,
			}
			try:
				old_prty = cls.find_one({'code_name': item['code_name']})
				old_prty.update(doc)
				old_prty.save()
			except:
				new_score = Scores(doc)
				new_score.save()

	return Scores
