import tornado.ioloop
import tornado.web
import webbrowser

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("serverTest")

#khoi tao server cho web hien thi log
class WebServer():

	#cau hinh Handle = MainHandle
	#cau hinh Port = 8888
	def __init__(self):
		ws  = tornado.web.Application([
			(r"/", MainHandler),
		])
		self.http_server = tornado.httpserver.HTTPServer(ws)
		self.port = 8888
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



if __name__ == "__main__":
	main = WebServer()
	main.run()