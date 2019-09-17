"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json, requests
import urllib.parse
    
## Load configuration
con_file = open("./config/config.json")
config = json.load(con_file)
con_file.close()

## initialize client
client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']


def retrieve_abstracts(headers, eid):
    url = 'https://api.elsevier.com/content/abstract/eid/'+eid
    r = requests.get(url, headers = headers)
    r = json.loads(r)
    return r['abstracts-retrieval-response']['coredata']['dc:description']


def extract_eids(headers, word):
    # all results
    base_url = 'https://api.elsevier.com/content/search/scopus?'
    query = "TITLE-ABS-KEY("+ word +") PUBYEAR > 2010"
    count = 25

    params = {
        'query': query,
        'start': '0',
        'count': count
        }
    url = base_url+urllib.parse.urlencode(params)
    r = json.loads(requests.get(url, headers = headers).text)
    total_results = int(r['search-results']['opensearch:totalResults'])

    start = 0; eids = []
    while start < total_results - count:
        print (start, "/", total_results)

        params = {
        'query': query,
        'start': start,
        'count': count
        }

        url = base_url+urllib.parse.urlencode(params)
        r = requests.get(url, headers = headers)
        r = json.loads(r.text)
        
        eids.append([doc['eid'] for doc in r['search-results']['entry']])
        start += count

    eids = [eid for sublist in eids for eid in sublist]

    return set(eids)


words_to_search = ['Electrochemical']

# 'electrochemistry', 'optoelectronic properties',
# 'functional materials', 'nanostructures', 'theroelectrics', 'thermoelectricity', 
# 'metal oxides', 'conducting metal oxides', 'battery materials', 'photovoltaic materials',
# 'semiconductor materials', 'electrolytes', 'cathode materials', 'anode materials', 
# 'organic semiconductors', 'inorganic semiconductors', 'organic electronics', 'Energy storage']

headers = {
            "X-ELS-APIKey"  : config['apikey'],
            "Accept"        : 'application/json'
            }


# set of eids to avoid duplication
set_of_eids = set()

for word in words_to_search:
    print ("words being searched: ", word)
    eids = extract_eids(headers, word)
    set_of_eids = set_of_eids.union(eids)


json.dump(list(set_of_eids), open('./data/eids_to_extract.json', 'w'))






# for eid in eids:
#     abstract = retrieve_abstracts(headers, eid)
#     break
