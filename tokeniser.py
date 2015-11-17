																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																															#/usr/bin/python
from nltk.tokenize import RegexpTokenizer
from os import listdir
from os.path import isfile, join
import gensim
from gensim import corpora, models, similarities
from gensim.models import *
from gensim.interfaces import *
import re
import logging


#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
fpath = "../../aan/papers_text"
#fpath='./files/'
print "reading filenames"
files =  [ f for f in listdir(fpath) if isfile(join(fpath,f)) ]
print "reading filenames over"
num_of_topics=100
num_of_iterations=1
top_words=10

#load stop words
print "populating stopwords"
stop_file = "./stopwords.txt"
f = open(stop_file,'r')
stop_list = f.readlines()
f.close()
stop_list = [line.rstrip('\n') for line in stop_list]
stop_set = set()
for word in stop_list:
	stop_set.add(word)
stop_set = sorted(stop_set)
# stop_list = f.readlines()
# stop_set = set()
# stop_set = (line.rstrip('\n') for line in stop_list)
#print stop_set

tokenizer = RegexpTokenizer('(?:(?:\w+(?:\w+|\-?)))+|\S+')


# files
print "adding to list list_tokenized ..."
list_tokenized = []
pattern = r'^[a-zA-Z-]+$'
i = 0

for fp in files:
	f = open(join(fpath,fp),'r')
	print files[i],i
	clean_tokens = []
	content = f.read()
	toklist = tokenizer.tokenize(content)
	for word in toklist:
		if re.search(pattern,word) and len(word) > 2 and word.lower() not in stop_set:
				clean_tokens.append(word.lower())
	#clean_sentence = ' '.join(clean_tokens)
	list_tokenized.append(clean_tokens)
	f.close()
	i+=1


#tokenize and add to list_tokenized
#print "adding to list_tokenized"
#list_tokenized = []
# numbers left.. try to change if accuracy goes down

# print "remove stop words from documents and store as list of words"
# texts = [[word for word in document.split() if word not in stop_set] for document in list_tokenized]
#print texts
print "computing frequency"
from collections import defaultdict
frequency = defaultdict(int)
for text in list_tokenized:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
        for text in list_tokenized]
# from pprint import pprint   # pretty-printer
# pprint(texts)

dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict') 
print "store the dictionary, for future reference"
#id2word = gensim.corpora.Dictionary.load('')

# #print(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
#print corpus
print "tfidf calculation"
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]														
# # for doc in corpus_tfidf:
# # 	print(doc)																															
print "lda model starting"
lda = gensim.models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_of_topics, update_every=1, chunksize=10000, passes=num_of_iterations)
topwordfile = open('./topic_top_words.txt','w')
topwordfile.write('\n'.join(lda.print_topics(num_of_topics)))
topwordfile.close()
print "storing final result"
outfile = open('./lda_res.txt','w')
outlist = []
for i in range(len(files)):																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																
	temp = []
	temp.append(files[i])
	temp.append(str(lda[corpus[i]]).strip('[]'))
	outlist.append(str(temp).strip('[]'))

outfile.write('\n'.join(outlist))
outfile.close()

print "Hola done"																																																																																																																																																																																																																																																																																																																											

