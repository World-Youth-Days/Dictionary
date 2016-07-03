import codecs
import os


def numeration(filename, start, row_delim, col_delim):
	f = codecs.open('../' + filename, "r", 'utf-8')

	os.system('mkdir ../data/edit')
	n = codecs.open('../data/edit/' + filename.replace('data/', ''), 'w', 'utf-8')
	data = [r.strip().split(col_delim) for r in f.read().split(row_delim)]
	h = ''
	for c in data[0]:
		h += c + str(col_delim)
	n.write(h + str(row_delim))

	# header of the reading
	s = '00 ' + data[1][0] + str(col_delim) + '00 ' + data[1][1]
	for col in data[1][2:]:
		s += str(col_delim) + col
	n.write(s + str(row_delim))

	for line in data[2:]:
		s = str(start).zfill(2) + ' ' + line[0] + str(col_delim) + str(start).zfill(2) + ' ' + \
		    line[1]
		for col in line[2:]:
			s += str(col_delim) + col
		n.write(s + str(row_delim))
		start += 1

	f.close()
	n.close()

numeration('data/06-30-17-02-1czyt 24-07.txt', 20, '\n', '*')
