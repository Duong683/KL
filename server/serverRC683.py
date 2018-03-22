import socketserver, subprocess, sys
from threading import Thread
from pprint import pprint
import json

my_unix_command = ['bc']
HOST = 'localhost'
PORT = 2001

class SingleTCPHandler(socketserver.BaseRequestHandler):
	"One instance per connection.  Override handle(self) to customize action."
	def handle(self):
		# self.request is the client connection
		data = self.request.recv(1024)  # clip input at 1Kb
		text = data.decode('utf-8')
		pprint(json.loads(text))
		self.request.send('OK'.encode('utf-8'))
		self.request.close()

class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	# Ctrl-C will cleanly kill all spawned threads
	daemon_threads = True
	# much faster rebinding
	allow_reuse_address = True

	def __init__(self, server_address, RequestHandlerClass):
		socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
	server = SimpleServer((HOST, PORT), SingleTCPHandler)
	# terminate with Ctrl-C
	try:
		print ('---------------------------------------------')
		print ('Server On')
		print ('---------------------------------------------')
		server.serve_forever()
	except KeyboardInterrupt:
		print ('---------------------------------------------')
		print ('Bye!')
		sys.exit(0)