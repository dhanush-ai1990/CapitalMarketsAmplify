__author__ = 'Sahba'
from collections import OrderedDict
from math import cos, sin, pi
import random
from QueryWord2Vec import *


def generate_js_file():
	map_info = GenerateTopicClusterMap()

	nodes = [] 
	edges = [] 

	id_counter = 1
	group_number = 1
	for [topic_title, people_list, related_topics_list] in map_info:
		topic_node = create_node(id_counter,topic_title.title(),group_number,'topic')
		nodes.append(topic_node)
		id_counter += 1
		
		for person_name in people_list:
			person_node = get_node(nodes,person_name)
			
			if not any(person_node):
				person_node = create_node(id_counter,person_name,group_number,'people')
				nodes.append(person_node)
				id_counter += 1
			edges.append([topic_node['id'],person_node['id']])

		for related_topic in related_topics_list:
			related_topic_node = get_node(nodes,related_topic)
			if any(related_topic_node):
				edges.append([topic_node['id'],related_topic_node['id']])

		group_number += 1

	nodes_string = get_node_string(nodes)
	edges_string = get_edge_string(edges)

	text_file = open("static/vendors/visjs/datasource/big_topic_cluster.js", "w+")
	text_file.write(nodes_string+"\n"+edges_string)
	text_file.close()

def create_node(id,label,group,node_type):
	new_node = {}
	new_node['id'] = id
	new_node['label'] = label
	new_node['group'] = group
	if node_type=='topic':
		new_node['value'] = 20
	else:
		new_node['value'] = 10
	return new_node


def get_node(nodes,person_name):
	for node in nodes:
		if node['label'] == person_name:
			return node
	return {}

def get_node_string(nodes):
    string = "var nodes = [\n"
    for node in nodes:
        string = string+ "\t" + str(node) +",\n"
    string = string + "];"
    return string

def get_edge_string(edges):
	string = "var edges =[\n"
	for edge in edges:
		string = string + "\t{from: "+str(edge[0])+", to: " + str(edge[1]) + "},\n"
	string = string + "];"
	return string


generate_js_file()