# -*- coding: utf-8 -*-


def display_dict(dicts, columns = ('id', 'base'), header=True):

	if isinstance(dicts, list):
		print 'ok'
	elif isinstance(dicts, dict):
		dicts = [dicts]
	else:
		print "Unrecognised type of dic! " + str(type(dicts))
		return 1

	def create_header():
		h = ''
		for col in columns:
			h += str(col) + '\t'
			if col == 'mono':
				h += '\t\t\t'
			elif col == 'author':
				h += '\t'
		return h[:-1] + '\n'


	if header  == False:
		pass
	elif header == "Only":
		print create_header()
		return 0
	elif header == True:
		print create_header()
	else:
		print "Unknown header value: " + str(header)
		return 2


	for word in dicts:
		s = u''
		for col in columns:
			add = u''

			try:
				add += word[col][:20] +'\t'

			except KeyError:
				add += "null\t"

			except TypeError:
				add += unicode(word[col]) + '\t'

			if col == u'mono':
				if len(add) < 6:
					add += "\t\t\t"
					#print "Prelonging"
				elif len(add) < 10:
					add += "\t\t"
				elif len(add) < 14:
					add += "\t"
					#print "Prelonging"
			elif col == u'author' and len(add) < 6:
				add += "\t"

			s += add

		print s[:-1]
	print ''	#empty line

	return 0