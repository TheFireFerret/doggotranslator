import pyrebase
import os
from bad_words import bad_words
from operator import itemgetter


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
	print("finding word: " + word)
	try:
		all_words = db.get()
		for item in all_words.each():
			if word == item.val()["word"]:
				# print("found word: " + word)
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

word_types=["english", "pupperspeak"]


def add_translation(word_type, word, *translations):
	"""

	Adds a new translation to database

	Args:
		word_type (boolean): False=english->pupperspeak; True=pupperspeak->english
		word (string): the word to translate
		*translations (string): one or more translation definitions for word
	"""
	print(type(translations))

	if word == "" or not translations:
		return

	print("######### add translation ##########")
	print(word_type)
	print(word)
	print(translations)

	word = word.upper()

	
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
		translation = translation.upper()
		print("TRANSLATION::: " + translation)
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


def remove(word):
	word_id = find_word(word)
	if word_id is None:
		return
	# go into each translation link and remove the link on that end
	# and then delete this node
	for item in db.child(word_id).get().each():
		# print(item.val())
		if not isinstance(item.val(), str):
			translation_id = item.val()["translation"]
			# print(translation_id)
			remove_link(translation_id, word_id)
	db.child(word_id).remove()

#remove link from word to translation (remove node within word_id)
def remove_link(word_id, translation_id):
	for item in db.child(word_id).get().each():
		if not isinstance(item.val(), str) and translation_id in item.val().values():
			# print(item.key())
			db.child(word_id).child(item.key()).remove()

def edit_word(word, new_word, new_type):
	word_id = find_word(word)
	if word_id is None:
		print("Edit failed for word: " + word)
		return

	# update the word to new_word and change the word type, keeping all links
	word_db = db.child(word_id)

	data = {"type": new_type, "word": new_word.upper()}
	word_db.update(data)


def get_translations(word):
	word = word.upper()
	# print(word)
	word_id = find_word(word)
	if word_id is None:
		return None
	print("get_translations word_id: " + word_id)
	translations = []
	for item in db.child(word_id).get().each():
		if not isinstance(item.val(), str):
			translations.append(db.child(item.val()["translation"]).get().val()["word"])

	return translations

def get_word_type(word):
	word = word.upper()
	try:
		all_words = db.get()
		for item in all_words.each():
			if word == item.val()["word"]:
				return item.val()["type"]
		return None
	except TypeError:
		return None

def get_word_type_list(words):
	lists = []
	for word in words:
		word = word.upper()
		try:
			all_words = db.get()
			for item in all_words.each():
				if word == item.val()["word"]:
					lists.append(item.val()["type"])
			return None
		except TypeError:
			return None
	return lists

# returns tuples of ["word", "type"]
def load_all():
	words = []
	try:
		all_words = db.get()
		for item in all_words.each():
			if item.val()["word"]:
				words.append((item.val()["word"], item.val()["type"]))
		print(words)
		words.sort(key=itemgetter(0))
		print(words)

		return words
	except TypeError:
		return None

def check_swearsies(*words):
	for word in words:
		if word.lower() in bad_words:
			return True
	return False


# def main():
	# edit_word("")
# 	# find_word("doggo")
# 	# add_translation(True, "woofwoof", "dog", "cow", "canine")
# 	# add_translation(False, "dog", "woofwoof", "doggo")
# 	# add_translation(False, "puppy", "pupper", "pupperino")

# 	# remove("dog")
# 	# get_translations("woofwoof")
# 	print("wow!")
# 	# print(load_all())


# if __name__ == "__main__":
#     main()