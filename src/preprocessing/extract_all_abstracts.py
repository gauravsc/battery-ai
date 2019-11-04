import csv
import os

base_url = './data/abstracts/'
abstracts_files = os.listdir(base_url)
fwrite = open('./data/abstracts.txt','w')

def get_all_eids_downloaded():
	eids = {}
	for file in abstracts_files:
		with open('./data/abstracts/'+file, 'r') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				eids[row['EID']] = 1

	return eids


eids_extracted = {}

for file in abstracts_files:
	with open('./data/abstracts/'+file, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['EID'] in eids_extracted:
				continue
			else:
				eids_extracted[row['EID']] = 1
				fwrite.write(row['Abstract'])
				fwrite.write('\n\n')

