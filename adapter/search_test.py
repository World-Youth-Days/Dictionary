# -*- coding: utf-8 -*-
from Db_adapter import DbAdapter
from dict_display import *

db = DbAdapter(None)
word = dict(base='grzyb')
find = db.find(word, raw=True)
words = []
for word in find:
	words.append(word)
#display_dict(dict(), columns=[u'id', u'mono', u'trans', u'level'], header="Only")
display_dict(words, columns=['id', 'mono', 'trans', 'level'], header=True)
