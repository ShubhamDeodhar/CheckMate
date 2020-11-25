import os
import pdfplumber
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from wtforms import MultipleFileField
from flask_wtf import FlaskForm
from flask_uploads import configure_uploads,  UploadSet

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from pdftotext import get_text
from pdftotext import get_percentages
from pdftotext import assign_comparison

from model import ml_model

from autoevaluate import get_qno_text
from autoevaluate import evaluate


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
    app.config['UPLOAD_FOLDER'] = 'uploads/'
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
    
    ml = ml_model()
    length = len(ml)

    path = r'uploads' 
    all_files_to_delete = glob.glob(path + "/*.pdf")
    all_files_to_delete = [x.replace('uploads\\', '') for x in all_files_to_delete]

    for files in all_files_to_delete:

        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], files))

    print(all_files_to_delete)

    return render_template('upload.html', results=ml , length = length)

@app.route('/autoevaluate')
def shift():

    return render_template('autoevaluate.html')

@app.route('/evaluateUpload',methods = ['GET', 'POST'])
def evaluateupload():

    app.config['UPLOAD_FOLDER'] = 'answersheets/'

    uploaded_files_answers = request.files.getlist("file[]")
    marks = request.form['marks']

    filenames = []
    
    for file in uploaded_files_answers:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)

    file_path_names = []

    for file in filenames:

        file_path = "answersheets/" + file

        file_path_names.append(file_path)

    reference_text = get_text(file_path_names[0])

    answer_sheet_text = get_text(file_path_names[1])

    #answer_sheet_text = []

    #for file in file_path_names[1:]:
    #    ans = get_text(file)
    #    answer_sheet_text.append(ans)

    reference_dict = get_qno_text(reference_text)

    answer_dict    = get_qno_text(answer_sheet_text)

    #answer_sheet_dict_list = []

    #for answers in answer_sheet_text:

    #    answer_sheet_dict_list.append(get_qno_text(answers))

    reference_keys = reference_dict.keys()
    answer_keys = answer_dict.keys()

    #answer_keys_list = []
    #for answer_sheet in answer_sheet_dict_list:

    #    answer_keys_list.append(answer_sheet.keys())

    list1_as_set = set(reference_keys)
    
    intersection = list1_as_set.intersection(answer_keys)
    
    intersection_as_list = list(intersection)

    final_question_similarity = []

    for questions in intersection_as_list:

        reference_value = reference_dict[questions]

        answer_value    = answer_dict[questions]

        corp_value = [reference_value , answer_value]

        vect = TfidfVectorizer(min_df=1, stop_words="english")
        tfidf = vect.fit_transform(corp_value)
        pairwise_similarity = tfidf * tfidf.T 

        list1 = pairwise_similarity.toarray()

        list2 = get_percentages(list1)
        comparison1 = assign_comparison(len(list1))

        #all_files_questions = [x.replace('answersheets\\', '') for x in all_files_questions]

        #final = []
        #count = 0
        #for i in range(0 , len(list2)):

            #first  = comparison1[i][0] - 1
            #second = comparison1[i][1] - 1

            #if list[i] > 0.7:
            #s = 
            #final.append(s)

            #count +=1 

        final_question_similarity.append(list2)


    final_question_similarity_list = []

    for i in final_question_similarity:
        for j in i:
            final_question_similarity_list.append(j)


    final_question_similarity_list = [i*100 for i in final_question_similarity_list]

    final_question_similarity_list = [round(i,2) for i in final_question_similarity_list]

    final_similarity_string = []

    marks_list    = []

    total = 0

    for i in range(0,len(final_question_similarity_list)):

        to_say = "The answers for Q" + str(intersection_as_list[i]) + " are " + str(final_question_similarity_list[i]) + " percent satisfactory."

        final_similarity_string.append(to_say)
        if (final_question_similarity_list[i] > 90):
            marks_awarded = 0

        elif (final_question_similarity_list[i] > 70 and final_question_similarity_list[i] < 90):

            marks_awarded = float(marks)*0.1

        elif (final_question_similarity_list[i] >30 and final_question_similarity_list[i] < 70):

            marks_awarded = float(marks)*.3
        elif (final_question_similarity_list[i] >10 and final_question_similarity_list[i] < 30):

            marks_awarded = float(marks)*.18
        else:
            marks_awarded = 0



        marks_awarded += (final_question_similarity_list[i])*float(marks)*0.01

        total += marks_awarded 

        marks_ele = "Marks for Q " + str(intersection_as_list[i]) + " are " + str(round(marks_awarded,2)) + " out of " + str(marks)



        marks_list.append(marks_ele)

        total_marks = float(marks)*(len(final_question_similarity_list))
    
    for i in reference_keys:

        if(i not in intersection_as_list):

            total_marks += int(marks)

            new_marks_ele = "Marks for Q " + str(i) + " are " + str(0)

            marks_list.append(new_marks_ele)

    print(marks_list)

    path = r'answersheets' 
    all_files_to_delete = glob.glob(path + "/*.pdf")
    all_files_to_delete = [x.replace('answersheets\\', '') for x in all_files_to_delete]

    for files in all_files_to_delete:

        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], files))

    return render_template('result.html',marks_list = marks_list ,
                                         total = total,
                                         total_marks = total_marks)


@app.route('/autoevaluate',methods = ['GET'])
def back():

    return render_template('autoevaluate.html')


if __name__ == '__main__':
    app.run(debug=True)


