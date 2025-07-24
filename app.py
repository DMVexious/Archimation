from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password': # Replace with actual authentication
            return render_template('index.html')
        else:
            return render_template('login.html', message='Invalid credentials')
    return render_template('login.html')


@app.route('/input.html')
def input():
    return render_template('input.html')

if __name__=='__main__':
    app.run(debug=True)