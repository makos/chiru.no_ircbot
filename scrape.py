# requires lxml and requests
# tested with python 3.4

from lxml import html
import requests

def now_playing():
	page = requests.get('http://chiru.no')
	tree = html.fromstring(page.text)

	nowplaying = tree.xpath('//div[@id="np"]/text()')
	return nowplaying[0]

def stats():
	page = requests.get('http://chiru.no')
	tree = html.fromstring(page.text)
	getstats = tree.xpath('//pre[@id="stats"]/text()')
	slist = getstats[0].split('\n')
	
	for x in range(slist.count('')):
		slist.remove('')
	
	statlist = []
	for string in slist:
		statlist.append(' '.join(string.split()))
	
	return statlist

def upcoming():
	page = requests.get('http://chiru.no')
	tree = html.fromstring(page.text)
	next = tree.xpath('//span[@id="upcoming"]/text()')

	if len(next) > 0:
		return next[0]
	else:
		return 'random'