#!/usr/bin/python

import sys, getopt
import requests
from MangaPandaHTMLParser import MangaPandaHTMLParser
import zipfile
from subprocess import call
from array import *

# ~~~~~ CONFIGURATION ~~~~~
site    = "http://www.mangapanda.com"
mangas  = 'tales-of-demons-and-gods'
chapNum = 3
# ~~~~~~~~~~~~~~~~~~~~~~~~~


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

print "Manga  : " + mangas
print "Chapter: " + str(chapNum)

url = site + "/" + mangas + "/" + str(chapNum)
index = 0
goNext = 1

images = []

parser = MangaPandaHTMLParser()
parser.setMangaName(mangas)

while goNext == 1:
	index += 1
	r = requests.get(url)
	if r.status_code != 200:
		print "Something went wrong:", r.status_code
		exit(1)

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

# call(["ebook-convert", n, m])

from ebooklib import epub

book = EpubBook()

# set metadata
book.set_identifier('id123456')
book.set_title('Sample Ebook')
book.set_language('en')

book.add_author('Author Tarrke')

# create chapter
c1 = epub.EpubHtml(title='Intro', file_name='chap_01.xhmtl', lang='en')
c1.content=u'<h1>Introduction</h1><p>Salut le monde.</p>'

book.add_item(c1)

book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'), epub.Section('Simple book'), (c1, ))

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

style= 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/cass", content=style)
book.add_item(nav_css)

book.spine = ['nav', c1]

epub.write_epub('est.epub', book, {})
