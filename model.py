import pdfplumber
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from pdftotext import get_text
from pdftotext import get_percentages
from pdftotext import assign_comparison



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

            count +=1 

    return final