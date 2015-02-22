# requires lxml and requests
# tested with python 3.4

from lxml import html
import requests

def get_current_data():
	page = requests.get('http://chiru.no/api.txt')
	page.encoding='utf-8'
	page = page.text.split('{}')
	data = page[:-1]
	# print(data[0])
	return data

def now_playing():
	np = get_current_data()
	return np[0]

def upcoming():
	next = get_current_data()
	if next[1] == '':
		return 'random'
	else:
		return next[1]

def stats():
	page = requests.get('http://chiru.no')
	tree = html.fromstring(page.text)
	getstats = tree.xpath('//pre[@id="stats"]/text()')
	slist = getstats[0].split('\n')
	
	for x in range(slist.count('')):
		slist.remove('')

	statlist = [' '.join(string.split()) for string in slist]
	
	return statlist

if __name__ == '__main__':
	print(get_current_data())
	print(stats())