#!/usr/bin/python

import sys, getopt
import requests
from HTMLParser import HTMLParser
import zipfile
from subprocess import call

# ~~~~~ CONFIGURATION ~~~~~
site    = "http://www.mangapanda.com"
mangas  = 'tales-of-demons-and-gods'
chapNum = 3
# ~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~ Classe de parsing HTML ~~~~~
class MangaPandaHTMLParser(HTMLParser):
	def findNextChapterFromURL(self, url):
		ret = ""
		# on recupere la chaine "/manga/chap/image"
		s = url[url.rfind(mangas)-1:]
		print "DBG: url:", url
		print "DBG: s  :", s
		if s.count('/') > 2:
			idx = s.rfind('/')
			idz = s.rfind('/', 0, idx)
			ret = s[idz+1:idx]
		else:
			# de temps en temps on a la chaine "/manga/chap"
			ret = s[s.rfind('/')+1:]
		return int(ret)

	def handle_starttag(self, tag, attrs):
		if self.verbose == 1:
			print "Encountered a start tag:", tag
		if self.verbose == 1 and tag == "div":
			self.numDiv += 1
		if self.verbose == 1 and tag == "a":
			for attr in attrs:
				print (attr[0], attr[1])
				if attr[0] == "href":
					self.nextURL = site + attr[1]
		if self.verbose == 1 and tag == "img":
			for attr in attrs:
				if attr[0] == "src":
					self.imgURL = attr[1]
		if tag == "div":
			for attr in attrs:
				if attr[0] == 'id' and attr[1] == 'imgholder':
					print "I'am a start div for image holding"
					self.verbose = 1

	def handle_endtag(self, tag):
		if self.verbose == 1:
			print "Encountered an end tag:", tag
		if self.verbose == 1 and tag == "div":
			if self.numDiv == 0:
				self.verbose = 0
			else:
				self.numDiv -= 1

	def handle_data(self, data):
		i = 1
		#print "Encountered some data  :", data

	def __init__(self):
		HTMLParser.__init__(self)
		self.verbose = 0
		self.numDiv  = 0
		self.nextURL = ""
		self.imgURL  = ""


	def reset(self):
		HTMLParser.reset(self)
		self.verbose = 0
		self.numDiv  = 0
		self.nextURL = ""
		self.imgURL  = ""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

usageHelp = sys.argv[0] + """  ---  Help

usage: 
	""" + sys.argv[0] + """ [-h] -m mangaTitle -c chapterNumber

with
	mangaTitle:	le titre du manga
"""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~ Parsing agrs ~~~~~~~~~~
try:
	opts, args = getopt.getopt(sys.argv[1:],"hm:c:")
except getopt.GetoptError:
	print usageHelp
	sys.exit(2)

from array import *

mandatory = array('c') # ceci est un array de caracteres
mandatory.append('m')
mandatory.append('c')

for opt, arg in opts:
	if opt == "-h":
		print usageHelp
		sys.exit()
	elif opt in ("-m"):
		mangas = arg
		mandatory.remove('m')
	elif opt in ("-c") :
		chapNum = int(arg)
		mandatory.remove('c')

if len(mandatory) > 0:
	print usageHelp
	sys.exit(3)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


url = site + "/" + mangas + "/" + str(chapNum)
index = 0
goNext = 1

images = []

while goNext == 1:
	index += 1
	r = requests.get(url)
	if r.status_code != 200:
		print "Something went wrong:", r.status_code
		exit(1)

	parser = MangaPandaHTMLParser()
	parser.feed(r.content)

	print "PARSER: image url:", parser.imgURL
	print "PARSER: next url :", parser.nextURL
	print "PARSER: next chap:", parser.findNextChapterFromURL(parser.nextURL)
	print "PARSER: curr chap:", chapNum
 
	r = requests.get(parser.imgURL)
	if r.status_code != 200:
		print "Something went wrong:", r.status_code
		exit(1)


	imageName = mangas + "." + format(chapNum, '03') + "." + format(index, '02') + ".jpg"
	print "Got image:", imageName
	
	images.append(imageName)

	with open(imageName, 'w') as fichier:
		fichier.write(r.content)

	if parser.findNextChapterFromURL(parser.nextURL) != chapNum:
		goNext = 0
	else:
		url = parser.nextURL
		parser.reset()

n = mangas + "." + format(chapNum, '03') + ".cbz"
m = mangas + "." + format(chapNum, '03') + ".epub"
z = zipfile.ZipFile(n, 'w', zipfile.ZIP_DEFLATED)
for image in images:
	z.write(image)
	print image
z.close()

call(["ebook-convert", n, m])
