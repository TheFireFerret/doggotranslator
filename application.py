from flask import Flask, request, render_template, url_for, redirect
from doggobackend import add_translation, get_translations, get_word_type, load_all
import urllib.parse as urlparse

application = Flask(__name__)

@application.route('/word')
@application.route('/')
def home():
    return render_template('index.html')

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# TODO add word not found page
@application.route('/word/<string:word>')
def search(word):
	word_type = get_word_type(word)
	if word_type is None:
		return render_template('404.html'), 404

	trans_type = "pupperspeak"
	if word_type == "pupperspeak":
		trans_type = "english"
	translations = get_translations(word)
	return render_template('word.html', word=word, word_type=word_type, translations=translations, trans_type=trans_type)

@application.route('/api/add', methods=['POST'])
def new_translation():
	# print(request.form)
	inputs = request.form
	type_req = False
	if inputs["type"] == "True":
		type_req = True 

	translations = [item for name, item in list(inputs.items())]
	print("@@@@@@@@NEW_TRANSLATION_API@@@@@@@@")
	print("type: " + str(type_req))
	print("word: " + inputs["word"])
	print("trans: " + str(list(translations[2:])))
	add_translation(type_req, inputs["word"], *list(translations[2:]))
	return redirect(url_for('home'))

@application.route('/all')
def view_all():
	words = load_all()
	return render_template('list.html', words=words)

# TODO for bot, return words only
# @application.route('/api/search', methods=['POST'])
# def search_translation():
# 	term = request.form['term']
# 	# print(term)
# 	# translations = get_translations(term)
# 	# print(translations)
# 	return redirect(url_for('search', word=term))

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production application.
    # applicationlication.debug = True
    application.run()
