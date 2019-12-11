import pandas as pd
import numpy as np
import spacy
from spacy.attrs import LOWER, POS
from spacy.matcher import Matcher
from sklearn.feature_extraction.text import TfidfVectorizer


nlp = spacy.load('en_core_web_sm')

def filter(patterns, sentence):
	matcher = Matcher(nlp.vocab)
	i = 0
	for pattern in patterns:
		matcher.add(str(i), None, [pattern])
		i+=1
	#matcher.add("Adj,adv", None, pattern)
	tokens = nlp(sentence)
	matches = matcher(tokens)
	tokens_filtered = list([tokens[start:end].text for match_id, start, end in matches])
	return tokens_filtered

def matching():
	df = pd.read_csv("evaluation_examples_backup.csv", sep=',', header=None)
	df["tokens"] = df[0].apply(lambda x: nlp(x))
	patterns = []
	# pattern_adj = {POS : {"NOT_IN" : list(("ADJ", "ADV"))}}
	# patterns.append(pattern_adj)

	# pattern_adj_stop = {POS : {"NOT_IN" : list(("ADJ", "ADV"))}, "IS_STOP" : False}
	# patterns.append(pattern_adj_stop)

	# pattern_stop = {"IS_STOP" : False}
	# patterns.append(pattern_stop)

	# pattern_verb = {POS : {"NOT_IN" : "VERB"}}
	# patterns.append(pattern_verb)

	# pattern_noun = {POS : "NOUN"}
	# patterns.append(pattern_noun)

	# pattern_propn = {POS : "PROPN"}
	# patterns.append(pattern_propn)

	# pattern_prop_n = {POS : {"IN" : ("NOUN", "PROPN")}}
	# patterns.append(pattern_prop_n)

	pattern_noun_stop = {POS : {"IN" : ("NOUN", "PROPN")}, "IS_STOP" : False}
	patterns.append(pattern_noun_stop)

	# pattern_verb = {POS : "VERB"}
	# patterns.append(pattern_verb)

	# pattern_noun_sym = {POS : {"IN" : "NOUN, SYM"}}
	# patterns.append(pattern_noun_sym)

	# pattern_punct = {"IS_PUNCT" : False}
	# patterns.append(pattern_punct)
	print(patterns)

	df["filtered"] = df[0].apply(lambda x :filter(patterns, x))

	df[0] = df["filtered"]
	df = df.drop(columns = ["tokens", "filtered"])
	print(df)
	df.to_csv("evaluation_examples.csv", header=False, index=False, index_label=False)

def tf_idf():
	df = pd.read_csv("evaluation_examples_backup.csv", sep=',', header=None)
	vectorizer = TfidfVectorizer()
	matrix = vectorizer.fit_transform(open("evaluation_examples_backup.csv"))
	print(matrix.shape)
	print(len(vectorizer.get_feature_names()))
	print(matrix.max())
	for i in matrix:
		print("TEST")
		test = i > 0.4
		print(i)
		print("test2")
		print(test)
	file = open("matrix", 'w')
	matrix = matrix.toarray()
	file.write("\n".join(str(elem) for elem in matrix))
	file.close();
	return -1

matching()