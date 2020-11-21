import pdfplumber

def get_text(filename):

	with pdfplumber.open(filename) as pdf:
		words = []
		pages = pdf.pages
		for page in pages:

			page_text = page.extract_text()
			words.append(page_text)


	text = (' '.join(words))

	splitted_text = text.split()
	for word in splitted_text:

		if word.isalnum() == False:

			del word

	final_text = (' '.join(splitted_text))

	return final_text

def get_percentages(list1):

    length = len(list1) - 1

    final = []
    for i in list1:

        if (length >= 1):

            s = ((i[-length:]))
            for j in s:

                final.append(j)

        length = length - 1

    return final

def assign_comparison(n):
	
	comparisons = []

	for i in range(1, n+1):
		for j in range(1,n+1):
			if ( i < j):
				comparisons.append([i,j])

	return comparisons

