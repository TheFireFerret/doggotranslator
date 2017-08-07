import pyrebase
import os

config = {
	  "databaseURL": os.environ['databaseURL'],
	  "apiKey": os.environ['apiKey'],
	  "authDomain": os.environ['authDomain'],
	  "storageBucket": os.environ['storageBucket']
	}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def find_word(word):
	"""
	Checks if a word exists in database
	word (string): the word to search for
	Returns the word ID if it exists, otherwise None
	"""
	try:
		all_words = db.get()
		for item in all_words.each():
			if word in item.val()["word"]:
				return item.key()
		return None
	except TypeError:
		return None

def add_links(word_id, translation_id):
	# check if a link exists before adding it, for both ways
	add_flag = True
	for item in db.child(word_id).get().each():
		if not isinstance(item.val(), str) and translation_id in item.val().values():
			add_flag = False

	if add_flag:
		data = {"translation": translation_id}
		db.child(word_id).push(data)
	
	add_flag = True

	for item in db.child(translation_id).get().each():
		if not isinstance(item.val(), str) and word_id in item.val().values():
			add_flag = False

	if add_flag:
		data = {"translation": word_id}
		db.child(translation_id).push(data)

word_types=["english", "doggospeak"]


def add_translation(word_type, word, *translations):
	"""
	# TODO: check if words exist yet, if they do, update them

	Adds a new translation to database

	Args:
		word_type (boolean): False=english->pupperspeak; True=pupperspeak->english
		word (string): the word to translate
		*translations (string): one or more translation definitions for word
	"""

	word_id = find_word(word)
	if not word_id:
		print("no word found for: " + word)
		# save word & type in FB
		data = {
			"word" : word,
			"type" : word_types[word_type]
		}
		word_id = db.push(data)["name"]

	

	id_list = []

	for translation in translations:
		id = find_word(translation)
		if not id:
			print("no translation found for: " + translation)
			data = {
				"word" : translation,
				"type" : word_types[not word_type]
				}
			id = db.push(data)["name"]
		id_list.append(id)

	for id in id_list:
		# check if link already exists
		add_links(word_id, id)


# def remove(word):


# def edit(word, new_translation):


# def find_translation(word):




def main():
	# find_word("doggo")
	# add_translation(True, "woofwoof", "dog", "cow", "canine")
	add_translation(False, "dog", "woofwoof", "doggo")


if __name__ == "__main__":
    main()