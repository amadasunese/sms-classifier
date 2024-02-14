from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import joblib

app = Flask(__name__)

# Load the trained model and vectorizer
model = MultinomialNB()
vectorizer = CountVectorizer()

# Assuming you have the trained model and vectorizer
# If not, you can load them using joblib or pickle
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
        result = f'The message is {prediction}.'

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
