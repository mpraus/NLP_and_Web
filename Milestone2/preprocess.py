import pandas as pd
import spacy

df = pd.read_csv("evaluation_examples.csv", sep=',', header=None)
nlp = spacy.load('en_core_web_sm')
df[0] = df[0].apply(lambda x: nlp(x))
print(len(df[0]))
for i in range(0, len(df[0])):
	tokens = df[0].at[i]
	#print(tokens)
	for token in tokens:
		if token.pos_ in ("ADV", "ADJ"):
			tokens.remove(token)
			#print(token)
print(df)
print(df.columns)