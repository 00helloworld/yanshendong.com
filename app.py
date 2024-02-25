from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def HomePage():
    return render_template('HomePage.html')


@app.route('/resume')
def show_resume():  # inline with the 'show_resume' of jinja href="{{ url_for('show_resume')}}"
    return render_template('resume.html')

