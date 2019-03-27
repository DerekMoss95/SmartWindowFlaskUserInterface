#!/usr/bin/evn python3
from flask import Flask, url_for, request, render_template, redirect, session, escape
import requests, json, serial, time, datetime

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
response = {}

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
ser.flushInput()

@app.route('/')
def index():
    if 'username' in session:
        username = 'Logged in as <b>%s</b>' % escape(session['username'])
        return username + "<br><a href = '/welcome'></b>" + \
        "Click here to go to your dashboard</b></a>"
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

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
    
@app.route('/weather', methods=['POST','GET'])
def weather():
    if request.method == 'GET':
        URL = 'http://api.openweathermap.org/data/2.5/weather?zip=84062'
        data = {'accept': 'application/json', 'apikey': '19c5d550c3114c28ad9abfde44856d17'}
        response = requests.get(url = URL, params = data)
        JSONresponse = response.json()
        stringResponse = json.dumps(JSONresponse)
        destructedResponse = json.loads(stringResponse)
        print(destructedResponse)
        output = "<div> Last time weather data received: " + datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %S %p") + "</div><br>"
        kelvinTemp = destructedResponse.get('main')['temp']
        farenheitTemp = kelvinTemp * (9/5) - 459.67
        temp = str(farenheitTemp)
        temp = temp[:5]
        output += "<div> Current temperature: " + temp + " F</div><br>"
        output += "<div> City: " + destructedResponse.get('name') + "</div><br>"
        output += "<div> Weather: " + destructedResponse['weather'][0]['main'] + "</div><br>"
        weather = destructedResponse['weather'][0]['main']
        #if weather == 'rain' or weather == 'snow':
        #    print("Signaled window to close")
        #    try:
        #        right = str.encode("0")
        #        ser.write(right)
        #    except:
        #        print("Input error, could not close window")
        #        ser.write(str.encode('WRONG'))
        return output
        
        
@app.route('/welcome', methods=['POST','GET'])
def welcome():
    if 'username' in session:
        if request.method == 'POST':
            turn = request.form['turn']
            if turn == 'open':
                print("Signaled window to " + turn)
                try:
                    left = str.encode("1")
                    ser.write(left)
                except:
                    print("Input error, could not open window")
                    ser.write(str.encode('WRONG'))
            if turn == 'close':
                print("Signaled window to " + turn)
                try:
                    right = str.encode("0")
                    ser.write(right)
                except:
                    print("Input error, could not close window")
                    ser.write(str.encode('WRONG'))
        return render_template('welcome.html')  # render a template
    else:
        return "You need to log in to see the dashboard page. <br><a href = '/login'></b>" + \
        "Click here to log in</b></a>"

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


