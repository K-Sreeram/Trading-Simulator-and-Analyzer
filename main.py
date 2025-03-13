# integrate HTML with the flask
# HTTP verb GET and POST

from flask import Flask,redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def loginPage():
    return render_template('login.html')

@app.route('/register')
def registerPage():
    return render_template('register.html')

if __name__=='__main__':
    app.run(debug=True)