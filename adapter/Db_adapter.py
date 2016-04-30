# -*- coding: utf-8 -*-
from dataset import *
from sqlalchemy import Integer, DateTime
import datetime

class DbAdapter:

		
#--------------------------------------------------------------------#
#------------------ Manage database, get reference ------------------#
#--------------------------------------------------------------------#


	def __init__(self, path_file=None, os="Linux"):
		if path_file == None and os == "Windows":
			self.db = connect(r'sqlite:///\..\dictionary.db')
			print( "Base oppened!")
		elif path_file == None:
			self.db = connect('sqlite:///../dictionary.db')
			print( "Base oppended!")
		else:
			self.self.db = dataset.connect('sqlite:'+path_file)
		#ought to add try-catch here
			
		self.new_word = dict(base=None, mono="", trans="",
		level=0, author=None, time=0)
		
		self.tags = self.db.get_table("tags")
		self.words = self.db.get_table("words")
		
		#initialize columns with non-tpical value types
		self.words.create_column('time', DateTime)
		self.words.create_column('level', Integer)
		
	def backup(self):
		print( "No backup utility so far...")
		return 1
		
	def get_table(self, name = None):
		if name == None:
			return self.db.tables
		else:
			return self.db.get_table(name)

	def unify(self):
		#check tag's id's integrity with words
		self.update_tags()
		for tag in self.tags:
			for word in tag:
				if len(self.words.find(id=word)) == 0:
					print( "No word found: "+word)
					self.db[tag].delete(word_id=word)
		
		self.update_tags()
		self.remove_without_tag()


#--------------------------------------------------------------------#
#---------------------------- Manage tags ---------------------------#
#--------------------------------------------------------------------#


	def join(self, word_list, tag_list):
		for item in [word_list, tag_list]:
			if type(item) != list:
				item = [item]	#make sure they're both iterable
			
		for tag in tag_list:
			if tag is '':
				continue
			for word in word_list:
			
				if self.get(word) == None: #check for existence...
					print( 'Warning: no word with such id!!! '+word)
					continue
				else:
					r = dict(word_id=word, base=self.get(word)['base'])
					
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
		self.tags.delete() #remove all old tag names
		for tag in tags:
			if len(tag) == 0:
				self.db[tag].drop()	#delete >table< from db
				continue
			
			self.tags.insert(dict(tag_name=tag))


#--------------------------------------------------------------------#
#------------------------- Manage words -----------------------------#
#--------------------------------------------------------------------#

# Need to add creation-time support!!!!  ##


	def add_words(self, records):
		count = len(self.words)
		#make sure it's iterable
		if type(records) != list:
			records = [records]
	
		for r in records:
			r['time'] = datetime.datetime.today().replace(second=0, microsecond=0)
			print( "Time: " + r['time'])
			self.words.upsert(r, ['base', 'author', 'trans', 'mono'])
		#adding level to this list causes strange crash...
		
		#have some statistic idea about what's happened ;)
		delta = len(self.words) - count
		print ("Added "+delta+" new words; updated "
		+len(self.words) - delta +".")
		
	def remove_without_tag(self):
	#get complete list of words, then remove every with tag
		id_list = self.get_id_list()
		for tag in self.tags:
			for word in tag:
				try:
					id_list.remove(word['word_id'])
				except ValueError:
					continue	#no word with such id, normal state
		
		#remove words which haven't been removed
		for word_id in id_list:
			self.words.delete(id=word_id)
			print ("Removed "+len(id_list) +
			" words without any tag.")
		
		self.unify()
		
	def remove_by_id(self, id_list):
		if type(id_list) != list:
			id_list = [id_list]
			count = len(self.words)
		for word in id_list:
			self.words.delete(id=word)
			#check for length change to get detailed info?
		delta = count - len(self.words)
		print("Removed " +delta+ " words; failed or duplicate "+ (len(self.words) - delta)+".")
		
		#try to find recently deleted words to give list of errors?
		self.unify()
			
	def remove_by_tag(self, tag):

		#count = len(self.words)
		for Id in self.tags[tag]:
			self.words.delete(id=Id)
			
				
#--------------------------------------------------------------------#
#---------------------------- Search --------------------------------#
#--------------------------------------------------------------------#

#need to adapt db.query() in self.find()

	def query_from_dict(self, dic, table="words", operator="AND"):
	
		c = operator.strip() + " "
		q = "SELECT * FROM " + table + "\nWHERE "
		for key in dic:
			q += key + "='" + dic[key] + "'\n" + c
	
		return q[0:-len(c)-1] + ";" #remove last conjunction
	
	def find(self, dic, raw="False"):
	
		lis = []
		q = self.query_from_dict(dic)
		if raw is True:
			return self.db.query(q)
		else:
			return [row['id'] for row in self.db.query(q)].sort()

		#for r in self.words.find([key=dic[key] for key in dic]):
			#base=dic['base']
			#	lis = r['id']
			#return lis
		
	def get(self, _id):
		res = self.words.find(id=_id)
		for r in res:
			return r
		return None

	def get_id_list(self):
	
		id_list = []
		for word in self.words:
			id_list.appednd(word['id'])
		return id_list
		
	def search_with_tags(self, tags):
	
		if type(tags) != list:
			tags = [tags]
		ls =  self.db[tags[0]].all()['word_id']
		for tag in tags[1:]:
			for row in tag:
				if row['word_id'] in ls:
					continue
				else:
					ls.remove(row['word_id'])
		
		return ls
		
			
#-------------------------------------------------------------------#
#-----------------      Testing purposes only!!  -------------------#
#----------------- This is a class-file, no runs -------------------#
#-------------------------------------------------------------------#


#db = DbAdapter()
#print db.query_from_dict(dict(name='John Doe', age=46, #country='China'))
			
		
#--------------------------------------------------------------------#
#------------------      Additional ideas        --------------------#
#--------------------------------------------------------------------#


#def additional():
#	return None
#	#remove element from list:
#	while el in lst:
#		lst.remove(el)
#		
#	# Insert a new record.
#	table.insert(dict(name='John Doe', age=46, country='China'))
