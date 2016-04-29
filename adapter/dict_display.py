# -*- coding: utf-8 -*-


def display_dict(dicts, columns = ('id', 'base')):

	if isinstance(dicts, list):
		print 'ok'
	elif isinstance(dicts, dict):
		dicts = [dicts]
	else:
		print "Unrecognised type of dic! " + str(type(dicts))
		return 1

	header = ''
	for col in columns:
		header += str(col) + '\t'
		if col is 'mono':
			header += '\t\t\t'
		elif col is 'author':
			header += '\t'
	print header[:-1] + '\n'

	for word in dicts:
		s = u''
		for col in columns:
			try:
				s += word[col][:16] +'\t'
			except KeyError:
				s += "null\t"
			except TypeError:
				s += str(word[col]) + '\t'

		print s[:-1]
	print ''	#empty line

	return 0