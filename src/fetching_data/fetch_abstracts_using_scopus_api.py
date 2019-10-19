"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json, requests
import urllib.parse
import os.path
import csv

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
    r = json.loads(r.text)
    return r['abstracts-retrieval-response']['coredata']['dc:description']


def store_eids_and_abstracts(headers, word):
    # all results
    base_url = 'https://api.elsevier.com/content/search/scopus?'
    query = "TITLE-ABS-KEY("+ word +")"
    count = 25
    cursor = '*'

    fieldnames = ['EID', 'URL', 'Title', 'Abstract']
    dict_writer = csv.DictWriter(open('./data/abstracts/'+ word +'.csv', 'w'), fieldnames=fieldnames)
    dict_writer.writeheader()

    params = {
        'query': query,
        'start': '0',
        'view': 'COMPLETE',
        'data': '2008-2018',
        'count': count
        }

    url = base_url+urllib.parse.urlencode(params)
    r = json.loads(requests.get(url, headers = headers).text)
    total_results = int(r['search-results']['opensearch:totalResults'])
    # total_results = 400

    start = 0; rows = []
    while start < total_results - count:
        print (start, "/", total_results)

        params = {
        'query': query,
        'count': count,
        'view': 'COMPLETE',
        'data': '2008-2018',
        'cursor': cursor
        }
# 'field': 'eid,url,title,description',

        url = base_url+urllib.parse.urlencode(params)
        r = requests.get(url, headers = headers)
        results = json.loads(r.text)

        # set cursor to next
        if 'search-results' in results and 'cursor' in results['search-results']:
            cursor = results['search-results']['cursor']['@next']
        
        if 'search-results' in results and 'entry' in results['search-results']:
            for doc in results['search-results']['entry']:
                if 'eid' in doc and 'dc:description' in doc and 'prism:url' in doc and 'dc:title' in doc:
                    rows.append({'EID':doc['eid'], 'URL':doc['prism:url'], 'Title':doc['dc:title'], 'Abstract':doc['dc:description']})
        else:
            print (results.keys(), results)

        # eids.append([doc['eid'] for doc in results['search-results']['entry']])
        start += count
        print ("# of rows written", len(rows))
        dict_writer.writerows(rows)
        rows = []

        # find out quota limits
        print ("X-RateLimit-Limit: ", r.headers['X-RateLimit-Limit'])
        print ("X-RateLimit-Remaining: ", r.headers['X-RateLimit-Remaining'])
        print ("X-RateLimit-Reset: ", r.headers['X-RateLimit-Reset'])


#  words_to_search = ['Electrochemical', 'electrochemistry', 'optoelectronic properties',
# 'functional materials', 'nanostructures', 'theroelectrics', 'thermoelectricity', 
# 'metal oxides', 'conducting metal oxides', 'battery materials', 'photovoltaic materials',
# 'semiconductor materials', 'electrolytes', 'cathode materials', 'anode materials', 
# 'organic semiconductors', 'inorganic semiconductors', 'organic electronics', 'Energy storage']


with open('./src/search_terms.csv', 'r', encoding='utf-8-sig') as content_file:
    words_to_search = content_file.read()
    words_to_search = words_to_search.strip().split('\n')
    words_to_search = [word.strip().lower() for word in words_to_search]    

print (words_to_search)

headers = {
            "X-ELS-APIKey"  : config['apikey'],
            "Accept"        : 'application/json'
            }

for word in words_to_search:
    if os.path.isfile('./data/abstracts/'+word+'.csv'):
        # this words has already been extracted
        continue
    
    print ("Word being searched: ", word)
    store_eids_and_abstracts(headers, word)
