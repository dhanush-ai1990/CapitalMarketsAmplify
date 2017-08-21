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
	#### SHIT CODE
	"""
	verlanderlich = {}
	count = 1
	verlanderlich["nodes"] = []
	verlanderlich["edges"] = []
	for key, value in temp_dict.items():
		cccc = 0
		for sub_dictionary in verlanderlich["nodes"]:
			if key.split()[0] in sub_dictionary["caption"] and not key.split()[1] in sub_dictionary["caption"]:
				some_id = sub_dictionary['id']
				print(some_id)
				verlanderlich["nodes"].append({"id": 's'+str(count), "caption": key.split()[1], "role": "person", "root": False})
				cccc += 1

			elif key.split()[1] in sub_dictionary["caption"] and not key.split()[0] in sub_dictionary["caption"]:
				verlanderlich["nodes"].append({"id": 's'+str(count), "caption": key.split()[0], "role": "person", "root": False})

		verlanderlich["nodes"].append({"id": 's'+str(count), "caption": key.split()[0], "role": "person", "root": False})
		count += 1
		verlanderlich["nodes"].append({"id": 's'+str(count), "caption": key.split()[1], "role": "person", "root": False})
		verlanderlich["edges"].append({"source": 's'+str(count-1), "target": 's'+str(count), "load": value})
	"""
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
	#print (final_dictionary)

	only_heuristics = extract_only_heuristic(final_dictionary)
	temp_dict = make_temp_dictionary(only_heuristics, 10)
	das_ergebnis = make_json_dictionary(temp_dict)

	print (das_ergebnis)
	joblib.dump(das_ergebnis, "das_ergebnis.pkl", protocol=2)

	raise Exception("STOP")

	final_dict = json.dumps(verlanderlich)
	final_json = json.loads(final_dict)

	#print (final_json)

	with open('final_json.json', 'w') as fp:
	    json.dump(final_json, fp)

	with open('final_json.json') as f:
	    data = json.load(f)

	#print (data)





	"""
	with open('final_json.json', 'r+') as f:
	    data = json.load(f)
	    data['id'] = 134 # <--- add `id` value.
	    f.seek(0)        # <--- should reset file position to the beginning.
	    json.dump(data, f, indent=4)
	    f.truncate()
	print (f)
	"""







