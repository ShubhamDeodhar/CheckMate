import re
from pdftotext import get_text

def get_qno_text(string):

	iter = re.finditer(r"Q\d", string)
	indices = [m.start(0) for m in iter]
	qnos = [int(string[i+1]) for i in indices]

	keys = qnos
	indices_text = []
	last = len(indices)
	for i in range(0,len(indices)):

		if i != last - 1:
			indices_text.append(string[indices[i]:indices[i+1]])
		else:
			indices_text.append(string[indices[i]:])
			

	dict1 = {qnos[i]: indices_text[i] for i in range(len(keys))} 

	return dict1

def evaluate(reference , answer):

    corpus = []

    for answers in reference:

        text = get_text(answers)
        
        corpus.append(text)

    for answers in answer:

        text = get_text(answers)
        
        corpus.append(text)

    return corpus