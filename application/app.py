from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import joblib
from form import ContactForm
from flask_mail import Mail, Message
import smtplib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a47680abc56efeea392f4af3a03453ee'

# Configure Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'amadasunese@gmail.com'
app.config["MAIL_PASSWORD"] = 'qxxo axga dzia jjsw'
app.config['MAIL_DEFAULT_SENDER'] = 'amadasunese@gmail.com'
mail = Mail(app)


# Load the trained model and vectorizer
model = MultinomialNB()
vectorizer = CountVectorizer()

model = joblib.load('model/spam_detection_model.joblib')
vectorizer = joblib.load('model/spam_detection_vectorizer.joblib')

# Load stopwords and stemmer
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Function for preprocessing text
def preprocess_text(text):
    words = [stemmer.stem(word) for word in text.split() if word.lower() not in stop_words]
    return ' '.join(words)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        message = request.form['message']
        processed_message = preprocess_text(message)
        message_vec = vectorizer.transform([processed_message])
        prediction = model.predict(message_vec)[0]
        
        if prediction == 'spam':
            result = 'This message is a spam.'
        else:
            result = 'This message is not a spam.'

    return render_template('index.html', result=result)

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        msg = Message("Contact Form Submission",
                      sender=email,
                      recipients=["amadasunese@gmail.com"])

        msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        mail.send(msg)
        flash('Your message has been sent.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':
    app.run(debug=True)
