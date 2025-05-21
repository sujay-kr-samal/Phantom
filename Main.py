from flask import Flask, render_template, request
from Backend.function import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login_post():
    try:
        username = request.form['username']
        password = request.form['password']
        
        user_data = get_user_data(username)
        if user_data is None:
            return render_template('index.html', error='User not found.')
        
        system_prompt = user_data.get('system_prompt')
        phantom_code = user_data.get('phantom_code')

        if login(username, password):
            return render_template('main.html', username=username, system_prompt=system_prompt, phantom_code=phantom_code)
        else:
            return render_template('index.html', error='Invalid username or password')
    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template('index.html', error='An error occurred during login.')

@app.route('/signup', methods=['POST'])
def signup_post(): 
    try:
        username = request.form['username']
        password = request.form['password']

        if signup(username, password):  # Check if signup was successful
            # After signup, directly log in the user
            system_prompt = get_user_data(username).get('system_prompt')
            phantom_code = get_user_data(username).get('phantom_code')

            return render_template('main.html', username=username, system_prompt=system_prompt, phantom_code=phantom_code)
        else:
            return render_template('index.html', error='Username already taken.')
    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template('index.html', error='An error occurred during login.')

@app.route('/sysprompt', methods=['POST'])
def sysprompt_post():
    username = request.form.get('username')
    sys = request.form.get('sysinput')
    code = request.form.get('codeinput')

    if username:
        success = sysprompt(username, sys, code)
        user_data = get_user_data(username)  # <- re-fetch updated values here

        return render_template(
            'ui.html',
            username=username,
            system_prompt=user_data.get('system_prompt'),
            phantom_code=user_data.get('phantom_code'),
            message="System prompt updated." if success else "Phantom code already used by another user."
        )
    else:
        return render_template('index.html', error='User not logged in')

@app.route("/input", methods=["POST"])
def input_post():
    username = request.form.get('username')
    input_text = request.form.get('input_txt')
    Ai(input_text, username)
    return render_template("ui.html", username=username, response_text=get_chat_history(username))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
