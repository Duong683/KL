from mitmproxy import ctx
import webServer

class Counter:
    def __init__(self):
        self.num = 0
        #ctx.log.info("abc")

    def request(self, flow):
        #self.num = self.num + 1
        #ctx.log.info("We've seen %d flows" % self.num)
        ctx.log.info(flow.request.url)

#main = webServer.WebServer()
#main.run()
addons = [Counter()]

