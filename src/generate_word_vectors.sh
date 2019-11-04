#!/bin/bash

src/word2vec/trunk/word2vec -train ./data/abstracts.txt -output ./data/word_vectors.txt -size 64 -window 5 -sample 1e-4 -negative 5 -hs 0 -binary 0 -cbow 1 -iter 10