from flask import Flask, request, render_template, url_for, redirect
from doggobackend import add_translation, get_translations, get_word_type, load_all, check_swearsies, edit_word, get_word_type_list, remove
import urllib.parse as urlparse
application = Flask(__name__)

@application.route('/')
def home():
    return render_template('index.html')

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', msg="404 angery doggos ate the page or word you were looking for"), 404

@application.route('/swearsies')
def swearsies():
    return render_template('swearsies.html')

@application.route('/word/<string:word>')
def search(word):
	if check_swearsies(word):
		return swearsies()
	word_type = get_word_type(word)
	if word_type is None:
		return render_template('404.html', msg="We don't have a translation for this word yet! <a href='/#add-words'>Why not make one?</a>"), 404

	trans_type = "pupperspeak"
	if word_type == "pupperspeak":
		trans_type = "english"


	translations = get_translations(word)
	if translations is False:
		return swearsies()

	trans_types = get_word_type_list(translations)
	
	return render_template('word.html', word=word, word_type=word_type, translations=translations, trans_types=trans_types)

@application.route('/api/add', methods=['POST'])
def new_translation():
	# print(request.form)
	inputs = dict(request.form)
	type_req = False
	if inputs.pop("type", None) == "True":
		type_req = True 

	word = inputs.pop("word", None)[0]
	# print(inputs.items())
	if word == "":
		print("Nothing inputted")
		return redirect(url_for('home'))
	translations = [item[0] for name, item in inputs.items()]
	for trans in translations:
		if trans == "":
			return redirect(url_for('home'))

	if check_swearsies(word) or check_swearsies(*translations):
		return swearsies()

	print("@@@@@@@@ NEW_TRANSLATION_API @@@@@@@@")
	print("type: " + str(type_req))
	print("word: " + str(word))
	print("trans: " + str(translations))

	add_translation(type_req, word, *translations)
	return redirect(url_for('home'))


@application.route('/edit/<string:word>')
def edit_view(word):
	word_type = get_word_type(word)
	if word_type is None:
		return render_template('404.html', msg="404 angery doggos ate the page or word you were looking for"), 404
	return render_template('edit.html', word=word, word_type=word_type)

@application.route('/api/edit', methods=['POST'])
def edit():

	inputs = dict(request.form)
	print(inputs)
	word = inputs.pop("word", None)[0]
	new_word = inputs.pop("new_word", None)[0]
	new_type = inputs.pop("new_type", None)[0]

	

	if word == "" or new_word == "" or new_type == "":
		return redirect(url_for('home'))
	print("updating")
	print(word)
	print(new_word)
	print(new_type)

	edit_word(word, new_word, new_type)

	return redirect(url_for('search', word=new_word))

@application.route('/api/delete', methods=['POST'])
def delete():
	inputs = dict(request.form)
	word = inputs.pop("word", None)[0]

	remove(word)
	return redirect(url_for('home'))


@application.route('/all')
def view_all():
	words = load_all()
	# print(words[0])
	if words is None:
		return render_template('404.html', msg="404 angery doggos ate the page or word you were looking for"), 404
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
