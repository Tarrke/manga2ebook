from HTMLParser import HTMLParser

# ~~~~~ Classe de parsing HTML ~~~~~
class MangaPandaHTMLParser(HTMLParser):
	def findNextChapterFromURL(self, url):
		ret = ""
		# on recupere la chaine "/manga/chap/image"
		s = url[url.rfind(self.mangas)-1:]
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
					self.nextURL = self.site + attr[1]
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
	
	def setMangaName(self, name):
		self.mangas = name

	def __init__(self):
		HTMLParser.__init__(self)
		self.verbose = 0
		self.numDiv  = 0
		self.nextURL = ""
		self.imgURL  = ""
		self.site    = "http://www.mangapanda.com"


	def reset(self):
		HTMLParser.reset(self)
		self.verbose = 0
		self.numDiv  = 0
		self.nextURL = ""
		self.imgURL  = ""
		self.site    = "http://www.mangapanda.com"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
