# -*- coding: utf-8 -*-
import copy

def display_dict(dicts, columns = ('id', 'base'), header=True):
	"""

	:param dicts: data in dicts to be printed
	:param columns: column names to be printed
	:param header: if True - print header, if "Only" - print only header
	:return: string to be displayed or error number
	"""

	if isinstance(dicts, list):
		pass
	elif isinstance(dicts, dict):
		dicts = [dicts]
	else:
		pass
		#return "1: Unrecognised type of dict! " + str(type(dicts))

	for row in columns:
		#make sure columns contain no surprises ;)
		try:
			dicts[0][row]
		except KeyError:
			columns.remove(row)
			print( "No " + row + " found in given dict!")

	h = []
	if header == True:
		for col in columns:
			h.append(str(col))
	else:
		print("Unknown header value: " + str(header))
		pass

	# make 2D table from dicts
	#tab = [[ word[val] for val in columns] for word in dicts]
	tab = [h.copy()]
	for word in dicts:
		tab.append([str(word[val]) for val in columns])

	widths = [max(map(len, col)) for col in zip(*tab)]

	if header is True:
		print(" ".join((val.ljust(width) for val, width in zip(h, widths))))
		print('')
	tab.remove(h)

	for row in tab:
		print( " ".join((val.ljust(width) for val, width in zip(row, widths))))

	print ('')
	return 0