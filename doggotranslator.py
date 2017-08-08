from flask import Flask, request, render_template, flash
from doggobackend import add_translation, get_translations
import urllib.parse as urlparse

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/add', methods=['POST'])
def add_translation():
	# print(request.form)
	inputs = request.form
	type_req = False
	if inputs["type"] == "True":
		type_req = True 

	translations = [item for name, item in list(inputs.items())]
	add_translation(type_req, inputs["word"], *list(translations[2:]))
	return render_template('word.html')

@app.route('/api/search', methods=['POST'])
def search_translation():
	term = request.form['term']
	print(term)
	translations = get_translations(term)
	print(translations)
	return render_template('word.html')