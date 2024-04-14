from flask import Flask,request, url_for, redirect, render_template
import pandas as pd
import numpy as np
import pickle
import sqlite3
import keras

app = Flask(__name__)

import tensorflow as tf
loaded_model = tf.keras.models.load_model('models/lstm.h5')

@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():

    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    temp = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")

@app.route('/predict',methods=['POST','GET'])
def predict():
    inp = []
    for i in range(1,20):
         inp.append(float(request.form[str(i)]))
    row_df = np.array(inp)
    row_df_reshaped = row_df.reshape(1, 1, 19)
    predictions = loaded_model.predict(row_df_reshaped)
    predicted_labels = np.argmax(predictions, axis=1)
    prediction = predicted_labels[0]
    if prediction == 0:
        return render_template('after.html',pred=f'Normal')
    elif prediction == 1:
        return render_template('after.html',pred=f'DoS Attack')
    elif prediction == 2:
        return render_template('after.html',pred=f'R2L Attack')
    elif prediction == 3:
        return render_template('after.html',pred=f'Probe Attack')
    elif prediction == 4:
        return render_template('after.html',pred=f'U2R Attack')



@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/notebook')
def note():
	return render_template('notebook.html')


if __name__ == '__main__':
    app.run(debug=True)
