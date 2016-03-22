import time
import atexit
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpserver

from robot.robot import Robot

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, robot):
            self.robot = robot 

    # TODO: serve up Antonio's main index and assets
    def get(self):
        self.write("Welcome PCCAPS Robotic Control. His name is: {}\n"
                .format(self.robot.Name))

class CameraHandler(tornado.web.RequestHandler):
    def initialize(self, robot):
            self.robot = robot 

    @tornado.gen.coroutine
    def get(self, up=None, down=None, left=None, right=None):
        direction=None
        if up:
            self.robot.CameraPitchUp()
            direction=up
        elif down:
            self.robot.CameraPitchDown()
            direction=down
        elif left:
            self.robot.CameraYawLeft()
            direction=left
        elif right:
            self.robot.CameraYawRight()
            direction=right
        self.write("Camera: {}".format(direction))

class BoomHandler(tornado.web.RequestHandler):
    def initialize(self, robot):
            self.robot = robot 

    @tornado.gen.coroutine
    def get(self):
        self.write("Boom control...")

class TreadHandler(tornado.web.RequestHandler):
    def initialize(self, robot):
            self.robot = robot 

    @tornado.gen.coroutine
    def get(self):
        self.write("Tread control...")

# global state
theRobot = Robot()

"""
Main Tornado web application definition
"""
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler,         {'robot':theRobot}),
                    (r"/camera/(up)$", CameraHandler, {'robot':theRobot}),
                    (r"/camera/(down)$", CameraHandler, {'robot':theRobot}),
                    (r"/camera/(left)$", CameraHandler, {'robot':theRobot}),
                    (r"/camera/(right)$", CameraHandler, {'robot':theRobot}),
                    (r"/boom", BoomHandler,     {'robot':theRobot}),
                    (r"/tread", TreadHandler,   {'robot':theRobot}),
                ]
        settings = dict(template_path='/templates',
                        static_path='/static', debug=False)
        tornado.web.Application.__init__(self, handlers, **settings)

# Run the instance
if __name__ == "__main__":
    port = 8080
    print "App server listening on {}\nQuit with Ctrl-C".format(port)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
