#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
from scrapy.selector import Selector


# In[4]:


response = requests.get("https://www.fragespiel.com/quiz/training.html")


# In[5]:


# getting categories using scrapy
cat_str = Selector(text=response.text).xpath('//select[@name="kat[]"]/option/text()').getall()
cat_id = Selector(text=response.text).xpath('//select[@name="kat[]"]/option/@value').getall()
categories = { k:x for (k, x) in zip(cat_id, cat_str)}
print(categories)


# In[6]:


levels = { 0: "sehr leicht", 1: "leicht", 2: "mittel", 3:"schwer", 4:"sehr schwer"}


# In[7]:


import json 

def get_questions(category, level):
    data = {"play":True, "kat[]":[category], "level[]":[level], "anzahl":300}
    response = requests.post("https://www.fragespiel.com/quiz/training.html", data=data)
    js_questions = Selector(text=response.text).xpath('//script[3]/text()').get()
    json_questions = js_questions.split("json\' : \'")[1].split("\',")[0]
    return json.loads(json_questions)


# In[12]:


questions = {"questions":[]}
for cat in categories:
    for level in levels:
        got_new_questions = True
        qids = []
        retries = 5
        while got_new_questions:
            qs = get_questions(cat, level)
            new_questions = []
            for q in qs["questions"]:
                # Skip question if it is already known
                if not q['id'] in qids:
                    # add category and level info
                    q["category"] = cat
                    q["level"] = level
                    # remove weird number
                    q["a"] = q["a"][0]
                    q["b"] = q["b"][0]
                    q["c"] = q["c"][0]
                    q["d"] = q["d"][0]
                    new_questions.append(q)
            questions["questions"] = questions["questions"] + new_questions
            qids += [q['id'] for q in new_questions]
            # if there are less than 150 questions, we dont need to request more than once
            if len(qids) < 150:
                got_new_questions = False
            else:
                got_new_questions = len(new_questions) > 0 or retries > 0
                if len(new_questions) == 0:
                    retries -= 1
        print(categories[cat], " -- ", levels[level], " -- ", len(qids))


# In[17]:


questions = questions["questions"]
print(len(questions))


# In[18]:


# There are duplicates, remove them from the category with highest amount of questions
import numpy as np

# category frequency
cats_dict = {}
for q in questions:
  if q['category'] in cats_dict:
    cats_dict[q['category']] += 1
  else:
    cats_dict[q['category']] = 1


unique_ids = {}

deleted_cats = np.zeros(max([int(c) for c in categories.keys()]))

for i,q in enumerate(questions):
  qid = q["id"]
  if qid in unique_ids:
    # found a duplicate, check which duplicate to remove based on category frequency
    other_i = unique_ids[qid]
    if cats_dict[q["category"]] < cats_dict[questions[other_i]["category"]]:
      unique_ids[qid] = i 
      deleted_cats[int(questions[other_i]["category"])] += 1
      cats_dict[questions[other_i]["category"]] -= 1
    else:
      unique_ids[qid] = other_i
      deleted_cats[int(q["category"])] += 1
      cats_dict[q["category"]] -= 1
  else:
    unique_ids[qid] = i

for i,n in enumerate(deleted_cats):
  if n > 0:
    print("deleted", n, "from", categories[str(i)])
questions = [questions[i] for i in unique_ids.values()]


# In[19]:


print(len(questions))


# In[30]:


# Replace HTML entities with unicode
import html
for q in questions:
    for s in ["title","a","b","c","d"]:
        q[s] = html.unescape(q[s])


# In[31]:


with open('questions.json', 'w', encoding='utf8') as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)


# Check if the same request produces different answers when there are more than 150 questions

# In[17]:


test_cat = 18
test_lvl = 2
qs1 = get_questions(test_cat, test_lvl)
ids1 = [q['id'] for q in qs1['questions']]
qs2 = get_questions(test_cat, test_lvl)
ids2 = [q['id'] for q in qs2['questions']]
print('The number of intersecting elements is: ',len(set(ids1) & set(ids2)))


# In[ ]:





# That is good because now we can just pull random requests until we get no new questions

# In[ ]:




