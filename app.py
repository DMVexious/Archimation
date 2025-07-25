import os
import uuid
from flask import Flask, render_template, request, url_for, jsonify, g
import logging
from Master_test import generate_video_from_topic 
app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html') 

@app.route('/input.html')
def input_page():
    return render_template('input--.html')

@app.route('/index.html')
def index():
    return render_template('index.html')
    
@app.route('/library.html')
def library():
    return render_template('library.html')

@app.route('/result.html')
def result():
    return render_template('result.html')
  
if __name__=='__main__':
    app.run(debug=True, port=5001)