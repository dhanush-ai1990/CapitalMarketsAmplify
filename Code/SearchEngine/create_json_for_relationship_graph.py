import json
from gensim.models import Word2Vec
import gensim
from sklearn.externals import joblib
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.tag import pos_tag
from nltk.tokenize import *
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.tokenize import *
from nltk.tag import pos_tag
import urllib
import urllib2
import json
import sqlite3
from sklearn.externals import joblib
from gensim.models import Word2Vec
import gensim
from sklearn.externals import joblib
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.tag import pos_tag
from nltk.tokenize import *
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.tokenize import *
from nltk.tag import pos_tag
import urllib
import urllib2
import json
import clearbit


file_loc = '/Users/Dhanush/Desktop/Enron_Data/Search_engine_pickle/'
org_loc = file_loc +"/Orgs/"

SearchEngineWordList=joblib.load(file_loc+'SearchEngineWordList.pkl')
SearchEngineWordList.pop('hughes')
SearchEngineWordList.pop('the')

mapping_to_type_dict=joblib.load(file_loc+'mapping_to_type_dict.pkl')

exception =[]
exception_file = open (file_loc+'exception.txt','r')
for line in exception_file:
    line = line.replace('\n','')
    exception.append(line)
exception = list(set(exception)) + ['ECT','Enron']
exception =[element.lower() for element in exception]

Database = sqlite3.connect('/Users/Dhanush/Desktop/Enron_Data/Enron_database.db')
c = Database.cursor()

SQL = "select `EMAIL ID`, FIRST, LAST, `FULL NAME`, ORGANIZATION from `EMPLOYEE`"
c.execute(SQL)

def fetch_type(word):
	global mapping_to_type_dict
	try:
		word = mapping_to_type_dict[word]
	except KeyError:
		return "PERSON"
	return word

enron_table = {}
other_org_table ={}
for record in c:
	if record[2] =='**':
		continue
	org = record[4].lower()
	if org == 'enron':
		enron_table[record[0].lower()] =[]
		enron_table[record[0].lower()].append('enron')
		enron_table[record[0].lower()].append(record[3])
	else:
		if org not in exception:
			other_org_table[record[0].lower()] =[]
			other_org_table[record[0].lower()].append(record[4])
			other_org_table[record[0].lower()].append(record[3])


#Now we have the databases for people.

with open('temp_10000.json') as json_data:
    d = json.load(json_data)
    nodes =d['nodes']
    edges =d['edges']



#Get all the Nodes from JSON
node_list = []

count =0
for node in nodes:
	if node['caption'] in enron_table:
		word = enron_table[node['caption']][1]
		org = enron_table[node['caption']][0]
		if word not in SearchEngineWordList:
			continue
		if word in exception:
			continue
		node_list.append([word,org,node['id']])
		count+=1
	elif node['caption'] in other_org_table:
		word = other_org_table[node['caption']][1]
		org = other_org_table[node['caption']][0]
		if word not in SearchEngineWordList:
			continue
		if word in exception:
			continue
		node_list.append([word,org,node['id']])
		count+=1
	else:
		continue







#Lets create the groups:
list_topics = ['gas','fuel','energy','power','wind','utilities','legal','technology','finance','security','operation','equity','accounting','asset','marketing','administration','revenue','insurance','investment','trade']
print len(list_topics)
Group ={}
count = 1

for item in list_topics:
	Group[item] = count
	count+=1


node_list_with_info = []



#step1

#Get info like People, Organization, Top topic results as cluster and next two as interests
#Now we have people mapped to organization. Now lets do the word2vec query to get the expertise and interests.
model = gensim.models.Word2Vec.load(file_loc+'wordvecmodel')
nlp = spacy.load('en')

new_node_list = []
for person in node_list:
	searchword = person[0].lower()
	vector = model.wv[searchword]
	list_words =  model.similar_by_vector(vector, topn=5000, restrict_vocab=None)
	flag =0
	cluster = ''
	cluster_size = 0
	interest_list = []
	for item in list_words:

			try:
				if (str(item[0]))in exception:
					continue

				if (item[0].title == searchword):
					continue

				if (fetch_type(str(item[0])) == "TOPIC"):
					if str(item[0]) in list_topics:
						if flag == 0:
							cluster_name = str(item[0]).title()
							cluster = Group[str(item[0])]
							cluster =4
							cluster_size = item[1]
							flag = 1
						if cluster_name =='Legal':
							print searchword
						if flag == 1:
							if len(interest_list) < 2:
								interest_list.append(item[0].title().encode("utf-8"))
			except UnicodeEncodeError:
				continue
	if cluster_size ==0:
		continue
	temp = []
	temp.append(cluster)
	temp.append(int(cluster_size*40))

	string =",".join(interest_list)
	temp.append(string)
	temp.append(cluster_name)
	joined = person + temp
	new_node_list.append(joined)

	#print person

#Now we have selected our Nodes. We remove any edges not in our nodes. This will be redundent data
print len(new_node_list)

gets_selected_id = []

for item in new_node_list:
	gets_selected_id.append(item[2])


#Get all the edges from JSON

edge_list = []
connection_exist =[]
for edge in edges:
	source = edge['source']
	target = edge['target']
	if source == target:
		continue
	value = edge['load']
	value = value/4
	value1 = int(value*10)
	value2 = int(value*200)
	connection_exist.append(edge['source'])
	connection_exist.append(edge['target'])

	edge_list.append([edge['source'],edge['target'],value1,value2])



print len(new_node_list)
print len(edge_list)
new_node_list = new_node_list[0:300]
#
new_node_list=sorted(new_node_list,key=lambda l:l[4], reverse=False)



#Now lets build the Json.
print new_node_list[0]
print edge_list[0]
nodes =[]
# {id: 1, label: 'Abdelmoumene Djabou', title: 'Country: ' + 'Algeria' + '<br>' + 'Team: ' + 'Club Africain', value: 22, group: 24},
F = open("WorldCup2014.js","w")
F.write("var nodes = [") 


for node in new_node_list:
	if node[2] not in connection_exist:
		continue
	string = "{id: " + str(node[2][1:]) + ", label: '" + str(node[0].title()) +"', title: "+ "'Organization: ' + '" + str(node[1].title()) +"' + '<br>' + 'Cluster: ' + '" + str(node[6].title()) +"' + '<br>' + 'Interests: ' + '" + str(node[5].title()) + "', value: " + str(node[3]) +", group:  " + str(node[4])+"},"
	nodes.append(string)
	#print string
	F.write(string)

F.write("];")
F.write("var edges = [")
edges =[]

for edge in edge_list:
	string = "{from: %s, to: %s, value: %s, title: 'Relationship score: %s'}," %(edge[0][1:],edge[1][1:],edge[2],edge[3])
	edges.append(string)
	F.write(string)

F.write("];")
F.close()

"""
x: -1392.5499, y: 1124.1614
x: -2016.3092, y: 442.13663
x: 276.62708, y: 826.51605},
x: -761.32623, y: 1152.3298},
x: -341.64163, y: -1640.5049},
x: 13.4137335, y: -43.777435},
x: 1990.1855, y: 1052.6255},
"""



print len(gets_selected_id)

joblib.dump(gets_selected_id,'we_are_getting_selected_id.pkl')

#Now lets build the edges
#{from: 2, to: 8, value: 3, title: '3 emails per week'},






