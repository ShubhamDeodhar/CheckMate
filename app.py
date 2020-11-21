import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from wtforms import MultipleFileField
from flask_wtf import FlaskForm
from flask_uploads import configure_uploads,  UploadSet

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

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
    
    return render_template('index.html', filenames=filenames)

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