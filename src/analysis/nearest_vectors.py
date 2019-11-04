import src.utils.embedding_operations as eoper
import numpy as np

# top k similar words
topk = 1000

# words whose nearest neighbours need to be searched
words_to_search = ["cathode", "anode"]

# extract the vocab and the embedding matrix from the word vector file
print ("loading embeddings .....")
vocab, word_to_ind, emb_mat = eoper.read_embeddings()
print ("done loading embeddings .....")

# normalize the embedding matrix
row_sums = np.sqrt(np.square(emb_mat).sum(axis=1))
emb_mat = emb_mat/row_sums[:, np.newaxis]

for word in words_to_search:
	idx = word_to_ind[word]
	search_vector = emb_mat[idx, :]

	res = np.dot(search_vector, emb_mat.T)
	res_idxs = np.argsort(res)[::-1][:topk]

	print ("Search for words similar to ", word)
	
	for res_idx in res_idxs:
		print (vocab[res_idx]," : ", res[res_idx])

	print ("\n\n\n")
