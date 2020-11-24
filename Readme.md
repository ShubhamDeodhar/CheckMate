# CheckMate
<p align="center">
<img src="https://github.com/ShubhamDeodhar/CheckMate/blob/master/image.jpg" width=20%/>


<h2 align="center">Team Dracarys</h2>

## Problem Statement

In the time when the world has come on the internet for education full time, it's equally important for these platforms to be strongly backed up by technology. One of the major loopholes is plagiarism and copying in online exams. To tackle this issue, we bring to you 'Check Mate'. 
With our tool, teachers and professors can get all the pdf documents compared and checked for plagiarism. 

## Our Solution

A fully functional end to end pipeline for finding the similarity between scanned handwritten documents. The web app comes with feature like uploading files in pdf formats, checking the similarity score between the documents and if the person caught in copying other stuff an automated email will generated and sent to the respective peoples email id's with the similarity scores

## Preview of UI

<img src="https://github.com/ShubhamDeodhar/CheckMate/blob/master/Images%20UI/UI_1.jpeg" width = 40%/> &nbsp;&nbsp;
<img src="https://github.com/ShubhamDeodhar/CheckMate/blob/master/Images%20UI/UI_2.jpeg" width = 40%/> &nbsp;&nbsp; <br><br>
<img src="https://github.com/ShubhamDeodhar/CheckMate/blob/master/Images%20UI/UI_3.jpeg" width = 40%/> &nbsp;&nbsp;
<img src="https://github.com/ShubhamDeodhar/CheckMate/blob/master/Images%20UI/UI_4.jpeg" width = 40%/>




## Why NLP?

We used the tf-idf and Bag of words techniques of NLP to check the similarity between the files, by tokenizing each sentence and creating the score.
We then return the similarity score of every pair of files.

## Stakeholders 

The stakeholders included are:
1. Professors and Teachers
2. Educational Institute

## Functionalities

1. Document similarity score:
The input documents are processed by the model, and a similarity score is generated as an output depicting the percentage of similarity (i.e. copying) between each pair of documents.
2. Automated email generation:
If the similarity score between any two docs is above 70%, an automated email will be generated and sent to the respective user( professor or teacher's) email.
3. Autoevaluation:
With this feature, the user can input a reference document and the document to be evaluated (of the same format), and then evaluation is given.

## TechStack

1. Data pipeline: The first step of data pipeline is to extract the pdf files transform them into .txt format.
2. NLP Implementation: We used the tf-idf and Bag of words techniques to check the similarity between the files.
We return the similarity score of every pair of files.
3. User Interface: We created a minimalistic designed frontend and displayed our results by a flask web-app.
We generate an automated email containing the similarity score( if only it's above a threshold value).

## Future Prospects:

1. Handwritten docs input:
Building a model to perform plagiarism for handwritten and scanned documents. 
2. Auto Evaluation with OMR:
Developing an application to compare the submission with a reference omr file and display results.
3. Working with gcr:
Making an extension of the app to be implemented on Google Classroom submissions.
4. Open sourcing the project:
To deploy the app and make it available for public use!


## How to Use

To run it on your local machine do the following using your command line

 * Clone the repository in your local machine 
 
 ```
 git clone https://github.com/ShubhamDeodhar/CheckMate.git
 ```
 
 * Change the directory
 ```
 cd YOUR-PATH\CheckMate
 ```
 
 * If you don't have virtual environment library installed , do the following
 ```
 pip install virtualenv
 ```
 
 * Create a new virtual environment for the directory and activate it
 ```
 py -m venv env
 
 .\env\Scripts\activate
 ```
 
 * Install requirements.txt file using pip
 ```
 pip install -r requirements.txt
 ```
 
 * Run Flask
 ```
 python app.py
 ```
 
 * Copy the localhost link and paste it in your browser & voila!
 
 #### Note
 
 You would need to delete the files uploaded from ``` answersheets ``` and ``` uploads ``` each time you run our app
 
