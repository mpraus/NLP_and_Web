import pandas as pd
import spacy
from spacy.attrs import LOWER, POS
from spacy.matcher import Matcher


df = pd.read_csv("evaluation_examples_backup.csv", sep=',', header=None)
nlp = spacy.load('en_core_web_sm')
df["tokens"] = df[0].apply(lambda x: nlp(x))
#df["as_array"] = df[0].apply(lambda x : x.to_array([LOWER, POS]))
print(len(df[0]))
matcher = Matcher(nlp.vocab)
pattern = [{POS : {"NOT_IN" : list(("ADJ", "ADV"))}}]
matcher.add("Adj,adv", None, pattern)
for i in range(0, len(df[0])):
	tokens = nlp(df[0].at[i])
	matches = matcher(tokens)
	df["filtered"].at[i] = [tokens[start:end].text for match_id, start, end in matches]
	# print(len(matches))
	# print(set([tokens[start:end].text for match_id, start, end in matches]))
print(df)
print(df.columns)