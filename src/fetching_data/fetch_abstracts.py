import json, requests
import urllib.parse
import os, os.path
from random import shuffle

## Load configuration
con_file = open("./config/config.json")
config = json.load(con_file)
con_file.close()

## initialize client
client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']

## init headers 
headers = {
            "X-ELS-APIKey"  : config['apikey'],
            "Accept"        : 'application/json'
            }

def retrieve_abstracts(headers, eid):
    url = 'https://api.elsevier.com/content/abstract/eid/'+eid
    r = requests.get(url, headers = headers)
    results = json.loads(r.text)

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

fwrite = open('./data/abstracts.txt', 'a+')

if os.path.isfile('./data/ctr.json'):
	ctr = int(json.loads(open('./data/ctr.json', 'r'))['ctr'])
else:
	ctr = 0

abstracts = []
for eid in eids[ctr:]:
    abstract = retrieve_abstracts(headers, eid)
    abstracts.append(abstract)
	ctr += 1

	if ctr % 10000 == 0:
		json.dump({'ctr':ctr}, open('./data/ctr.json', 'w'))
		fwrite.write("/n".join(abstracts))
		abstracts = []

