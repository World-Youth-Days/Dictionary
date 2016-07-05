# -*- coding: utf-8 -*-
import datetime
import dataset
import logging
from sqlalchemy import Integer, DateTime, String


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
		q += key + "='" + str(dic[key]).replace('\'', '\'\'') + "'\n" + c

	return q[0:-len(c) - 1] + ";"  # remove last conjuncton

def tag_enhance(tag):
	""":argument tag : OrderedDict"""
	n = tag['tag_name']
	r = tag.get('readable')
	f = tag.get('flag')
	d = tag.get('description')

	if r in [None, '']:
		tag['readable'] = n.replace('_', ' ').title()  # first letter of each word is upper-case

	if f in [None, '']:  # is this needed at all?
		tag['flag'] = 'live'

	if 'to_' in n[:3]:
		tag['flag'] = 'to'

	if 'from_' in n[:5]:
		tag['flag'] = 'from'

	return tag

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
		for k in ['tag_name', 'readable', 'flag', 'description']:
			self.tags.create_column(k, String)

		self.words = self.db.get_table("words")
		self.words.create_column('time', DateTime)
		self.words.create_column('level', Integer)
		self.words.create_column('mono', String)

	def backup(self):
		import codecs, os, hashlib

		try:
			ver_f = codecs.open('../backup/version.txt', "r", 'utf-8')
		except SystemError:
			print("Error while opening version file!")
			return 1

		ver = int(ver_f.readline()) + 1


		os.system('cp ../dictionary.db ../backup/dictionary-'+str(ver)+'.db')
		print( 'New backup file with version {} created!'.format(ver))
		ver_f.close()

		try:
			ver_f = codecs.open('../backup/version.txt', "w", 'utf-8')
		except SystemError:
			print("Error while opening version file!")
		ver_f.write(str(ver))

		ver_f.close()
		return 0

	def backup_version_reset(self, version):
		f = open('../data/version.txt', 'w')
		f.write(str(version))
		f.close()

	def get_table(self, name=None):
		if name is None:
			return self.db.tables
		else:
			return self.db.get_table(name)

	def unify(self):

		"""
			1. Removes words with no tag
			2. Searches for corrupted entries in tag-tables
			3. Removes empty tag-tables. Does enhncing
		"""

		self.remove_without_tag()

		for tag in self.tags:
			for word in self.db['tag']:
				if self.words.count(id=word) == 0:
					print("No word found: " + word)
					self.db[tag].delete(word_id=word['word_id'])
		
		self.update_tags()

		for t in self.db['tags'].find():
			self.tags.upsert(tag_enhance(t), ['tag_name'])

	def update_tag_bases(self):
		for tag in self.tags:
			for record in self.db.get_table(tag['tag_name']):
				word = self.words.find_one(id=record['word_id'])
				if word != None:
					record['base'] = word['base']
					self.db.get_table(tag['tag_name']).upsert(record, ['id'])

	# --------------------------------------------------------------------#
	# ---------------------------- Manage tags ---------------------------#
	# --------------------------------------------------------------------#

	def join(self, word_list, tag_list, check=True):
		if not isinstance(word_list, list):
			word_list = [word_list]  # make sure they're both iterable
		if not isinstance(tag_list, list):
			tag_list = [tag_list]

		for tag in tag_list:
			if tag is '':
				continue

			for word in word_list:

				if check is True:
					if self.get_dic(word) in [[], dict()]:  # check for existence...
						print('Warning: no word with such id!!! ' + word)
						continue
				if self.db[tag.strip()].count(word_id=word) == 0:
				# check if word is already joined with tag...
					r = dict(word_id=word, base=self.get_dic(word)['base'])
					self.get_table(tag).insert(r)
		if check is True:
			self.update_tags()

	def disjoin(self, word_list, tag_list):
		for tag in tag_list:
			for word in word_list:
				if tag in self.db["tags"]:
					self.db[tag].delete(id=word)

		self.update_tags()

	def update_tags(self):
		"""removes empty tags and drops their tables."""
		tags = self.db.tables[:]
		tags.remove("words")
		tags.remove("tags")
		for tag in tags:
			if self.db[tag].count() == 0:
				self.db[tag].drop()  # delete >table< from db
				continue
			
			self.tags.upsert(dict(tag_name=tag), ['tag_name'])

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
				dict(tag_name=name, flag=flag),
				['tag_name'])
		else:
			print("Error, no such tag in tags: " + str(name))

	def set_description(self, name, description):
		if self.tags.count(tag_name=name) is not 0:
			tag = self.get_tag(name)
		else:
			print("Error, no such tag in tags: " + str(name))

		if description != '':
			self.tags.upsert(
				dict(tag_name=name, description=description),
				['tag_name'])


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
			self.words.upsert(r, ['base', 'trans', 'mono', 'level'])
			#author-insensitive because of technical limitation of upsert to take up to four
		# filters...

		# have some statistic idea about what's happened ;)
		delta = len(self.words) - count
		return dict(added=delta, updated=(len(records) - delta))

	def remove_without_tag(self):
		# get complete list of words, then remove every with tag
		id_list = self.get_id_list()
		for tag in self.tags:
			for word in self.db[tag['tag_name'].strip()]:
				try:
					id_list.remove(word['word_id'])
				except ValueError:
					continue  # no word with such id, normal case

				# remove words which stayed on list
		for word_id in id_list:
			self.words.delete(id=word_id)

			logging.info('Removed ' + str(len(id_list)) + ' words without any tag.')

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
			id_list.append(word['id'])
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

