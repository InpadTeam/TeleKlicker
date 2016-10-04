import databasemanager

def get_party(party_code):
	return databasemanager.get_party(str(party_code))

def create_party(owner, text):
	prt_id = str(owner.uid)

	if owner.nickname is None:
		return (False, 'Party creator must have a telegram username!')

	party = get_party(owner.uid)
	if party is not None:
		return (False, 'You already have party!\n\nTo join it:\n```/join___{0}```'.format(prt_id))

	party = {
		'name': text,
		'leader': owner.nickname,
		'slogan': 'We are the Best!',
		'points': 0.0,
		'code_name': prt_id 
	}

	databasemanager.set_party(prt_id, party)
	owner.party = prt_id

	return (True, 'You created your own awesome party!')

def click(party_code, cnt=1):
	party = get_party(party_code)
	party['points'] += cnt

	databasemanager.add_to_leaderboard(party, 'parties')

	databasemanager.set_party(str(party_code), party)

	return party['points']

def get_party_name(party_code):
	return get_party(party_code)['name']

def get_party_points(party_code):
	return get_party(party_code)['points'] 

def get_party_leader(party_code):
	return get_party(party_code)['leader']

def get_party_slogan(party_code):
	return get_party(party_code)['slogan']
