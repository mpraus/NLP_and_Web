import json
import spacy
import requests
import html2text
from spacy.attrs import LOWER, POS
from spacy.matcher import Matcher
import wikipediaapi
import wikipedia as wiki

de_wiki = wikipediaapi.Wikipedia('de') # load german wikipedia
wiki.set_lang("de")
session = requests.Session()
def wiki_search(query, parse_html=True):
  url = "https://de.wikipedia.org/w/api.php"
  params = {
      "action": "query",
      "format": "json",
      "list": "search",
      "srlimit": 25,
      "srsearch": query
  }

  response = session.get(url=url, params=params)
  data = response.json()

  if parse_html:
    for sr in data['query']['search']:
      sr["title"] = sr["title"]
      sr["snippet"] = html2text.html2text(sr["snippet"])

  return data['query']['search']


fragewoerter = ['Wie', 'Wo', 'Wer', 'Wann', 'Wem', 'Wen', 'Woher', 'Was', 'Welche']
count = 0
w_fragen = []
nlp = spacy.load("de_core_news_sm")
file = open("questions.json", "r")
questions = json.load(file)
print(questions[0])
for question in questions:
	# if question['title'].split()[0] in fragewoerter:
	# 	count += 1
	# 	w_fragen.append(question)
	if question['category'] == '8':
		if question['level'] == 2:
			w_fragen.append(question)
			count+=1
	# text = nlp(question['title'])
	# for token in text:
	# 	print(token.tag_)
print(count)
print(count/len(questions))
print(len(w_fragen))

matcher = Matcher(nlp.vocab)
pattern = {POS : {"IN" : ("NOUN", "PROPN")}, "IS_STOP" : False}
matcher.add("pattern", None, [pattern])

print(w_fragen[2])
print(w_fragen[0]['title'])
tokens = nlp(w_fragen[0]['title'])
print(tokens)
for token in tokens:
	print(token.tag_)
matches = matcher(tokens)
tokens_filtered = list([tokens[start:end].text for match_id, start, end in matches])
print(tokens_filtered)
print(" ".join(tokens_filtered))
result = wiki_search(" ".join(tokens_filtered))
print(len(result))
for x in result:
	print()
	print(x)
	print()
print(result[2]['text'])
answers = ["a", "b", "c", "d"]
for answer in answers:
	test = w_fragen[0][answer]
	if test in result:
		print(test)