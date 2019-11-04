import numpy as np

def read_embeddings():

	with open('./data/word_vectors.txt', 'r', encoding = 'latin-1') as f:
		data = f.readlines()
	lines = data[1:]

	word_emb_dict = {}

	for line in lines:
		line = line.strip().split(' ')
		word = line[0]
		embedding = [float(v) for v in line[1:]]
		word_emb_dict[word] = embedding

	# fix the vocab and the word2index 		
	vocab = sorted(word_emb_dict.keys())

	word_to_ind = {}
	for i, word in enumerate(vocab):
		word_to_ind[word] = i

	# generate the embedding matrix
	emb_mat = []
	for i in range(len(vocab)):
		emb_mat.append(np.array(word_emb_dict[vocab[i]]))
	emb_mat = np.vstack(emb_mat)

	return vocab, word_to_ind, emb_mat