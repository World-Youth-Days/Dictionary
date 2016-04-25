# -*- coding: utf-8 -*-
import os, sys
import codecs
from Db_adapter import DbAdapter


#--------------------------------------------------------------------#
#--------------------------   Open file     -------------------------#
#--------------------------------------------------------------------#


def insert_from_file_line_is_record(path_name, delimiter = ',', **kwargs):
	records = []
	tags_pos = None, 
	
	try:
		f = codecs.open(path_name, "r", 'utf-8')
	except:
		print "Error while opening file!"
		return 4
	print "\nFile: " + path_name + "\n"
	
	rows = ['base', 'mono', 'trans', 'author', 'level']
	pos = dict(base=None, mono=None, trans=None, author=None, level=None)		#sorry, I avoid understanding deep/shalow copy specs ;)
	const = dict()
	
	
#--------------------------------------------------------------------#
#----------------------    Examine header   -------------------------#
#--------------------------------------------------------------------#


	header = f.readline().strip().split(delimiter)
	print "Header: " + str(header)
	print "Kwargs: " + str(kwargs)
	
	for col in rows:
		if col in kwargs:
			const[col] = kwargs[col]
			print "OK: Const " + col + " found"
	
		
				
		try:
			pos[col] = header.index(col)
			print "OK: " + col + " at column " + str(pos[col])
		except ValueError:
			print "Info: No "+ str(col) +" header found"
			del pos[col]
			
	if 'tags' in kwargs:	#find sources of tags
		const_tags = kwargs['tags'].split(',')
	else:
		const_tags = None
	if 'tags' in header:
		tags_pos = header.index('tags')
	
	print "pos: " + str(pos)
	print "const: " + str(const)
	print "const_tags: " + str(const_tags)
	print "tags_pos: " + str(tags_pos)
	

#--------------------------------------------------------------------#
#------------------   Check for integrity      ----------------------#
#--------------------------------------------------------------------#


	if len(pos) + len(const) < 4:
		print "Error: Insufficient information provided to fill all columns."
		return 2
		
	if pos['base'] == None:
		print "Warning: No base-word, assuming 0-th column as base"
		pos['base'] = 0
		
	if 'trans' not in pos and 'mono' not in pos:
		print "Error: Neither monolingual nor translation defined, error!"
		return 1
		
	if (tags_pos == None) and const_tags == None:
		print "Error: No tags provided!"
		return 3
	

#--------------------------------------------------------------------#
#----------------------    Build records    -------------------------#
#--------------------------------------------------------------------#


	for line in f:
		d = dict()
		line = line.strip().split(delimiter)
		for key in const:
			d[key] = const[key]
		for key in pos:		#constant values CAN be overrriden by those 									taken directly from table (^-^)
			d[key] = line[pos[key]]
			
		records.append(d)
		
	#need to print records in purpose of confirmation by human...
	for r in records:
		print r


#--------------------------------------------------------------------#
#----------------------    Human check ;)   -------------------------#
#--------------------------------------------------------------------#


	if "force_yes" in kwargs and kwargs["force_yes"] == True:
		print "Automatic yes choosen..."
	elif raw_input("Are those OK? (don't care about special chars) [y/n]") is not 'y':
		print "Aborting..."
		return 5
		
	db = DbAdapter(None)					#define db connection
	db.add_words(records)
	

#--------------------------------------------------------------------#
#----------------------     Add tags        -------------------------#
#--------------------------------------------------------------------#

#--------need to add remove-# feature
	
	ids = []
	for r in records:	#add const_tags
		ids.append(db.find(r)[0])
		#I'm pretty sure to find one record here...
		
	if const_tags is not None:
		db.join(ids, const_tags)
		print "Joined all with tags: "+str(const_tags)
	
	
	f.seek(0)	#start new reading, skip header
	f.readline()
	i = 0
	
	if tags_pos is not None:
		for line in f:		#add tags form tags_pos
			line = line.strip().split(delimiter)
			if len(line[tags_pos:]) > 0:	#do sth about empty u''
				db.join( db.find(records[i]), line[tags_pos:] )
				print "Joined "+ str(db.find(records[i])) + "with tags "+str(line[tags_pos:])
			i += 1
	
	print "Closing..."	
	f.close()
	
	
	
#--------------------------------------------------------------------#
#----------------------    Call the function-------------------------#
#--------------------------------------------------------------------#

#li.index("example")	
	
insert_from_file_line_is_record("../data/test1.txt", author="francuski", tags="const_tag_1", level=10, force_yes=False)

insert_from_file_line_is_record("../data/test2.txt", author="angielski", level=4, force_yes=True)

insert_from_file_line_is_record("../data/test3.txt", author=u"śmieszek", force_yes=False)







