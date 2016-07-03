# -*- coding: utf-8 -*-
import codecs
import logging
import sys

from DbAdapter import *
from display_dict import *

db = DbAdapter(None)  # open db connection
printable = []  # here place all processed records
rows = ['base', 'mono', 'trans', 'author', 'level']
pos = dict()  # dict with positions in file
const = dict()  # dict with const values
tags_info = []
VERSES = True


def zero():
	global printable, pos, const
	printable = []
	pos = dict()
	const = dict()


def examine_sources(header, **kwargs):
	# --------need to add remove-# feature

	"""find pos and const in file and kwargs"""
	""":arg : header : list(str)"""
	logging.info("Header: " + str(header))

	global rows, pos, const

	for col in rows:
		if col in kwargs:
			const[col] = kwargs[col]
			logging.info("OK: Const " + col + " found")

		try:
			pos[col] = header.index(col)
			logging.info("OK: " + col + " at column " + str(pos[col]))
		except ValueError:
			logging.info("Info: No " + col + " header found")

	if 'tags' in header:
		pos['tags'] = header.index('tags')
	if 'tags' in kwargs:
		# const['tags'] = []      # if needed #issue
		const['tags'] += kwargs['tags'].strip().split(',')
		if '' in const['tags']:
			const['tags'].remove('')
		# override plain string with table

	return 0


def check_sources():
	if len(pos) + len(const) < 4:
		logging.error("Error: Insufficient information provided to fill all columns.")
		return 1

	if 'base' not in pos:
		logging.warning("Warning: No base-word, assuming 0-th column as base")
		pos['base'] = 0

	if 'trans' not in pos and 'mono' not in pos:
		logging.error("Error: Neither monolingual nor translation defined, error!")
		return 2

	if 'tags' not in pos and 'tags' not in const:
		logging.error("Error: No tags provided!")
		return 3

	return 0


def human_check(force_yes):
	global printable, rows
	display_dict(printable, rows + ['tags'])  # display using new method form display_dict.py

	if force_yes is True:
		print("Automatic yes chosen...")
		return 0
	elif input("Are those OK?[y/n]") not in ['y', 'yes', 'Y', 'Yes']:

		print('Ups, what\'s wrong with it?')
		print('1 - I want to add static tag')
		print('2 - I want to remove a tag')
		print('3 - I want to change author')
		print('4 - I want to change level')
		print('5 - I want to add second direction in from-to')
		print('9 - I want to abort and try again')
		print('0 - Just ask me again')
		i = int(input("Choose number please: "))

		if i == 0:
			return 1
		elif i == 1:
			tag = input('Please type tag name: ')
			if tag != '':
				const['tags'].append(tag)
				for w in printable:
					w['tags'].append(tag)
			else:
				print('Error, empty string can\'t be a tag!')
				return 1
		elif i == 2:
			tag = input('Please type tag name: ')
			if tag in const['tags']:
				const['tags'].remove(tag)
				for w in printable:
					w['tags'].remove(tag)
			else:
				print('No such tag found!')
				return 1
		elif i == 3:
			author = input('Please type tag name: ')
			if author != '':
				const['author'] = author
				for w in printable:
					w['author'] = author
			else:
				print('Invalid author!')
				return 1
		elif i == 4:
			level = int(input('Please type new level: '))
			if level in range(10):
				const['level'] = level
				for w in printable:
					w['level'] = level
			else:
				print('Invalid level!')
				return 1
		elif i == 5:
			f, t = None, None
			for tag in const['tags']:
				if tag[:5] == 'from_':
					f = tag[5:]
				elif tag[:3] == 'to_':
					t = tag[3:]

			const['tags'] += ['from_' + t, 'to_' + f]
			for w in printable:
				w['tags'] += ['from_' + t, 'to_' + f]

			print('Added new tags:', ['from_' + t, 'to_' + f])
		elif i == 9:
			sys.exit("Aborting...")
		else:
			return 1
	else:
		return 0


def open_file(path_name):
	try:
		f = codecs.open(path_name, "r", 'utf-8')
		print("\nFile: " + path_name + "\n")
		return f
	except SystemError:
		print("Error while opening file!")
		return 1


def add_to_db():
	global printable, db, tags_info

	db.db.begin()
	# begin a transaction. No data will be written to db until commit()

	for tag in tags_info:
		if tag['tag_name'] == '':
			continue
		db.db.get_table(tag['tag_name'].strip())
		tag = tag_enhance(tag)
		if tag['description'] == '':
			tag['description'] = None
		db.tags.upsert(tag, ['tag_name'])
		# db.set_flag(tag['tag_name'], tag['flag'])
		# db.set_readable(tag['tag_name'], tag['readable'])
		# db.set_description(tag['tag_name'], tag.get('description'))

	records = []
	stats = [0, 0]
	for p in printable:
		r = dict(p)
		del r['tags']
		for key in ['base', 'trans']: # need to try if mono exists at all
			r[key] = r[key].replace('<br>', '\n').replace('\\n', '\n')

		records.append(r)
		res = db.add_words(r)
		stats[0] += res['added']
		stats[1] += res['updated']
		del r['time']
		p['id'] = db.find_id(r)[0]

	print("Added " + str(stats[0]) + ", updated " + str(stats[1]))

	for p in printable:
		db.join(p['id'], p['tags'])
		logging.info("Joined '" + str(p['base']) + "' with tags " + str(p['tags']))

	db.unify()

	db.db.commit()
	# write data to db. Additional checking might be done before

	print("Changes written to db. Now check if everything went properly...")
	if input("Do you want to make backup?[y/n]") in ['y', 'yes', 'Y', 'Yes']:
		db.backup()


def extract_metadata(filename, delimiters):
	global tags_info, const

	try:
		info = codecs.open(filename + '.inf', 'r', 'utf-8')
	except SystemError:
		print("Failed to open metadata file!")
		return 1

	d = dict()
	for x in ['rd', 'cd', 'author', 'from', 'to', 'level']:
		d[x] = info.readline().strip()

	delimiters['row_delim'] = d['rd'].replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
	delimiters['col_delim'] = d['cd'].replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
	#           process delimiters!!!! str.replace([\n, \t])...

	const['tags'] = ['from_' + d['from'], 'to_' + d['to']]
	const['level'] = int(d['level'])
	const['author'] = d['author']

	for line in info:       # const tags
		if len(line) < 5:
			break

		tag = line[:line.find('<r>')]
		read = line[line.find('<r>') + 3: line.find('</r>')]
		desc = line[line.find('<d>') + 3: line.find('</d>')]
		if tag != '':
			tags_info.append({'tag_name': tag.strip(), 'readable': read, 'description': desc,
				'flag': 'live'})
			const['tags'].append(tag)

	for line in info:       # live tag's descriptions
		if len(line) < 5:
			break

		tag = line[:line.find(',')]
		read = line[line.find('<r>') + 3: line.find('</r>')]
		desc = line[line.find('<d>') + 3: line.find('</d>')]
		if tag != '':
			tags_info.append({'tag_name': tag, 'readable': read, 'description': desc, 'flag': 'live'})

	info.close()
	return 0


# --------------------------------------------------------------------#
# ----------------------   Main methods      -------------------------#
# --------------------------------------------------------------------#


def insert_with_meta_delimiters(path_name, **kwargs):
	global db, printable, rows, pos, const

	f = open_file(path_name)
	if f == 1:
		return 4

	# --------------------       Set delimiters    -----------------------#

	delimiters = dict()
	if extract_metadata(path_name, delimiters) != 0:
		return 5
	col_delim = delimiters['col_delim']
	row_delim = delimiters['row_delim']

	# --------------------       Grab data     --------------------------#

	data = [s.split(col_delim) for s in f.read().split(row_delim)]
	if len(data[-1][0]) == 0:  # prevent last empty line in file...
		data = data[:-1]
	f.close()

	examine_sources(data[0], **kwargs)

	logging.info("pos: " + str(pos) + ", const: " + str(const))

	if check_sources() != 0:
		return 2

	# ----------------------    Build records    ------------------------#

	for line in data[1:]:
		d = dict()
		for key in const:
			d[key] = const[key]
		for key in pos:  # constant values CAN be overridden by those
			# taken directly from table (^-^)
			d[key] = line[pos[key]].strip()

		d['tags'] = d['tags'][:-1]  # override with table containing all live tags
		if line[pos['tags']] is not '':
			d['tags'] += line[pos['tags']:]

		if 'tags' in const:
			d['tags'] += const['tags']
		for t in d['tags']:
			if t.startswith('#'):
				d['tags'][d['tags'].index(t)] = t[1:]  # remove initial # in tags

		printable.append(d)  # now contains tags as a list also

	del data[:]

	# -----------------------    Human check    --------------------------#

	while human_check(kwargs.get('force_yes')) != 0:
		pass

	# ----------------------     Add to db       -------------------------#

	add_to_db()

	zero()


# not ready
def insert_custom_record_quotes(path_name, col_delim=',', row_begin='', row_end='\n', **kwargs):
	global db, printable, rows, pos, const

	f = open_file(path_name)
	if f == 1:
		return 4

	extract_metadata(path_name, kwargs)
	# --------------------       Grab data     --------------------------#

	data = [s.split(col_delim) for s in f.read().split(row_delim)]
	f.close()

	examine_sources(data[0], **kwargs)

	logging.info("pos: " + str(pos) + ", const: " + str(const))

	if check_sources() != 0:
		return 2

	# ----------------------    Build records    ------------------------#

	for line in data[1:]:
		d = dict()
		for key in const:
			d[key] = const[key]
		for key in pos:  # constant values CAN be overridden by those
			# taken directly from table (^-^)
			d[key] = line[pos[key]].strip()

		d['tags'] = []  # override with table containing all live tags
		if line[pos['tags']] is not '':
			d['tags'] += line[pos['tags']:]

		if 'tags' in const:
			d['tags'] += const['tags']
		for t in d['tags']:
			if t.startswith('#'):
				d['tags'][d['tags'].index(t)] = t[1:]  # remove initial # in tags

		printable.append(d)  # now contains tags as a list also

	del data[:]

	# -----------------------    Human check    --------------------------#

	while human_check(kwargs.get('force_yes')) != 0:
		pass

	# ----------------------     Add to db       -------------------------#

	add_to_db()

	zero()


def insert_line_per_record(path_name, delimiter=',', **kwargs):
	global db, printable, rows, pos, const

	f = open_file(path_name)
	if f == 1:
		return 4

	if extract_metadata(path_name, dict()) != 0:
	 	return 5

	# --------------------       Grab data     --------------------------#

	header = f.readline().strip().split(delimiter)
	header[0] = header[0].replace('\ufeff', '')
	examine_sources(header, **kwargs)
	logging.info("pos: " + str(pos) + ", const: " + str(const))

	if check_sources() != 0:
		return 2

	# ----------------------    Build records    ------------------------#

	for line in f:
		d = dict()
		line = line.strip().split(delimiter)
		for key in const:
			d[key] = const[key]
		for key in pos:  # constant values CAN be overridden by those
			# taken directly from table (^-^)
			d[key] = line[pos[key]]

		d['tags'] = []  # override with table containing all live tags
		if len(line) >= pos.get('tags', 100):
			d['tags'] += line[pos['tags']:]

		if 'tags' in const:
			d['tags'] += const['tags']
		for t in d['tags']:
			if t.startswith('#'):
				d['tags'][d['tags'].index(t)] = t[1:]  # remove initial # in tags

		printable.append(d)  # now contains tags as a list also

	f.close()

	# -----------------------    Human check    --------------------------#

	while human_check(kwargs.get('force_yes')) != 0:
		pass

	add_to_db()

	zero()


def import_from_csv(path_name, **kwargs):
	import csv
	global db, printable, pos, const, rows

	file = open_file(path_name)
	if file == 1:
		print("Can't open file", path_name)
		return 1

	f = csv.reader(file, **(kwargs.get('csv', dict())))       # dialect='excel'

	if extract_metadata(path_name, dict()) != 0:
		return 5

	# --------------------       Grab data     --------------------------#

	for row in f:
		header = row
		break

	examine_sources(header, **kwargs)
	logging.info("pos: " + str(pos) + ", const: " + str(const))

	if check_sources() != 0:
		return 2

	# ----------------------    Build records    ------------------------#

	for line in f:
		d = dict()
		for key in const:
			d[key] = const[key]
		for key in pos:  # constant values CAN be overridden by those
			# taken directly from table (^-^)
			d[key] = line[pos[key]]

		d['tags'] = []  # override with table containing all live tags
		if line[pos['tags']] is not '':
			d['tags'] += line[pos['tags']:] # adding tables here

		if 'tags' in const:
			d['tags'] += const['tags']
		for t in d['tags']:
			if t.startswith('#'):
				d['tags'][d['tags'].index(t)] = t[1:]  # remove initial # in tags

		printable.append(d)  # now contains tags as a list also

	file.close()

	# -----------------------    Human check    --------------------------#

	while human_check(kwargs.get('force_yes')) != 0:
		pass

	add_to_db()

	zero()




def test_tags_table():
	global db
	db.set_readable('const_tag_1', 'First Constant Tag')
	db.set_readable('rock4ever', 'Rock for Ever')
	db.set_flag('const_tag_1', 'hidden')
	db.set_flag('live_tag1', 'live')
	db.set_flag('live_tag_2', 'live')
	print(db.get_tag("heheszki"))

def custom():
	for r in db.words.find(author='Whitepeaony'):
		r['author'] = 'Whitepaeony'
		db.words.upsert(r, ['id'])
# --------------------------------------------------------------------#
# ----------------------    Call the functions   ---------------------#
# --------------------------------------------------------------------#


# insert_with_meta_delimiters("../data/test1.txt", force_yes=True)
#
# insert_line_per_record("../data/test2.txt", author="angielski", tags="#from_en,to_pl",
#                        level=4, force_yes=True)
#
# insert_line_per_record("../data/test3.txt", author="śmieszek", tags="from_pl-de,#to_pl",
#                        force_yes=True)

# import_from_csv("../data/test1.csv", author='Hubert', level=2, csv={})

# test_tags_table()

# print(extract_metadata('../data/info-test1.txt'))

# tags_info = [{'tag_name': 'scriptures', 'flag': 'live', 'readable': 'Księgi', 'description':
# 	'Księgi Pisma Świętego'}]

# insert_line_per_record('../data/edit/06-25-11-44-1cz 20-07.txt', delimiter='*', tags='verse')

# insert_line_per_record('../data/edit/06-25-11-44-1cz 20-07.txt', delimiter='*', tags='verse')

insert_line_per_record('../' + 'data/06-30-17-02-1czyt 24-07.txt'.replace('data',
                                                                               'data/edit'),
                       delimiter='*')
