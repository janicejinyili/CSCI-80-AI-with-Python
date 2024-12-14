import nltk
nltk.download('punkt')
import sys
import string


s = 'I ate a pissa today. The price was 53dolloars'
word_list = nltk.tokenize.word_tokenize(s)
tokens = [t.lower().translate(str.maketrans('', '', string.punctuation)) for t in word_list if any(l.isalpha() for l in t)]
print(tokens)