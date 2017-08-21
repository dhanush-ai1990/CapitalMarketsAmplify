import sqlite3
from sklearn.externals import joblib


def load_raw_emails():
	file_out = '/Users/AdaEne/Documents/Entity Recognition/'
	Database = sqlite3.connect(file_out + 'Enron_database.db')
	c = Database.cursor()
	SQL = "select distinct(msgid), raw_body,subject from `Enron Prime`"
	c.execute(SQL)
	all_emails = []
	count = 0
	for data in c:
		body = data[1].split('-----Original Message-----')[0]
		count +=1
		print('Currently processing the email number: ' + str(count))
		all_emails.append(str(body))
		#print type(all_emails[0])
		#raise Exception("OFAHRGUHR")
	#joblib.dump(all_emails,"all_emails.pkl")
	return all_emails
	#with open('raw_emails.pkl','w') as f:
	#    pickle.dump(all_emails,f)

if __name__ == "__main__":
	#emails = load_raw_emails()

	emails = joblib.load('raw_emails.pkl') 

	print emails[732]