# -*- coding: utf-8 -*-
from Db_adapter import DbAdapter
from dict_display import *

db = DbAdapter(None)
word = dict(base='grzyb')
find = db.find(word, raw=True)
#display_dict(dict(), columns=[u'id', u'mono', u'trans', u'level'], header="Only")
for r in find:
	display_dict(r, columns=[u'id', u'mono', u'trans', u'level'], header=False)
