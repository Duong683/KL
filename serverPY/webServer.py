import os.path
import tornado.ioloop
import tornado.web
import webbrowser
<<<<<<< HEAD
import time
import json
from threading import Thread

data = {
   'url' : 'www.temp123.com',
   'method' : 'GET',
   'number' : 0
}

count = 0
#send log to web UI
class ShowLog(tornado.web.RequestHandler):

	def get(self):
		global count
		global data
		#print (count)
		data['number'] = count
		self.write(json.dumps(data))
		count = count + 1
		
		
#render web UI
class MainHandler(tornado.web.RequestHandler):

	def get(self):
		
		self.render('index.html')

#khoi tao server cho web hien thi log
class WebServer():
=======

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		print ("trigge")
		self.render('index.html', test="Hello, world!")

#khoi tao server cho web hien thi log
class WebServer():

>>>>>>> f857e120d9b298dc9f238dca5d90785c8ad1643f
	#cau hinh Handle = MainHandle
	#cau hinh Port = 8888
	def __init__(self):
		ws  = tornado.web.Application([
<<<<<<< HEAD
			(r"/", MainHandler),
			(r"/ShowLog", ShowLog)],
=======
			(r"/", MainHandler)],
>>>>>>> f857e120d9b298dc9f238dca5d90785c8ad1643f
			static_path = os.path.join(os.path.dirname(__file__), "static"),
			template_path = os.path.join(os.path.dirname(__file__), "templates"))

		self.http_server = tornado.httpserver.HTTPServer(ws)
<<<<<<< HEAD
		self.port = 6685
=======
		self.port = 6683
>>>>>>> f857e120d9b298dc9f238dca5d90785c8ad1643f
		self.web_url = "http://localhost:{}/".format(self.port)

	#tao loop - start server
	def run(self):
		self.http_server.listen(self.port)

		#print URL cua web 
		print ("Web server on: ")
		print (self.web_url)

		#auto open web UI
		success = self.open_browser(self.web_url)
		if not success:
			print ("Erro: cant open {} on your browser".format(self.web_url))
				
		try:
			tornado.ioloop.IOLoop.instance().start()
		except KeyboardInterrupt:
			self.shutdown()

	#shutdown Server
	def shutdown(self):
		tornado.ioloop.IOLoop.instance().stop()

	#Open a URL in a browser window.
	def open_browser(self, url: str) -> bool:
	
		browsers = (
			"windows-default", "macosx",
		 "google-chrome", "chrome", "chromium", "chromium-browser",
		 "firefox", "opera", "safari",
		)
		for browser in browsers:
			try:
				b = webbrowser.get(browser)
			except webbrowser.Error:
				pass
			else:
				b.open(url)
				return True
		return False

<<<<<<< HEAD
	def setQueue(self, n: str):
		global data
		data['url'] = n




#if __name__ == "__main__":
#	main = WebServer()
#	main.run()
=======


if __name__ == "__main__":
	main = WebServer()
	main.run()
>>>>>>> f857e120d9b298dc9f238dca5d90785c8ad1643f
