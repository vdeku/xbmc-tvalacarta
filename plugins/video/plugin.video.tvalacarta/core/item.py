class Item(object):
	channel = ""
	title = ""
	url = ""
	page = ""
	thumbnail = ""
	plot = ""
	duration = ""
	fanart = ""
	folder = ""
	action = ""
	server = ""
	extra = ""
	show = ""

	def __init__(self, channel="", title="", url="", page="", thumbnail="", plot="", duration="", fanart="", action="", server="", extra="", show="", folder=True):
		self.channel = channel
		self.title = title
		self.url = url
		if page=="":
			self.page = url
		else:
			self.page = page
		self.thumbnail = thumbnail
		self.plot = plot
		self.duration = duration
		self.fanart = fanart
		self.folder = folder
		self.server = server
		self.action = action
		self.extra = extra
		self.show = show

	def tostring(self):
		return "title=["+self.title+"], url=["+self.url+"], thumbnail=["+self.thumbnail+"], action=["+self.action+"], show=["+self.show+"]"