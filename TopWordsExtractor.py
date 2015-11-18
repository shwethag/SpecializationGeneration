#/usr/bin/python

from nltk.tokenize import RegexpTokenizer
from os import listdir
from os.path import isfile, join
import gensim
from gensim import corpora, models, similarities
from gensim.models import *
from gensim.interfaces import *
import logging


def loadDocNames():
	f=open('lda_res1.txt','r')
	fdata=f.readlines()
	f.close()
	namelist = []
	for data in fdata:
		tlist=data.strip('\n').split('|')
		doc_name=tlist[0].split('.')[0]
		namelist.append(doc_name)


	return namelist


def saveTopWords():
	namelist = loadDocNames()
	# for i in range(len(namelist)):
	# 	print i,namelist[i]

	dictonary = corpora.Dictionary.load('deerwester.dict')
	token2id =  dictonary.token2id


	id2token = { v : k for k,v in token2id.items()}


	corpus = corpora.MmCorpus('./deerwester.mm')

	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	ind = 0
	topwordmap = {}

	for doc in corpus_tfidf:
		doc = sorted(doc,key = lambda x:x[1],reverse=True)
		topwordmap[namelist[ind]] = []
		size = min(5,len(doc))
		for i in range(size):
			topwordmap[namelist[ind]].append(id2token[doc[i][0]])
		ind += 1
		#break
	#print corpus
	ofile = open('topwords.txt','w')
	for item in topwordmap.items():
		docname,wordl = item
		topwords = ''
		for word in wordl:
			topwords += word+','
		ofile.write(docname+'|'+topwords.rstrip(',') + '\n')


	ofile.close()

saveTopWords()
