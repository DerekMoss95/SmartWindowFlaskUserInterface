#!/usr/bin/evn python3
from flask import Flask, url_for, request, render_template, redirect, session, escape
from Crypto.Hash import SHA256
import requests, json, serial, time, datetime

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
        username = request.form['username']
        password = request.form['password']
        encodedPassword = password.encode('utf-8')
        encryptedPassword = SHA256.new(encodedPassword).hexdigest()
        if username != 'derek' or encryptedPassword != '701fbfd68fbf2b9890d2d2bc8f61ded15153d9cbc5771376737d68ba9c1c9250':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = username
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
        URL = 'http://api.openweathermap.org/data/2.5/weather?zip=84604'
        data = {'accept': 'application/json', 'apikey': '19c5d550c3114c28ad9abfde44856d17'}
        response = requests.get(url = URL, params = data)
        JSONresponse = response.json()
        stringResponse = json.dumps(JSONresponse)
        destructedResponse = json.loads(stringResponse)
        print(destructedResponse)
        output = "<div> <b> Last time weather data received: </b>" + datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %S %p") + "</div><br>"
        kelvinTemp = destructedResponse.get('main')['temp']
        farenheitTemp = kelvinTemp * (9/5) - 459.67
        #farenheitTemp = 35
        temp = str(farenheitTemp)
        temp = temp[:5]
        weather = destructedResponse['weather'][0]['main']
        #weather = 'Clouds'
        #weather = 'Rain'
        city = destructedResponse.get('name')
        output += "<div> <b> Current temperature: </b>" + temp + " F</div><br>"
        output += "<div> <b> City: </b>" + city + "</div><br>"
        output += "<div> <b> Weather: </b>" + weather + "</div><br>"
        fileRead = open("autoWeather.txt", "r")
        fileContents = fileRead.read()
        fileRead.close()
        if fileContents == "yes":
            output += "<div> When the temperature falls below <b>40</b> degrees, it will close.</div><br>"
            if weather == 'Rain' or weather == 'Snow' or farenheitTemp <= 40:
                print("Signaled window to close")
                try:
                    right = str.encode("0")
                    ser.write(right)
                except:
                    print("Input error, could not close window")
                    ser.write(str.encode('WRONG'))
                request.form = {}
        return output
    else:
        return "Couldn't connect to weather API"

@app.route('/window', methods=['POST','GET'])
def window():
    check = str.encode("2")
    ser.write(check)
    if request.method == 'GET':
        if (ser.in_waiting > 0):
            inputV = ser.readline()
            inputV = str(inputV)
            inputValue = "<div> <b> Current window status: </b>" + inputV[2:-5] + "</div><br>"
            return inputValue
        else:
            inputValue = "<div> <b> Current window status: </b> Retrieving window data... </strong></div><br>"
            return inputValue
            
@app.route('/autoWeather', methods=['POST','GET'])
def autoWeather():
    if request.method == 'GET':
        fileRead = open("autoWeather.txt", "r")
        fileContents = fileRead.read()
        fileRead.close()
        contents = "<div> <b> Weather based auto close status: </b>" + fileContents + "</div><br>"
        return contents

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
            if turn == 'auto':
                fileRead = open("autoWeather.txt", "r")
                fileContents = fileRead.read()
                fileRead.close()
                print(fileContents)
                if fileContents == "yes":
                    with open('autoWeather.txt', "w") as autoFile:
                        autoFile.write("no")
                    print("Changed user preference to no")
                elif fileContents == "no":
                    with open('autoWeather.txt', "w") as autoFile:
                        autoFile.write("yes")
                    print("Changed user preference to yes")
        request.form = {}
        return render_template('welcome.html')
    else:
        return "You need to log in to see the dashboard page. <br><a href = '/login'></b>" + \
        "Click here to log in</b></a>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


