import sqlite3
import pickle
from sklearn.externals import joblib 
from dijktras_algorithm import *
from sklearn.externals import joblib
import numpy as np

def push_file(value, column_name, table_name):
	"""
	Tries to insert an ID (if it does not exist yet)
	with a specific value in a second column
	"""
	c.execute("INSERT OR IGNORE INTO {tn} ({cn}) VALUES ({v})".format(tn=table_name, cn=column_name, v=value))


def push_2_values(value1, value2, column_name, table_name):
	"""
	Inserts 2 values into 1 slot in the db.
	"""
	c.execute("INSERT INTO {tn} ({cn}) VALUES ({v1}, {v2})".format(tn=table_name, cn=column_name, v1=value1, v2 = value2))
	

if __name__ == "__main__":

	all_formality_scores = joblib.load("normalized_formality_scores.pkl")
	all_sentiment_scores = joblib.load("normalized_sentiment_scores.pkl")
	exchanges_CC = joblib.load("exchange_number_map_cc.p")

	sqlite_file = 'Enron_Entity.db'
	table_name = 'Nodegraph'
	PERSON1 = 'PERSON1'
	PERSON2 = 'PERSON2'
	TIME_KNOWN = 'TIMEKNOWN'
	FORMALITY_SCORE = 'FORMALITY'
	SENTIMENT_SCORE = 'SENTIMENT'
	NUM_EXCHANGES = 'EXCHANGECOUNT'
	HEURISTIC_SCORE = 'SCORE'

	# Connecting to the database file
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

	# Add overall formality score
	cc = 1
	for i in range(len(all_formality_scores)):
		value = all_formality_scores[i][1][0]
		push_file(value, FORMALITY_SCORE, table_name)
		print ("FORMALITY_SCORE ... inserting row #: ", cc) 
		cc += 1

	# Add overall sentiment score
	cc = 1
	for i in range(len(all_sentiment_scores)):
		value = all_sentiment_scores[i][0]
		push_file(value, SENTIMENT_SCORE, table_name)
		print ("SENTIMENT_SCORE ... inserting row #: ", cc) 
		cc += 1


	exchanges_CC = joblib.load("exchange_number_map_cc.p")
	p1 = []
	p2 = []
	num_exchanges = []
	for key, value in exchanges_CC.items():
		p1.append(key[0])
		p2.append(key[1])
		num_exchanges.append(value)

	# Add person 1
	cc = 1
	for thing in p1:
		t = thing.split()
		value = thing
		push_file(thing, PERSON1, table_name)
		print ("PERSON1 ... inserting row #: ", cc) 
		cc += 1

	# Add person 2
	cc = 1
	for thing in p2:
		value = thing
		push_file(value, PERSON2, table_name)
		print ("PERSON2 ... inserting row #: ", cc) 
		cc += 1

	conn.commit()
	conn.close()


