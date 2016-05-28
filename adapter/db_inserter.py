# -*- coding: utf-8 -*-
import codecs
import logging

from DbAdapter import DbAdapter
from display_dict import display_dict

db = DbAdapter(None)  # define db connection
printable = []    # here place all processed records
rows = ['base', 'mono', 'trans', 'author', 'level']
pos = dict()  # dict with positions in file
const = dict()      # dict with const values


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
			const['tags'] = kwargs['tags'].split(',')
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

	display_dict(printable, rows + ['tags'])  # display using new method form display_dict.py

	if force_yes is True:
		print("Automatic yes chosen...")
	elif input("Are those OK?[y/n]") not in ['y', 'yes', 'Y', 'Yes']:
		print("Aborting...")
		return 1

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
	global printable, db
	db.db.begin()
	# begin a transaction. No data will be written to db until commit()
	records = []
	stats = [0, 0]
	for p in printable:
		r = dict(p)
		del r['tags']
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

	print("Changes written to db.")


# --------------------------------------------------------------------#
# ----------------------   Main methods      -------------------------#
# --------------------------------------------------------------------#


def insert_custom_record(path_name, col_delim=',', row_delim='\n', **kwargs):
	global db, printable, rows, pos, const

	zero()
	f = open_file(path_name)
	if f == 1:
		return 4

	# --------------------       Grab data     --------------------------#

	data = [s.split(col_delim) for s in f.read().split(row_delim)]
	if len(data[-1][0]) == 0:    # prevent last empty line in file...
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

	if human_check(kwargs.get('force_yes')) != 0:
		return 3

	# ----------------------     Add to db       -------------------------#

	add_to_db()

	print("Changes written to db.")


def insert_custom_record_quotes(path_name, col_delim=',', row_begin='', row_end='\n', **kwargs):
	global db, printable, rows, pos, const

	zero()
	f = open_file(path_name)
	if f == 1:
		return 4

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

	if human_check(kwargs.get('force_yes')) != 0:
		return 3

	# ----------------------     Add to db       -------------------------#

	add_to_db()

	print("Changes written to db.")


def insert_line_per_record(path_name, delimiter=',', **kwargs):
	global db, printable, rows, pos, const
	zero()

	f = open_file(path_name)
	if f == 1:
		return 4

	# --------------------       Grab data     --------------------------#

	header = f.readline().strip().split(delimiter)
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
		if line[pos['tags']] is not '':
			d['tags'] += line[pos['tags']:]

		if 'tags' in const:
			d['tags'] += const['tags']
		for t in d['tags']:
			if t.startswith('#'):
				d['tags'][d['tags'].index(t)] = t[1:]       # remove initial # in tags

		printable.append(d)   # now contains tags as a list also

	f.close()

	# -----------------------    Human check    --------------------------#

	if human_check(kwargs.get('force_yes')) != 0:
		return 3

	add_to_db()


def import_from_csv(path_name, **kwargs):
	import csv
	global db, printable, pos, const, rows
	pos['tags'] = None,

	try:
		f = csv.reader(codecs.open("foo.csv", encoding="utf-8"), dialect='excel')
	except SystemError:
		print("Error while opening file!")
		return 4
	print("\nFile: " + path_name + "\n")

	rows = ['base', 'mono', 'trans', 'author', 'level']
	pos = dict(base=None, mono=None, trans=None, author=None,
	           level=None)  # sorry, I avoid understanding deep/shallow copy specs ;)
	const = dict()

def test_tags_table():
	global db
	db.set_readable('const_tag_1', 'First Constant Tag')
	db.set_readable('rock4ever', 'Rock for Ever')
	db.set_flag('const_tag_1', 'hidden')
	db.set_flag('live_tag1', 'live')
	db.set_flag('live_tag_2', 'live')
	print(db.get_tag("heheszki"))

# --------------------------------------------------------------------#
# ----------------------    Call the functions   ---------------------#
# --------------------------------------------------------------------#


insert_custom_record("../data/test1.txt", author="francuski", tags="from_fr,to_pl",
                       level=8, force_yes=True)

insert_line_per_record("../data/test2.txt", author="angielski", tags="#from_en,to_pl",
                       level=4, force_yes=True)

insert_line_per_record("../data/test3.txt", author="śmieszek", tags="from_pl-de,#to_pl",
                       force_yes=True)

#test_tags_table()
