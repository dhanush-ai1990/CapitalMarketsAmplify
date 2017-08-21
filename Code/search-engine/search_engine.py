import bottle
from bottle import *
import urllib
import urllib2
import sys, json, requests
from QueryWord2Vec import *
from topic_cluster_graph import *
import cgi, cgitb 

@route('/hello')
def hello():
    return "Hello World!"

@bottle.get('/')
def index():
	return bottle.redirect('index.html')

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@route('/search', method='GET')
def submit_form():
	query = request.query.get('query')
	searchArea = request.query.get('searchArea')

	if searchArea == None:
		searchArea =[]
	else:
		searchArea = [searchArea]
		
	result = GeneralSearch(query,searchArea)
	print "---------------------"
	print result
	return template('SearchResult.html', result =result, query=query)

@bottle.get('/profile/<name>')
def personal_page_viwer(name):
	name = name.split('+')
	name = ' '.join(name)

	result,nodes,edges = PeopleSearch(name)
	print result
	[name,organization,email,expertise,interests] = result

	info = {
	'name': name,
	'organization': organization,
	'email': email,
	'interests': interests,
	'expertise': expertise
	}
	return template('Profile.html', info)

@bottle.get('/client/<name>')
def client_page_viwer(name):
	try:
		name = name.split('+')
		name = ' '.join(name)
		org_result,json = OrgSearch(name)
		[name,org_type,description,link,image,interests,top_from_company,top_from_enron,places] = org_result
		get_js_file_org(name,json)

		info = {'name': name,
		'link': link,
		'logo': image,
		'orgType': org_type,
		'description': description,
		'top_from_company': top_from_company,
		'top_from_enron': top_from_enron,
		'interests': interests
		}
		return template('client.html', info)
	except:
		abort(404, "The data you are looking for is not in our database")

@bottle.get('/topic/<name>')
def topic_page_viwer(name):
	try:
		generate_js_file(name,1,['true','true','false','false','false','false'])
		return template('topic.html',topic=name)
	except:
		abort(404, "The data you are looking for is not in our database")

@route('/topic', method='POST')
def ajaxtest():
	show_people = request.forms.get('showPeople')
	show_topics = request.forms.get('showTopics')
	show_experts = request.forms.get('showExperts')
	show_clients = request.forms.get('showClients')
	show_organizations = request.forms.get('showOrgs')
	show_places = request.forms.get('showPlaces')

	options = [show_people,show_topics,show_experts,show_clients,show_organizations,show_places]
	topic_name = request.forms.get('topic_name').strip()
	generate_js_file(topic_name,1,options)
	print 'done'
	return

@bottle.get('/<path:path>')
def html_pages(path):
	return bottle.static_file(path, root='')

from bottle import error
@error(404)
def error404(error):
    return 'Nothing here, sorry'
    # abort(404, "No such database.")


run(host='localhost', port=8080, debug=True)