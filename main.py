from flask import Flask, render_template, Response, request, redirect,url_for,jsonify
from forms import LoginForm
import os
import datetime
import sqlite3 as sql

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"

# database part
path = 'database/'
users = sql.connect(path + 'user.db',check_same_thread=False)
statics = sql.connect(path + 'sta.db',check_same_thread=False)
udb = users.cursor()
sdb = statics.cursor()

global login_success
# router
@app.route('/')
@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        global username
        username = request.form.get('username',None)
        password = request.form.get('password',None)
        print(username,password)
        memberinfo = udb.execute('''
        Select * From membership
        ''')
        login_success = False
        for row in memberinfo:
            if username == row[0] and password == row[1]:
                login_success = True
        if login_success == True:
            return redirect('/index')
        else:
            print('wrong!')
            return redirect('/login')
    
@app.route('/index')
def index():
    global username
    print(username)
    return render_template('index.html',username=username)

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/video_play')
def video_play():
    return render_template('video_play.html')

def gen(camera):
     """Video streaming generator function."""
     while True:
         frame = camera.get_frame()
         yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
     """Video streaming route. Put this in the src attribute of an img tag."""
     return Response(gen(Camera()),
                     mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/mystatic')
def mystatic():
    x = []
    y = []
    teminfo = sdb.execute('''
    Select * From statics
    ''')
    for row in teminfo:
        x.append(str(row[0])+'h')
        y.append(int(row[1]))
    print(x,y)
    return render_template('static.html',x=x,y=y)

@app.route('/feed')
def feed():
    feedtime = datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
    print(feedtime)
    with open('command.txt','w') as f:
        f.write('2')
    return render_template('static.html',feedtime=feedtime)

@app.route('/changewater')
def water():
    watertime = datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
    print(watertime)
    with open('command.txt','w') as f:
        f.write('1')
    return render_template('static.html',watertime=watertime)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)
