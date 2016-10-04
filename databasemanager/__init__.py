from pymongo import MongoClient
from databasemanager.party_model import get_model as get_parties_model
from databasemanager.leaderboard_model import get_model as get_leaderboard_model

client = MongoClient()
db = client['klicker']

Leaderboards = get_leaderboard_model(db)
Parties = get_parties_model(db)

POINTS_TABLE = 'points'

def add_to_leaderboard(user, leaderboard_name='users'):
	Leaderboards.add_to_leaderboard(user, leaderboard_name)

def get_leaderboard(leaderboard_name='users', count=20):
	return Leaderboards.get_leaderboard(leaderboard_name, count)

def get_party(party_code):
	return Parties.get_party(party_code)

def set_party(party_code, party):
	Parties.set_party(party_code, party)
