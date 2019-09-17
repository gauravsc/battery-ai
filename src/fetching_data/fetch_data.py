"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json, requests
    
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


def extract_eids(word):
    #   all results
    doc_srch = ElsSearch("TITLE-ABS-KEY("+ word +") PUBYEAR > 2018",'scopus')
    doc_srch.execute(client, get_all = True)
    print ("doc_srch has", len(doc_srch.results), "results.")
    print (doc_srch.results)

    # extract all the eids
    eids = [doc['eid'] for doc in doc_srch.results]

    return set(eids)


words_to_search = ['Electrochemical']

# 'electrochemistry', 'optoelectronic properties',
# 'functional materials', 'nanostructures', 'theroelectrics', 'thermoelectricity', 
# 'metal oxides', 'conducting metal oxides', 'battery materials', 'photovoltaic materials',
# 'semiconductor materials', 'electrolytes', 'cathode materials', 'anode materials', 
# 'organic semiconductors', 'inorganic semiconductors', 'organic electronics', 'Energy storage']



# set of eids to avoid duplication
set_of_eids = set()

for word in words_to_search:
    print ("words being searched: ", word)
    eids = extract_eids(word)
    set_of_eids = set_of_eids.union(eids)


json.dump(list(set_of_eids), open('./data/eids_to_extract.json', 'w'))









# headers = {
#             "X-ELS-APIKey"  : config['apikey'],
#             "Accept"        : 'application/json'
#             }


# for eid in eids:
#     abstract = retrieve_abstracts(headers, eid)
#     break
