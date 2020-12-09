import flask
import os
from flask import Flask, flash, request, redirect, url_for

from flask import request, jsonify
import sqlite3
from flask import request

from parser import *
import json
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'uploads/'

app = flask.Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# app.config["DEBUG"] = True

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

@app.route('/', methods=['POST'])
def readFile():
    print(request.method)
    # print(request.form['name'])
    file = request.files['file']
    if file:
        filename = file.filename
        print(file)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # print("Tags", get_tags(url))
        # return redirect(url_for('success', name = get_tags(url)))
        return json.dumps(get_tags(url))
    return '''No Files'''

@app.errorhandler(404)
def page_not_found(e):
    return '{ "error": { "code": "NOT_FOUND", "message": "The requested path could not be found" } }', 404

app.run(debug=True, host='0.0.0.0')