import os
import pdfplumber
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from wtforms import MultipleFileField
from flask_wtf import FlaskForm
from flask_uploads import configure_uploads,  UploadSet

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from pdftotext import get_text
from pdftotext import get_percentages
from pdftotext import assign_comparison



app=Flask(__name__)

app.config['SECRET_KEY']='thisisasecret'
app.config['UPLOAD_FOLDER'] = 'uploads/'

app.config['ALLOWED_EXTENSIONS'] = set([ 'pdf'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
    
    ml = ml_model()
    length = len(ml)
    return render_template('upload.html', results=ml , length = length)



def ml_model():
    path = r'uploads' # use your path
    all_files = glob.glob(path + "/*.pdf")

    corpus = []

    for file in all_files:

        text = get_text(file)
        corpus.append(text)

    vect = TfidfVectorizer(min_df=1, stop_words="english")
    tfidf = vect.fit_transform(corpus)
    pairwise_similarity = tfidf * tfidf.T 

    list1 = pairwise_similarity.toarray()

    list = get_percentages(list1)
    comparison = assign_comparison(len(list1))


    all_files = [x.replace('uploads\\', '') for x in all_files]

    final = []
    count = 0
    for i in range(0 , len(list)):

        first  = comparison[i][0] - 1
        second = comparison[i][1] - 1

        if list[i] > 0.7:
            s = " Your score is {:0.2f}".format((list[i]*100))  + " % between " + str(all_files[first]) + " and " + str(all_files[second])
            final.append(s)

            #print("\nYour Celsius value is {:0.2f}ºC.\n".format(answer))

            count +=1 
        


    return final

if __name__ == '__main__':
    app.run(debug=True)