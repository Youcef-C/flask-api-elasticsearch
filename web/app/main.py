import string
import flask
from flask import Flask, url_for, jsonify
from datetime import datetime
from marmiton import Marmiton
from urllib import request, parse
import zipfile

app = Flask(__name__)

@app.route('/')
def index():
	return jsonify(status='ok',message='Hi there')

def get_marmiton_val(keywords):
	keywords = keywords.replace('-', ' ')
	query_opt = {
		"aqt": keywords
	}
	query_search = Marmiton.search(query_opt)
	return query_search

def sort_values(query_search, y, limit, isdlable):
	final = dict()
	if (isdlable == True):
		zipc = zipfile.ZipFile('./images.zip', 'w')
	for x in range (y, limit):
		final[x] = query_search[x]['image']
		name = '/tmp/img-recipe-' + str(x) + '.jpg'
		if (isdlable == True):
			request.urlretrieve(final[x], name)
			zipc.write(name)
	if (isdlable == True):
		zipc.close()
	return final

@app.route('/recipes/search<string:keywords>/<int:limit>/<int:offset>', methods=['post', 'get'])
def recipes_dl(keywords, offset, limit, isdlable=None):
	if (flask.request.args.get('download') == ''):
		isdlable = True
	else:
		isdlable = False
	query_search = get_marmiton_val(keywords)
	limit = (len(query_search) if (limit > len(query_search) or limit <= 0) else limit)
	x = (offset if (offset < len(query_search) and offset >= 0) else 0)
	final = sort_values(query_search, x, limit, isdlable)
	return jsonify(final)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
