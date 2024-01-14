from flask import Flask, request, url_for, redirect, render_template, flash, get_flashed_messages
from werkzeug.datastructures import ContentRange
import requests, json
import os
from werkzeug.utils import secure_filename
from flask_wtf import RecaptchaField, FlaskForm
import numpy as np


UPLOAD_FOLDER = '/users/mariaserrao/again/vids'
# change this to file location in your computer
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mov'}

app= Flask(__name__)
app.secret_key='bruh'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


sitekey = "6Le18UEeAAAAAEktBliN2LSCnc7zISxkhnkesqdu"
@app.route('/ai_page', methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        captcha_response = request.form['g-recaptcha-response']
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # You can either call the function using the file in the 
            # file as the variable for the function
            # You can also take the file and predict it straight away
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', name=filename))

        if is_human(captcha_response):
            # Process request here
            status = "Detail submitted successfully."
        else:
             # Log invalid attempts
            status = "Sorry ! Bots are not allowed."

        flash(status)
        return redirect(url_for('upload_file'))
    return render_template('ai_page.html', sitekey=sitekey)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about_us')
def about():
    return render_template('about_us.html')
@app.route('/contact_us')
def contact():
    return render_template('contact_us.html')
@app.route('/ono')
def pls():
    return render_template('why.html')

def is_human(captcha_response):
    """ Validating recaptcha response from google server.
        Returns True captcha test passed for the submitted form 
        else returns False.
    """
    secret = "6Le18UEeAAAAAPnsE6ZymwVWRCFc6pLbFlzl_OTq"
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']

if __name__ == "__main__":
    app.run(debug=True)