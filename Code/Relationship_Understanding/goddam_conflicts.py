from sklearn.externals import joblib

def please_work(der_pickles):
	msgID_sender_receiver = joblib.load(der_pickles)
	new_list = []
	temp = []
	for msgid in msgID_sender_receiver:
		temp.append(msgid)
		temp.append(msgID_sender_receiver[msgid]['sender_email'])
		temp.append(msgID_sender_receiver[msgid]['receiver_email'])
		new_list.append(temp)
		temp = []
	joblib.dump(new_list, "goddammit.pkl")
	return new_list