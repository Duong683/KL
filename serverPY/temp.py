#! /usr/bin/python2.7
import os
import json
import tornado.ioloop
import tornado.web
from serial import *


tornadoPort = 8888
cwd = os.getcwd() # used by static file server


# Make a Serial object
serialPort = '/dev/ttyACM0'
serialBaud = 9600
ser = Serial( serialPort, serialBaud, timeout=0, writeTimeout=0 )



# gets serial input in a non-blocking way
serialPending = ''
def checkSerial():
    try:
        s = ser.read( ser.inWaiting() )
    except:
        print("Error reading from %s " % serialPort )
        return
    
    if len(s):
        serialPending += s
        paseSerial()
    

#called whenever there is new input to check
serialHistory = ''
mostRecentLine = ''
def parseSerial():
    split = serialPending.split("\r\n")
    if len( split ) > 1:
        for line in split[0:-1]:
            print( line )
            
            #do some stuff with the line, if necessary
            #example:
            mostRecentLine = line
            # in this example, status will show the most recent line

            serialHistory += line

        pending = split[-1]


# send the index file
class IndexHandler(tornado.web.RequestHandler):
    def get(self, url = '/'):
        self.render('index.html')
    def post(self, url ='/'):
        self.render('index.html')


# handle commands sent from the web browser
class CommandHandler(tornado.web.RequestHandler):
    #both GET and POST requests have the same responses
    def get(self, url = '/'):
        print "get"
        self.handleRequest()
        
    def post(self, url = '/'):
        print 'post'
        self.handleRequest()
    
    # handle both GET and POST requests with the same function
    def handleRequest( self ):
        # is op to decide what kind of command is being sent
        op = self.get_argument('op',None)
        
        #received a "checkup" operation command from the browser:
        if op == "checkup":
            #make a dictionary
            status = {"server": True, "mostRecentSerial": mostRecentLine }
            #turn it to JSON and send it to the browser
            self.write( json.dumps(status) )
        
        #operation was not one of the ones that we know how to handle
        else:
            print op
            print self.request
            raise tornado.web.HTTPError(404, "Missing argument 'op' or not recognized")


# adds event handlers for commands and file requests
application = tornado.web.Application([
    #all commands are sent to http://*:port/com
    #each command is differentiated by the "op" (operation) JSON parameter
    (r"/(com.*)", CommandHandler ),
    (r"/", IndexHandler),
    (r"/(index\.html)", tornado.web.StaticFileHandler,{"path": cwd}),
    (r"/(.*\.png)", tornado.web.StaticFileHandler,{"path": cwd }),
    (r"/(.*\.jpg)", tornado.web.StaticFileHandler,{"path": cwd }),
    (r"/(.*\.js)", tornado.web.StaticFileHandler,{"path": cwd }),
    (r"/(.*\.css)", tornado.web.StaticFileHandler,{"path": cwd }),
])


if __name__ == "__main__":
    
    #tell tornado to run checkSerial every 10ms
    serial_loop = tornado.ioloop.PeriodicCallback(checkSerial, 10)
    serial_loop.start()
    
    #start tornado
    application.listen(tornadoPort)
    print("Starting server on port number %i..." % tornadoPort )
    print("Open at http://127.0.0.1:%i/index.html" % tornadoPort )
    tornado.ioloop.IOLoop.instance().start()