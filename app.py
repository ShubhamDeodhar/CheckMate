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
    print(ml)
    return render_template('upload.html', results=ml)



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
    for i in range(0 , len(list)):

        first  = comparison[i][0] - 1
        second = comparison[i][1] - 1

        if list[i] > 0.7:
            s = " Your score is " + str(list[i]*100) + " % between " + str(all_files[first]) + " and " + str(all_files[second])
            final.append(s)
        #print(" Your score is " , list[i]*100 , "% between " , all_files[first] , "and" , all_files[second] , "pdfs")


    return final
    #return render_template('index.html')

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
#@app.route('/uploads/<filename>')
#def uploaded_file(filename):
    #return send_from_directory(app.config['UPLOAD_FOLDER'],
                              # filename)




if __name__ == '__main__':
    app.run(debug=True)