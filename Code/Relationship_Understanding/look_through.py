import sqlite3
import pickle
from sklearn.externals import joblib 
from dijktras_algorithm import *
from sklearn.externals import joblib


file_out = '/Users/AdaEne/Documents/Entity Recognition/'
Database = sqlite3.connect(file_out + 'Enron_database.db')
c = Database.cursor()
SQL = "select distinct(msgid), raw_body from `Enron Prime`"
c.execute(SQL)
list_of_stuff = []
count = 1
for data in c:
	p = raw_input()
	if p == ' ':

		print (data)
		print ("##############################################################################")