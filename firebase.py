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


def word_exists(word):
	"""
	Checks if a word exists in database
	word (string): the word to search for
	Returns the word ID if it exists, otherwise None
	"""
	all_words = db.get()
	for item in all_words.each():
		if word in item.val()["word"]:
			return item.key()
	return None

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
	# save word & type in FB
	data = {
		"word" : word,
		"type" : word_types[word_type]
	}
	word_id = db.push(data)["name"]

	id_list = []

	for translation in translations:
		data = {
			"word" : translation,
			"type" : word_types[not word_type]
		}
		id = db.push(data)["name"]
		id_list.append(id)

	for id in id_list:
		data = {"translation": id}
		db.child(word_id).push(data)

		data = {"translation": word_id}
		db.child(id).push(data)

# def remove(word):


# def edit(word, new_translation):


# def find_translation(word):




def main():
	word_exists("doggo")
	# add_translation(True, "dog", "doggo", "doggy")


if __name__ == "__main__":
    main()