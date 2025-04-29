from flask import Flask, render_template, request
from Backend.function import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    if login(username, password) == True:
        return render_template('main.html', username=username)
    else:
        return render_template('index.html', error='Invalid username or password')

@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form['username']
    password = request.form['password']

    signup(username, password)
    return render_template('main.html', username=username)

@app.route('/sysprompt', methods=['POST'])
def sysprompt_post():
    username = request.form['username']   # YOU NEED TO GET THE USERNAME HERE
    sys = request.form['sysinput']
    code = request.form['codeinput']
    sysprompt(username, sys, code)  # Call the sysprompt function with the username

    if username:
        success = sysprompt(username, sys, code)
        if success:
            return render_template('main.html', username=username, message="System prompt updated.")
        else:
            return render_template('main.html', username=username, error="Phantom code already used by another user.")
    else:
        return render_template('index.html', error='User not logged in')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
