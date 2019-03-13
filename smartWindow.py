#!/usr/bin/evn python3
from flask import Flask, url_for, request, render_template, redirect, session, escape
import requests, json 
import time

app = Flask(__name__)


# session = {}
# session['username'] = 'admin'
# URL = 'http://api.openweathermap.org/data/2.5/weather?zip=84062'
# data = {'accept': 'application/json', 'apikey': '19c5d550c3114c28ad9abfde44856d17'}
# r = requests.get(url = URL, params = data)
# response = r.json()
# response = json.dumps(response)


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
response = {}


@app.route('/')
def index():
    if 'username' in session:
        username = 'Logged in as <b>%s</b>' % escape(session['username'])
        return username + "<br><a href = '/welcome'></b>" + \
        "Click here to go to your dashboard</b></a>"
        #return 'Logged in as %s' % escape(session['username'])
    return "You are not logged in <br><a href = '/login'></b>" + \
    "click here to log in</b></a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form['username']
        username = request.form['password']
        if username != 'admin' or password != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = 'admin'
            session['password'] = 'admin'
            return redirect(url_for('index'))
    return render_template('login.html', error=error)
    # return '''
    #     <form method="post">
    #         <p><input type=text name=username>
    #         <p><input type=submit value=Login>
    #     </form>
    # '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))



# session = {}
# session['username'] = 'admin'

# @app.route('/')
# def index():
#     if 'username' in session:
#         URL = 'http://api.openweathermap.org/data/2.5/weather?zip=84062'
#         data = {'accept': 'application/json', 'apikey': '19c5d550c3114c28ad9abfde44856d17'}
#         r = requests.get(url = URL, params = data)
#         response = r.json()
#         response = json.dumps(response)
#         return response
#     else:
#         time.sleep(2)
#         return redirect(url_for('login'))
#     return render_template('welcome.html', error='Need to login to see this')
    
@app.route('/welcome')
def welcome():
    if 'username' in session:
        URL = 'http://api.openweathermap.org/data/2.5/weather?zip=84062'
        data = {'accept': 'application/json', 'apikey': '19c5d550c3114c28ad9abfde44856d17'}
        response = requests.get(url = URL, params = data)
        JSONresponse = response.json()
        stringResponse = json.dumps(JSONresponse)
        destructedResponse = json.loads(stringResponse)
        output = "<div> City: " + destructedResponse.get('name') + "</div><br>"
        output += "<div> Weather: " + destructedResponse['weather'][0]['main'] + "</div><br>"
        return render_template('welcome.html', response = output)  # render a template
    else:
        return "You need to log in to see the dashboard page. <br><a href = '/login'></b>" + \
        "Click here to log in</b></a>"

# # Route for handling the login page logic
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             if 'username' in session:
#                 return redirect(url_for('welcome'))
#     return render_template('login.html', error=error)

# @app.route('/logout', methods=['GET', 'POST'])
# def logout():
#     error = None
#     if 'username' in session:
#         session.pop('username', None)
#     else:
#         return redirect(url_for('login'))
#     return render_template('login.html', error=error)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

