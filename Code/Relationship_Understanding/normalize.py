import numpy as np
from sklearn import preprocessing 

### NORMALIZE SENTIMENT 
def normalize_sentiment(scores):
	"""
		Input: List of scores. Ex: [1., -1., .8]
		Output: A 1 * N normalized array of scores.
	"""
	l = [-1.5, 1.5] + scores
	X_train = np.array(l).reshape(-1,1)

	min_max_scaler = preprocessing.MinMaxScaler()
	X_train_minmax = min_max_scaler.fit_transform(X_train)
	return X_train_minmax

### NORMALIZE NUMBER OF EMAILS 
def normalize_num_exchanges(num_emails):
	"""
		Input: List of number of emails for each receiver. Ex: [1,2,3,4,5,6,7,3,2]
		Output: A 1 * N normalized array of scores.
	"""
	new_num_emails = []
	for num in num_emails:
		num = float(num)
		if num > 5.:
			num = 5.
		new_num_emails.append(num)
	print (new_num_emails)
	l = [1., 5.] + new_num_emails 
	X_train = np.array(l).reshape(-1,1)

	min_max_scaler = preprocessing.MinMaxScaler()
	X_train_minmax = min_max_scaler.fit_transform(X_train)
	return X_train_minmax

### NORMALIZE TIME_KNOWN
def normalize_time_known(zeit):
	"""
		Input: List of days known for each pair of people. Ex: [1,2,3,4,5,6,7,3,2]
		Output: A 1 * N normalized array of scores.
	"""
	neu_zeit = []
	for num in zeit:
		num = float(num)
		if num > 100.:
			num = 100.
		neu_zeit.append(num)
	print (neu_zeit)
	l = neu_zeit 
	X_train = np.array(l).reshape(-1,1)

	min_max_scaler = preprocessing.MinMaxScaler()
	X_train_minmax = min_max_scaler.fit_transform(X_train)
	return X_train_minmax


if __name__ == "__main__":
	V = normalize_sentiment([1., -1., .8])
	print (V)
	print (len(V))
	









