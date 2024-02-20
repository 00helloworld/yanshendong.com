from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def hello():
    return render_template('resume.html')

#######
@app.route('/user/<name>')
def user_page(name):
    return f'{name} page'