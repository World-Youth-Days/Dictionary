# -*- coding: utf-8 -*-
from DbAdapter import DbAdapter
from display_dict import display_dict

db = DbAdapter(None)
word = { 'level': 10, 'base': 'grzyb', 'author': 'francuski', 'trans': 'un champigon'}
find = db.find_dic(word)
words = []
for word in find:
	words.append(word)
#display_dict(dict(), columns=[u'id', u'mono', u'trans', u'level'], header="Only")
display_dict(words, columns=['id', 'base', 'trans', 'level', 'author'], header=True)
