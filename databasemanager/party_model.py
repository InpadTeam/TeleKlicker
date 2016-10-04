from mongothon.model import NotFoundException

from mongothon import Schema
from mongothon import create_model

party_schema = Schema({
		'name': {"type": str, "required": True},
		'leader': {"type": str, "required": True },
		'slogan': {"type": str, "required": True },
		'points': {"type": float, "required": True },
		'code_name': {"type": str, "required": True}
	})

def get_model(db):
	Parties = create_model(party_schema, db['parties'])

	@Parties.class_method
	def get_party(cls, code_name):
		try:
			return cls.find_one({'code_name': code_name})
		except:
			return None

	@Parties.class_method
	def set_party(cls, code_name, party):
		try:
			var = cls.find_one({'code_name': code_name})
			var.update(party)
			var.save()
		except:
			var = Parties(party)
			var.save()

	return Parties