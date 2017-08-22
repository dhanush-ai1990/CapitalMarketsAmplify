import json
import pickle
from sklearn.externals import joblib

def extract_only_heuristic(old_dictionary):
	neu_dict = {}
	for key, value in final_dictionary.items():
		p1 = key[0]
		p2 = key[1]
		pairs = p1 + ' ' + p2
		neu_dict[pairs] = value[4]
	return neu_dict

def make_temp_dictionary(old_dictionary, max):
	temp_dict = {}
	count = 0
	for key,value in old_dictionary.items():
		if count > max:
			break
		else:
			temp_dict[key] = value
			count += 1
	return temp_dict

def make_json_dictionary(old_dictionary):
	verlanderlich = {}
	der_knoten_liste = []
	der_kanten_liste = []

	for key, value in old_dictionary.items():
		node_temp1 = {}
		node_temp2 = {}
		edge_temp = {}
		p1 = key.split()[0]
		p2 = key.split()[1]
		node_temp1['caption'] = p1
		node_temp2['caption'] = p2
		if node_temp1 not in der_knoten_liste:
			der_knoten_liste.append(node_temp1)
			true_once = True
		if node_temp2 not in der_knoten_liste:
			der_knoten_liste.append(node_temp2)
			true_twice = True
		edge_temp['source'] = p1
		edge_temp['target'] = p2
		edge_temp['load'] = value * 2	# make an edge between these two new nodes
		der_kanten_liste.append(edge_temp)

	verlanderlich['nodes'] = der_knoten_liste
	verlanderlich['edges'] = der_kanten_liste

	ego = 1
	for artikel in verlanderlich['nodes']:
		artikel['id'] = 's'+str(ego)
		artikel['role'] = 'person'
		artikel['root'] = 'false'
		ego += 1

	for element in verlanderlich['edges']:
		for artikel in verlanderlich['nodes']:
			if element['source'] == artikel['caption']:
				element['source'] = artikel['id']
			if element['target'] == artikel['caption']:
				element['target'] = artikel['id']


	return verlanderlich 
		

if __name__ == "__main__":

	final_dictionary = pickle.load( open( "final_dictionary.pkl", "rb" ) )

	only_heuristics = extract_only_heuristic(final_dictionary)
	temp_dict = make_temp_dictionary(only_heuristics, 10)
	das_ergebnis = make_json_dictionary(temp_dict)
	joblib.dump(das_ergebnis, "das_ergebnis.pkl", protocol=2)

	final_dict = json.dumps(verlanderlich)
	final_json = json.loads(final_dict)


	with open('final_json.json', 'w') as fp:
	    json.dump(final_json, fp)

	with open('final_json.json') as f:
	    data = json.load(f)


