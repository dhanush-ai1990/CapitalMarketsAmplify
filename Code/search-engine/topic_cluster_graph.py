__author__ = 'Sahba'
from collections import OrderedDict
from math import cos, sin, pi
import random
from QueryWord2Vec import *

div_x = 800
div_y = 800

def get_total_nodes(options,json):
    [clients,employees,places,orgs,related_topics] = json
    total_nodes = 0 
    if options[0]=='true':
        total_nodes += len(employees)
    if options[1]=='true':
        total_nodes += len(related_topics)
    if options[3]=='true':
        total_nodes += len(clients)
    if options[4]=='true':
        total_nodes += len(orgs)
    if options[5]=='true':
        total_nodes += len(places)
    return total_nodes

# options = [show_employees, show_topics, show_experts, show_clients, show_organizations, show_places]
def generate_js_file(topic,group_number,options):
    global div_x 
    global div_y
    div_y = 800
    div_x = 800

    output_array,json = TopicSearch(topic)
    [clients,employees,places,orgs,related_topics] = json
    [show_employees, show_topics, show_experts, show_clients, show_organizations, show_places] = options

    print employees

    nodes = []
    edges = []

    topic_node = {'id':1,'label':topic,'value':35,'group':group_number,'x':div_x/2,'y':div_y/2}
    nodes.append(topic_node)

    total_nodes = get_total_nodes(options,json)
    random_list = random.sample(range(total_nodes), total_nodes)

    id_counter = 2

    if show_employees=='true':
        for expert,score in employees.iteritems():
            if show_experts=='true' and score<0.52:
                continue
            new_node = generate_node(id_counter,'people',expert,random_list,score)
            nodes.append(new_node)
            edges.append([1,id_counter,score])
            id_counter += 1

    if show_topics=='true':
        for related_topic,score in related_topics.iteritems():
            new_node = generate_node(id_counter,'related_topic',related_topic,random_list,score)
            nodes.append(new_node)
            edges.append([1, id_counter, score])
            id_counter += 1

    if show_clients=='true':
        for client,score in clients.iteritems():
            new_node = generate_node(id_counter,'client',client,random_list,score)
            nodes.append(new_node)
            edges.append([1,id_counter,score])
            id_counter += 1

    if show_organizations=='true':
        for org,score in orgs.iteritems():
            new_node = generate_node(id_counter,'organization',org,random_list,score)
            nodes.append(new_node)
            edges.append([1,id_counter,score])
            id_counter += 1

    if show_places=='true':
        for place,score in places.iteritems():
            new_node = generate_node(id_counter,'place',place,random_list,score)
            nodes.append(new_node)
            edges.append([1,id_counter,score])
            id_counter += 1

    nodes_string = get_node_string(nodes)
    edges_string = get_edge_string(edges)

    text_file = open("static/vendors/visjs/datasource/"+topic+".js", "w+")
    text_file.write(nodes_string+"\n"+edges_string)
    text_file.close()

def generate_node(id_counter,node_type,label,random_list,similarity_score):
    new_node = {}
    new_node['id'] = id_counter
    new_node['label'] = label
    node_value = 10
    group_number = 1;
    if node_type=='people':
        group_number = 2

    if node_type=='client':
        group_number = 3

    if node_type=='related_topic':
        group_number = 4

    if node_type=='organization':
        group_number = 5

    if node_type=='place':
        group_number = 6

    new_node['value'] = node_value
    new_node['group'] = group_number
    angle = (2 * pi * (random_list[id_counter - 2])) / len(random_list)
    x, y = point_on_circle(angle, similarity_score)
    new_node['x'] = x
    new_node['y'] = y
    return new_node

def get_node_string(nodes):
    string = "var nodes = [\n"
    for node in nodes:
        string = string+ "\t" + str(node) +",\n"
    string = string + "];"
    return string

def get_edge_string(edges):
    string = "var edges =[\n"
    for edge in edges:
        string = string + "\t{from: "+str(edge[0])+", to: " + str(edge[1]) + ", title:\'Similarity Score: "+str(round(edge[2]*100,3))+"%\'},\n"
    string = string + "];"
    return string

def point_on_circle(angle,score):
    center = [div_x/2,div_y/2]
    radius = -((3*div_x)/8)*score + (div_x/2 - 25)
    x = center[0] + (radius * cos(angle))
    y = center[1] + (radius * sin(angle))
    return x,y


def get_js_file_org(org_name,json):
    global div_y 
    global div_x
    div_y = 400
    div_x = 600

    [Clients,Enron_People,places,related_topics] = json
    total_nodes = len(Clients) + len(Enron_People) + len(places) + len(related_topics)
    random_list = random.sample(range(total_nodes), total_nodes)
    print "--------------"
    print random_list

    nodes = []
    edges = []

    org_node = {'id':1,'label':org_name,'value':35,'group':1,'x':div_x/2,'y':div_y/2}
    nodes.append(org_node)

    id_counter = 2
    for client,score in Clients.iteritems():
        new_node = generate_node(id_counter,'client',client.encode("utf-8"),random_list,score)
        nodes.append(new_node)
        edges.append([1,id_counter,score])
        id_counter += 1

    for people,score in Enron_People.iteritems():
        new_node = generate_node(id_counter,'people',people.encode("utf-8"),random_list,score)
        nodes.append(new_node)
        edges.append([1,id_counter,score])
        id_counter += 1

    for place,score in places.iteritems():
        new_node = generate_node(id_counter,'place',place.encode("utf-8"),random_list,score)
        nodes.append(new_node)
        edges.append([1,id_counter,score])
        id_counter += 1

    for related_topic,score in related_topics.iteritems():
        new_node = generate_node(id_counter,'related_topic',related_topic.encode("utf-8"),random_list,score)
        nodes.append(new_node)
        edges.append([1,id_counter,score])
        id_counter += 1

    nodes_string = get_node_string(nodes)
    edges_string = get_edge_string(edges)

    text_file = open("static/vendors/visjs/datasource/"+org_name+".js", "w+")
    text_file.write(nodes_string+"\n"+edges_string)
    text_file.close()
