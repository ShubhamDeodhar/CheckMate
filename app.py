from flask import Flask, render_template, request, redirect,flash
from wtforms import MultipleFileField
from flask_wtf import FlaskForm
from flask_uploads import configure_uploads,IMAGES,UploadSet

import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

app=Flask(__name__)

app.config['SECRET_KEY']='thisisasecret'
app.config['UPLOADED_IMAGES_DEST']='uploads/'

pdfs=UploadSet('files',IMAGES)
configure_uploads(app,pdfs)


class NewFileForm(FlaskForm):
    files = MultipleFileField('files')

###@app.route('/')
#def landing():
   #return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload():
    form = NewFileForm()
    if form.validate_on_submit():
        files_filenames = []
        for file in form.files.data:
            file_filename = secure_filename(file.filename)
            
            files_filenames.append(file_filename)
        print(files_filenames)
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)



if (__name__ == "__main__"):
   app.run(debug=True)