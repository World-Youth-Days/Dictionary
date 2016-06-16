import codecs
import os


def add_tag(path, filename, start, row_delim, col_delim):
	f = codecs.open(path + '/' + filename, "r", 'utf-8')

	# os.system('mkdir ' + path + '/edit')
	n = codecs.open(path + '/edit/' + filename, 'w', 'utf-8')
	data = [r.strip().split(col_delim) for r in f.read().split(row_delim)]
	h = ''
	for c in data[0]:
		h += c + str(col_delim)
	n.write(h + str(row_delim))

	for line in data[1:]:
		s = str(start) + ' ' + line[0] + str(col_delim) + str(start) + ' ' + line[1]
		for col in line[2:]:
			s += str(col_delim) + col
		n.write(s + str(row_delim))
		start += 1

	f.close()
	n.close()

add_tag('../data', '06-14-Whitepaeony.txt', 10, '\n', ',')
