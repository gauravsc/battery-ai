import json, requests
import urllib.parse
import os, os.path
from random import shuffle
import csv


## Load configuration
con_file = open("./config/config.json")
config = json.load(con_file)
con_file.close()

## init headers 
headers = {
			"X-ELS-APIKey"  : config['apikey'],
			"Accept"        : 'application/json'
			}

def retrieve_abstracts(headers, eid):
	url = 'https://api.elsevier.com/content/abstract/eid/'+eid
	r = requests.get(url, headers = headers)
	results = json.loads(r.text)

	# find out quota limits
	print ("X-RateLimit-Limit: ", r.headers['X-RateLimit-Limit'])
	print ("X-RateLimit-Remaining: ", r.headers['X-RateLimit-Remaining'])
	print ("X-RateLimit-Reset: ", r.headers['X-RateLimit-Reset'])

	return results['abstracts-retrieval-response']['coredata']['dc:description']


def extract_all_eids():
	# extract all the eid files
	base_url = './data/eids/'
	files = os.listdir(base_url)
	
	eids = []
	for file in files:
		eids += json.load(open(base_url+file,'r'))
	eids = list(set(eids))

	shuffle(eids)

	return eids	

eids_to_extract = extract_all_eids() 
print ("Total abstracts to download: ", len(eids_to_extract))

if os.path.isfile('./data/ctr.json'):
	ctr = int(json.loads(open('./data/ctr.json', 'r'))['ctr'])
else:
	ctr = 0

fieldnames = ['EID', 'Abstract']
dict_writer = csv.DictWriter(open('./data/abstracts.txt', 'a+'), fieldnames=fieldnames)
dict_writer.writeheader()

rows = []
for eid in eids_to_extract[ctr:]:
	abstract = retrieve_abstracts(headers, eid)
	print (ctr, "/", len(eids_to_extract))
	rows.append({'EID':eid, 'Abstract':abstract})
	ctr += 1

	if ctr % 10000 == 0:
		json.dump({'ctr':ctr}, open('./data/ctr.json', 'w'))
		# fwrite.write("/n".join(abstracts))
		dict_writer.writerows(rows)
		rows = []

