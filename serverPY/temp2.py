import webServer
import time
from threading import Thread

def deftemp(webServer):
	webServer.run()

main = webServer.WebServer()

worker = Thread(target=deftemp, args=(main,))
worker.setDaemon(False)
worker.start()
time.sleep(5)
main.setQueue("test set")

