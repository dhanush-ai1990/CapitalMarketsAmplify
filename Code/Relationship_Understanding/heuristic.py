from normalize import *
import sqlite3
import pickle
from sklearn.externals import joblib 
from dijktras_algorithm import *
from sklearn.externals import joblib
import numpy as np
import os.path
import re
import matplotlib.pyplot as plt

"""
	For all people that are connected with a closeness score, we can find the k-shortest paths, 
	being the greatest sentiment between two nodes. 
"""

def get_the_stuff():
	file_out = '/Users/AdaEne/Documents/Entity Recognition/'
	Database = sqlite3.connect(file_out + 'Enron_database.db')
	c = Database.cursor()
	SQL = "select distinct(msgid), sender_email, receiver_email from `Enron Prime`"
	c.execute(SQL)
	list_of_stuff = []
	count = 1
	for data in c:
		print ("processing email # ", count)
		list_of_stuff.append(data)
		count += 1
	joblib.dump(list_of_stuff,"msgID_sender_receiver.pkl")
	
 
def heuristic(theta1, theta2, theta3, sentiment_score, formality_score, time_known):
	"""
	Input: 	Fixed parameters: theta1, theta2, theta3
			Sentiment Score: sentiment_score
			Formality Score: formality_score
			Time known: time_known 
	"""		
	return sentiment_score*theta1 + formality_score*theta2 + time_known*theta3 


def N_max(a,N):
    return np.argsort(a)[::-1][:N]


def N_min(a,N):
    return np.argsort(a)[:N]


def return_top_n_best_worst(list_of_scores, list_of_IDs, N):
	"""
	Input: 	list_of_scores: list of sentiments
			list_of_IDs: a list containing all email contents
			N: number of best and worst emails to return (total: N*2)
	Output:	N best + N worst emails
	"""
	max_N_indeces = N_max(list_of_scores, N)
	min_N_indeces = N_min(list_of_scores, N)
	print (max_N_indeces)
	print (min_N_indeces)

	emails = []
	for i in range(N):
		emails.append((list_of_bodies[int(min_N_indeces[i])], list_of_bodies[int(max_N_indeces[i])]))
	return emails


def pair_sender_receiver(msgID_sender_receiver, sorted_dictionary_of_stuff, dict_of_times):
	# loop through msgID_sender_receiver and make following dictionary:
	# { ['sender', receiver]: [msgID_1, msgID_2 ...], }
	map_it = {}
	for i in range(len(msgID_sender_receiver)):
		try:
		    sentiment = sorted_dictionary_of_stuff[msgID_sender_receiver[i][0]][0]
		    formality = sorted_dictionary_of_stuff[msgID_sender_receiver[i][0]][1]
		    time_stamp = dict_of_times[msgID_sender_receiver[i][0]]
		    if (msgID_sender_receiver[i][1], msgID_sender_receiver[i][2]) in map_it:		#if key exists
		    	map_it[(msgID_sender_receiver[i][1], msgID_sender_receiver[i][2])][0].append(msgID_sender_receiver[i][0])
		    	map_it[(msgID_sender_receiver[i][1], msgID_sender_receiver[i][2])][1].append(sentiment)
		    	map_it[(msgID_sender_receiver[i][1], msgID_sender_receiver[i][2])][2].append(formality)
		    	map_it[(msgID_sender_receiver[i][1], msgID_sender_receiver[i][2])][3].append(time_stamp)
		    else:
		    	map_it[(msgID_sender_receiver[i][1], msgID_sender_receiver[i][2])] = [[msgID_sender_receiver[i][0]], [sentiment], [formality], [time_stamp]] 
		except KeyError:
			pass
	
	joblib.dump(map_it, "map_it.pkl")
	return map_it

def das_average(die_liste):
	return sum(die_liste) / float(len(die_liste))


def time_known(die_liste):
	"""
	Return max_value - min_value in list.
	"""
	return max(die_liste) - min(die_liste) + 1


def time_to_be_average(ze_dict):
	"""
	Average out the sentiments and formalities
	"""
	timessss = []
	neu_dict = {}
	for key, value in ze_dict.items():
		neu_dict[key] = [value[0], das_average(value[1]), das_average(value[2]), time_known(value[3])]
		timessss.append(time_known(value[3]))
	return neu_dict, timessss


def binarySearch(alist, item):
	if len(alist) == 0:
		return False
	else:
		midpoint = len(alist)//2
		if alist[midpoint]==item:
			return midpoint
		else:
			if item<alist[midpoint]:
				return binarySearch(alist[:midpoint],item)
			else:
				return binarySearch(alist[midpoint+1:],item)


def make_temp_dict(emailIDs, sentiments, formalities):
	"""
	temp_dict = {n_i: [s_i, f_i] ... }
	"""
	temp_dict = {}
	for i in range(len(emailIDs)):
		temp_dict[emailIDs[i]] = [sentiments[i], formalities[i][1][0]]
	return temp_dict


def sort_dict(dict):
	sorted_dict = {}
	for key, value in sorted(dict.items()):
		sorted_dict[key] = value
	return sorted_dict


def please_work(der_pickles):
	#msgID_sender_receiver = joblib.load(der_pickles)
	with open(der_pickles, 'rb') as f:
	    msgID_sender_receiver = pickle.load(f, encoding='latin1')
	new_list = []
	temp = []
	for msgid in msgID_sender_receiver:
		temp.append(str(msgid))
		temp.append(msgID_sender_receiver[msgid]['sender_email'])
		temp.append(msgID_sender_receiver[msgid]['receiver_email'])
		new_list.append(temp)
		temp = []
	return new_list


def fix_the_goddam_format(der_list):
	new_list = []
	temp = []
	for thing in der_list:
		for ughhhh in thing[2]:
			temp.append(thing[0])
			temp.append(thing[1])
			temp.append(ughhhh)
			new_list.append(temp)
			temp = []
	return new_list


def change_stuff(das_worterbuch):
	neu_worterbuch = {}
	for key, value in das_worterbuch.items():
		print (value)
		relevant_stuff = value.split()
		if relevant_stuff != []:
			relevant_stuff = relevant_stuff[0]
			date = re.sub('-', '', relevant_stuff)
			neu_worterbuch[str(key)] = int(date)
	return neu_worterbuch

def make_resulting_dictionary(temp_dict, neu_zeit):
	final_dict = {}
	i = 0
	for key, value in averaged_dictionary.items():
		final_dict[key] = [value[0], value[1], value[2], neu_zeit[i], heuristic(.5, .3, .2, value[1], value[2], neu_zeit[i])]
		i += 1
	return final_dict

if __name__ == "__main__":
	nl = please_work("Email_Entity_Mapping.pkl")
	msgID_sender_receiver = fix_the_goddam_format(nl)
	#print (msgID_sender_receiver)
	#hard_prob = joblib.load("Formal-Informal/formal_out.pkl")

	### CODE BELOW WAS USEFUL AT SOME POINT
	#print ("loading msgID, sender, receiver info ... ")
	#msgID_sender_receiver = joblib.load("msgID_sender_receiver.pkl")
	#print ("length of msgID_sender_receiver: ", len(msgID_sender_receiver))

	email_labels = joblib.load("map_it.pkl")

	print ("loading email labels ... ")
	email_labels = joblib.load("Sentiment Analysis/labels.pkl")
	print ("length of email_labels: ", len(email_labels))
	email_labels = email_labels[0:176000]
	print ("sentiment emailID: ", email_labels[175999])

	print ("loading soft formal probabilities ... ")
	soft_formal_probabilities = joblib.load("Formal-Informal/formal_proba.pkl")
	print ("length of soft_formal_probabilities: ", len(soft_formal_probabilities))
	soft_formal_probabilities = soft_formal_probabilities[0:176000]
	print ("formal emailID: ", soft_formal_probabilities[175999])

	print ("loading sentiment neuron activations ... ")
	sentiment_neuron_activations  = joblib.load("Sentiment Analysis/activations.pkl")
	sentiment_neuron_activations = sentiment_neuron_activations[0:176000]
	print ("length of sentiment_neuron_activations: ", len(sentiment_neuron_activations))

	print ("normalizing scores ... ")
	all_formality_scores = soft_formal_probabilities
	all_sentiment_scores = normalize_sentiment(sentiment_neuron_activations)
	#all_number_of_exchanges = normalize_num_exchanges(all_number_of_exchanges)
	all_sentiment_scores = all_sentiment_scores[2:] # remove the normalizing values
	#all_number_of_exchanges = []

	joblib.dump(all_formality_scores, "normalized_formality_scores.pkl")
	joblib.dump(all_sentiment_scores, "normalized_sentiment_scores.pkl")
	print ("done")

	all_formality_scores = joblib.load("normalized_formality_scores.pkl")
	all_sentiment_scores = joblib.load("normalized_sentiment_scores.pkl")

	all_sentiment_scores = np.array(all_sentiment_scores).tolist()
	all_sentiment_scores = [val for sublist in all_sentiment_scores for val in sublist]

	temp_dict = make_temp_dict(email_labels, all_sentiment_scores, all_formality_scores)
	down_with_times = joblib.load("get_timestamp.pkl")
	neu_dict = change_stuff(down_with_times)
	print (neu_dict)
	full_dictionary_over_time = pair_sender_receiver(msgID_sender_receiver, temp_dict, neu_dict)
	print (full_dictionary_over_time)
	joblib.dump(full_dictionary_over_time, "full_dictionary_over_time.pkl")
	averaged_dictionary, zeit = time_to_be_average(full_dictionary_over_time)
	print (averaged_dictionary)
	print (zeit)
	neu_zeit = normalize_time_known(zeit)
	print (neu_zeit)
	neu_zeit = np.array(neu_zeit).tolist()
	neu_zeit = [val for sublist in neu_zeit for val in sublist]
	print (neu_zeit)
	final_dictionary = make_resulting_dictionary(averaged_dictionary, neu_zeit)
	print (final_dictionary)
	joblib.dump(final_dictionary, "final_dictionary.pkl")









