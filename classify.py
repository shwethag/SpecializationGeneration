#/usr/bin/python

#This file is used to identify the subfields of each and every document


f=open('lda_res.txt','r')
fdata=f.readlines()
f.close()
unwanted = [92,88,44]
subfield_map = {}
for data in fdata:
	#print data
	tlist=data.strip('\n').split('|')
	doc_name=tlist[0].split('.')[0]
	#print len(tlist)
	if len(tlist) <= 2:
		continue 

	prob=0
	subfield=-1
	#print maxdoc,prob
	for i in range(1,len(tlist)):
		curlist=tlist[i].strip('(').strip(')').split(',')
		cur_subfield=int(curlist[0])
		if cur_subfield in unwanted:
			continue

		cur_prob=float(curlist[1])
		if cur_prob > prob:
			prob=cur_prob
			subfield=cur_subfield
	#print subfield,doc_name	

	if subfield in subfield_map:
		subfield_map[subfield].append(doc_name)
	else:
		dlist = []
		dlist.append(doc_name)
		subfield_map[subfield]=dlist


for item in subfield_map.items():
	k,v=item
	#print k,len(v)			
	print k,v
	#print "------------------------"	
