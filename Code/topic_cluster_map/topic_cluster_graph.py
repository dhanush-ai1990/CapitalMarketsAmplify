__author__ = 'Sahba'
from collections import OrderedDict
from math import cos, sin, pi
import random

div_x = 800
div_y = 800


def generate_js_file(topic,group_number):
    experts = {'Sahba':0.1, 'Aditi':0.8, 'Dhanush':0.5, 'Ada':0.3,"Greg":1}
    related_topics = {'Gas':0.9, 'Power':0.5,'Electricity':0.01}
    nodes = []
    edges = []

    topic_node = {'id':1,'label':topic,'value':35,'group':group_number,'x':div_x/2,'y':div_y/2}
    nodes.append(topic_node)

    total_nodes = len(experts)+len(related_topics)
    random_list = random.sample(range(total_nodes), total_nodes)

    id_counter = 2
    for expert,score in experts.iteritems():
        new_node = {}
        new_node['id'] = id_counter
        new_node['label'] = expert
        new_node['value'] = 10
        new_node['group'] = group_number
        angle = (2 * pi * (random_list[id_counter-2])) / len(random_list)
        x, y = point_on_circle(angle, score)
        new_node['x'] = x
        new_node['y'] = y
        nodes.append(new_node)
        edges.append([1,id_counter,score])
        id_counter += 1

    group_counter = 1
    for topic,score in related_topics.iteritems():
        new_node = {}
        new_node['id'] = id_counter
        new_node['label'] = topic
        new_node['value'] = 20
        new_node['group'] = group_number+group_counter
        angle = (2 * pi * (random_list[id_counter - 2])) / len(random_list)
        x, y = point_on_circle(angle, score)
        new_node['x'] = x
        new_node['y'] = y
        nodes.append(new_node)
        edges.append([1, id_counter, score])
        group_counter += 1
        id_counter += 1

    nodes_string = get_node_string(nodes)
    edges_string = get_edge_string(edges)

    print(nodes_string)
    print(edges_string)

def get_node_string(nodes):
    string = "var nodes = [\n"
    for node in nodes:
        string = string+ "\t" + str(node) +",\n"
    string = string + "];"
    return string

def get_edge_string(edges):
    string = "var edges =[\n"
    for edge in edges:
        string = string + "\t{from: "+str(edge[0])+", to: " + str(edge[1]) + ", title:\'Similarity Score: "+str(edge[2])+"\'},\n"
    string = string + "];"
    return string

def point_on_circle(angle,score):
    center = [div_x/2,div_y/2]
    radius = -300*score + 375
    x = center[0] + (radius * cos(angle))
    y = center[1] + (radius * sin(angle))
    return x,y

generate_js_file("oil",1)