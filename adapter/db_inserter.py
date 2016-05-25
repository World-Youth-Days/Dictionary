# -*- coding: utf-8 -*-
import codecs
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


# --------------------------------------------------------------------#
# ----------------------    Examine header   -------------------------#
# --------------------------------------------------------------------#


def examine_sources(header, **kwargs):

	# --------need to add remove-# feature

	"""find pos and const in file and kwargs"""
	""":arg : header : list(str)"""
	print("Header: " + str(header))
	print("Kwargs: " + str(kwargs))

	global rows, pos, const

	for col in rows:
		if col in kwargs:
			const[col] = kwargs[col]
			print("OK: Const " + col + " found")

		try:
			pos[col] = header.index(col)
			print("OK: " + col + " at column " + str(pos[col]))
		except ValueError:
			print("Info: No " + col + " header found")

		if 'tags' in header:
			pos['tags'] = header.index('tags')
		if 'tags' in kwargs:
			const['tags'] = kwargs['tags'].split(',')
		# override plain string with table

	return 0


# --------------------------------------------------------------------#
# ------------------   Check for integrity      ----------------------#
# --------------------------------------------------------------------#


def check_sources():
	if len(pos) + len(const) < 4:
		return "Error: Insufficient information provided to fill all columns."

	if 'base' not in pos:
		print("Warning: No base-word, assuming 0-th column as base")
		pos['base'] = 0

	if 'trans' not in pos and 'mono' not in pos:
		return "Error: Neither monolingual nor translation defined, error!"

	if 'tags' not in pos and 'tags' not in const:
		return "Error: No tags provided!"

	return 0


# --------------------------------------------------------------------#
# ----------------------    Human check      -------------------------#
# --------------------------------------------------------------------#


def human_check(force_yes):

	display_dict(printable, rows + ['tags'])  # display using new method form display_dict.py

	if force_yes is True:
		print("Automatic yes chosen...")
	elif input("Are those OK?[y/n]") not in ['y', 'yes', 'Y', 'Yes']:
		return "Aborting..."

	return 0


# --------------------------------------------------------------------#
# ----------------------   Line is record    -------------------------#
# --------------------------------------------------------------------#


def insert_from_file_line_is_record(path_name, delimiter=',', **kwargs):
	global db, printable, rows, pos, const
	zero()

	# ----------------------      Open file      -------------------------#

	try:
		f = codecs.open(path_name, "r", 'utf-8')
	except SystemError:
		print("Error while opening file!")
		return 4
	print("\nFile: " + path_name + "\n")

	# -------------- examine header --------------------------------------#
	header = f.readline().strip().split(delimiter)
	examine_sources(header, **kwargs)
	
	print("pos: " + str(pos))
	print("const: " + str(const))

	# ----------------------- check sources -----------------------------#
	check = check_sources()
	if check != 0:
		print(check)
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
		printable.append(d)   # now contains tags as a list also

	# May be further developped to allow issue solving

	if 'force_yes' in kwargs:
		human = human_check(kwargs['force_yes'])
	else:
		human = human_check(False)

	if human != 0:
		print(human)
		return 3

	# --------------------------------------------------------------------#
	# ----------------------     Add to db       -------------------------#
	# --------------------------------------------------------------------#
	records = []
	stats = [0,0]
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
		print("Joined " + str(p['id']) + " with tags " + str(p['tags']))
	
	print("Closing source file...")
	f.close()


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


insert_from_file_line_is_record("../data/test1.txt", author="francuski", tags="from_fr,to_pl",
                                level=10, force_yes=True)

insert_from_file_line_is_record("../data/test2.txt", author="angielski", tags="from_en,to_pl",
 level=4, force_yes=True)

insert_from_file_line_is_record("../data/test3.txt", author="śmieszek", tags="from_pl,to_pl",
 force_yes=True)

#test_tags_table()

#

# --------------------------------------------------------------------#
# ----------------------     CSV import      -------------------------#
# --------------------------------------------------------------------#


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
