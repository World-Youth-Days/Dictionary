# -*- coding: utf-8 -*-
import dataset
from sqlalchemy import Integer, DateTime, String
import datetime


def query_from_dict(dic, table="words", operator="AND"):
	"""

	:param dic: dict: FIND query arguments
	:param table: str: table to search in
	:param operator: str: AND/OR to put between dic elements
	:return: str: string with SQL query
	"""
	c = operator.strip() + " "
	q = "SELECT * FROM " + table + "\nWHERE "
	for key in dic:
		q += key + "='" + str(dic[key]) + "'\n" + c

	return q[0:-len(c) - 1] + ";"  # remove last conjuncton


class DbAdapter:
	# --------------------------------------------------------------------#
	# ------------------ Manage database, get reference ------------------#
	# --------------------------------------------------------------------#

	def __init__(self, path_file=None, os="Linux"):
		if path_file is None and os == "Windows":
			self.db = dataset.connect(r'sqlite:///\..\dictionary.db')
			print("Base opened!")
		elif path_file is None:
			self.db = dataset.connect('sqlite:///../dictionary.db')
			print("Base opened!")
		else:
			self.db = dataset.connect('sqlite:' + path_file)
		# ought to add try-catch here

		self.new_word = {'base': None, 'mono': "", 'trans': "", 'level': 0, 'author': None,
		                 'time': 0}
		
		self.tags = self.db.get_table("tags")
		# initialize columns with non typical value types
		self.tags.create_column('readable', String)
		self.tags.create_column('flag', String)

		self.words = self.db.get_table("words")
		self.words.create_column('time', DateTime)
		self.words.create_column('level', Integer)

	def backup(self):
		print("No backup utility so far...")
		return 1

	def get_table(self, name=None):
		if name is None:
			return self.db.tables
		else:
			return self.db.get_table(name)

	def unify(self):
		# check tag's id's integrity with words
		self.update_tags()
		for tag in self.tags:
			for word in tag:
				if len(self.words.find(id=word)) == 0:
					print("No word found: " + word)
					self.db[tag].delete(word_id=word)
		
		self.update_tags()
		self.remove_without_tag()

	# --------------------------------------------------------------------#
	# ---------------------------- Manage tags ---------------------------#
	# --------------------------------------------------------------------#

	def join(self, word_list, tag_list):
		for item in [word_list, tag_list]:
			if type(item) != list:
				item = [item]  # make sure they're both iterable

		for tag in tag_list:
			if tag is '':
				continue
			for word in word_list:

				if self.get_dic(word) is None:  # check for existence...
					print('Warning: no word with such id!!! ' + word)
					continue
				else:
					r = dict(word_id=word, base=self.get_dic(word)['base'])

				self.get_table(tag).insert(r)

		self.update_tags()
	
	def disjoin(self, word_list, tag_list):
		for tag in tag_list:
			for word in word_list:
				if tag in self.db["tags"]:
					self.db[tag].delete(id=word)

		self.update_tags()

	def update_tags(self):
		tags = self.db.tables[:]
		tags.remove("words")
		tags.remove("tags")
		self.tags.delete()  # remove all old tag names
		for tag in tags:
			if len(tag) == 0:
				self.db[tag].drop()  # delete >table< from db
				continue
			
			self.tags.insert(dict(tag_name=tag))

	def set_readable(self, name, readable):
		if self.tags.count(tag_name=name) is not 0:
			self.tags.upsert(
				dict(tag_name=name, flag=self.get_tag(name)['flag'], readable=readable),
				['tag_name'])
		else:
			print("Error, no such tag in tags: " + str(name))

	def set_flag(self, name, flag):
		if self.tags.count(tag_name=name) is not 0:
			self.tags.upsert(
				dict(tag_name=name, flag=flag, readable=self.get_tag(name)['readable']),
				['tag_name'])
		else:
			print("Error, no such tag in tags: " + str(name))

	def get_tag(self, name):
		l = [t for t in self.tags.find(tag_name=name)]
		return l[0]

	# --------------------------------------------------------------------#
	# ------------------------- Manage words -----------------------------#
	# --------------------------------------------------------------------#S

	# Need to add creation-time support!!!!  ##

	def add_words(self, records):
		""":argument records list"""
		count = len(self.words)

		# make sure it's iterable
		if not isinstance(records, list):
			records = [records]

		for r in records:
			# add current time, with accuracy to 1 minute
			r['time'] = datetime.datetime.today().replace(second=0, microsecond=0)
			# print( "Time: " + str(r['time']))
			self.words.upsert(r, ['base', 'author', 'trans', 'mono', 'level'])
		# adding level to this list causes strange crash...
		
		# have some statistic idea about what's happened ;)
		delta = len(self.words) - count
		print("Added " + str(delta) + " new words; updated " + str(len(records) - delta) + ".")

	def remove_without_tag(self):
		# get complete list of words, then remove every with tag
		id_list = self.get_id_list()
		for tag in self.tags:
			for word in tag:
				try:
					id_list.remove(word['word_id'])
				except ValueError:
					continue  # no word with such id, normal case

				# remove words which stayed on list
		for word_id in id_list:
			self.words.delete(id=word_id)

		print('Removed ' + str(len(id_list)) + ' words without any tag.')
		self.unify()

	def remove_by_id(self, id_list):
		if not isinstance(id_list, (list, tuple)):
			id_list = [id_list]

		count = len(self.words)
		for word in id_list:
			self.words.delete(id=word)

		delta = count - len(self.words)
		print('Removed ' + str(delta) + ' words.')
		
		# try to find recently deleted words to give list of errors?
		self.unify()

	def remove_by_tag(self, tag):

		count = len(self.words)
		for Id in self.tags[tag]:
			self.words.delete(id=Id)

		print('Removed ' + str(count - len(self.words)) + 'words')

	# --------------------------------------------------------------------#
	# ---------------------------- Search --------------------------------#
	# --------------------------------------------------------------------#

	# need to adapt db.query() in self.find()

	def find_dic(self, dic):
		""":return : list[OrderedDict]"""
		q = query_from_dict(dic)
		return [d for d in self.db.query(q)]

	def find_id(self, dic):
		""":rtype: list"""
		q = query_from_dict(dic)
		return sorted([row['id'] for row in (self.db.query(q))])

	def get_dic(self, _id):
		""":rtype OrderedDict"""
		res = self.words.find(id=_id)
		for r in res:
			return r

		return None

	def get_id_list(self):
		""":rtype: list"""

		id_list = []
		# @type : list
		for word in self.words:
			id_list.appednd(word['id'])
		return id_list

	def search_with_tags(self, tags):

		if type(tags) != list:
			tags = [tags]
		ls = self.db[tags[0]].all()['word_id']
		for tag in tags[1:]:
			for row in tag:
				if row['word_id'] in ls:
					continue
				else:
					ls.remove(row['word_id'])
		
		return ls

# -------------------------------------------------------------------#
# -----------------      Testing purposes only!!  -------------------#
# ----------------- This is a class-file, no runs -------------------#
# -------------------------------------------------------------------#


# db = DbAdapter()
# print db.query_from_dict(dict(name='John Doe', age=46, #country='China'))


# --------------------------------------------------------------------#
# ------------------      Additional ideas        --------------------#
# --------------------------------------------------------------------#


# def additional():
#	return None
#	#remove element from list:
#	while el in lst:
#		lst.remove(el)
#		
#	# Insert a new record.
#	table.insert(dict(name='John Doe', age=46, country='China'))
