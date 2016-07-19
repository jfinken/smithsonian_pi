import time
import atexit
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpserver

#from robot.robot import Robot

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, robot):
            self.robot = robot 

    def get(self):
        #self.write("Welcome PCCAPS Robotic Control. His name is: {}\n"
                #.format(self.robot.Name))
        self.render("html/index.html", title="PCCAPS Smithsonian Robotics")

class CameraPitchHandler(tornado.web.RequestHandler):
    def initialize(self, robot):
            self.robot = robot 

    @tornado.gen.coroutine
    def get(self):
        direction = self.get_argument('dir')
        amount = self.get_argument('amt')
        # TODO: parameter validation!
        # self.robot.CameraPitch(direction, amount)
        msg = "Camera: {}".format(direction)
        print(msg)
        self.write(msg)

class CameraYawHandler(tornado.web.RequestHandler):
    def initialize(self, robot):
            self.robot = robot 

    @tornado.gen.coroutine
    def get(self):
        direction = self.get_argument('dir')
        amount = self.get_argument('amt')
        # TODO: parameter validation!
        # self.robot.CameraYaw(direction, amount)
        msg = "Camera: {}".format(direction)
        print(msg)
        self.write(msg)

class BoomHandler(tornado.web.RequestHandler):
    def initialize(self, robot):
            self.robot = robot 

    @tornado.gen.coroutine
    def get(self):
        direction = self.get_argument('dir')
        amount = self.get_argument('amt')
        # TODO: parameter validation!
        #self.robot.Boom(direction, amount)
        msg = "Boom: {} for {} steps.".format(direction, amount)
        print(msg)
        self.write(msg)

class TreadHandler(tornado.web.RequestHandler):
    def initialize(self, robot):
            self.robot = robot 

    @tornado.gen.coroutine
    def get(self):
        direction = self.get_argument('dir')
        amount = self.get_argument('amt')
        # TODO: parameter validation!
        #self.robot.Tread(direction, float(amount))
        msg = "Tread control: {} for {} sec.".format(direction, amount)
        print(msg)
        self.write(msg)


# global state
# theRobot = Robot()
theRobot = None

"""
Main Tornado web application definition
"""
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler,                     {'robot':theRobot}),
                    (r"/cameraPitch$", CameraPitchHandler,  {'robot':theRobot}),
                    (r"/cameraYaw$", CameraYawHandler,      {'robot':theRobot}),
                    (r"/boom$", BoomHandler,                {'robot':theRobot}),
                    (r"/tread$", TreadHandler,              {'robot':theRobot}),
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
