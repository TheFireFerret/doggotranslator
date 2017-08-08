from flask import Flask, request
import doggobackend
import urllib.parse as urlparse

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/add', methods=['POST'])
def add_translation():
	print(request.form)
	inputs = request.form
	type_req = False
	if inputs["type"] == "True":
		type_req = True 
	doggobackend.add_translation(type_req, inputs["word"], inputs["def"])
	return "wow"