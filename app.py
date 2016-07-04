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

    def get(self):
        #self.write("Welcome PCCAPS Robotic Control. His name is: {}\n"
                #.format(self.robot.Name))
        self.render("html/index.html", title="PCCAPS Smithsonian Robotics")

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
        msg = "Camera: {}".format(direction)
        print(msg)
        self.write(msg)

class BoomHandler(tornado.web.RequestHandler):
    def initialize(self, robot):
            self.robot = robot 

    @tornado.gen.coroutine
    def get(self, up=None, down=None):
        direction=None
        if up:
            self.robot.BoomUp()
            direction=up
        elif down:
            self.robot.BoomDown()
            direction=down
        msg = "Boom: {}".format(direction)
        print(msg)
        self.write(msg)

class TreadHandler(tornado.web.RequestHandler):
    def initialize(self, robot):
            self.robot = robot 

    @tornado.gen.coroutine
    #def get(self, forward=None, backward=None, left=None, right=None):
    def get(self):
        direction = self.get_argument('dir')
        amount = self.get_argument('amt')
        """
        if forward:
            #self.robot.TreadForward()
            direction=forward
        elif backward:
            #self.robot.TreadBackward()
            direction=backward
        elif left:
            #self.robot.TreadLeft(float(amount))
            direction=left
        elif right:
            #self.robot.TreadRight(float(amount))
            direction="foo"
        """
        msg = "Tread control: {} for {} sec.".format(direction, amount)
        print(msg)
        self.write(msg)


# global state
theRobot = Robot()

"""
Main Tornado web application definition
"""
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler,                 {'robot':theRobot}),
                    (r"/camera/(up)$", CameraHandler,   {'robot':theRobot}),
                    (r"/camera/(down)$", CameraHandler, {'robot':theRobot}),
                    (r"/camera/(left)$", CameraHandler, {'robot':theRobot}),
                    (r"/camera/(right)$", CameraHandler,{'robot':theRobot}),
                    (r"/boom/(up)$", BoomHandler,       {'robot':theRobot}),
                    (r"/boom/(down)$", BoomHandler,     {'robot':theRobot}),
                    (r"/tread$", TreadHandler,{'robot':theRobot}),
                    #(r"/tread/(backward)$",TreadHandler,{'robot':theRobot}),
                    #(r"/tread/(left)$", TreadHandler,   {'robot':theRobot}),
                    #(r"/tread/(right)$", TreadHandler,  {'robot':theRobot}),
                    #(r"/tread/(right)$", TreadHandlerDirection,  {'robot':theRobot}),
                    #(r"/tread/(left)$", TreadHandlerDirection,  {'robot':theRobot}),
                ]
        settings = dict(template_path='template/',
                        static_path='static/', debug=False)
        tornado.web.Application.__init__(self, handlers, **settings)

# Run the instance
if __name__ == "__main__":
    port = 8080
    print "App server listening on {}\nQuit with Ctrl-C".format(port)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
