# import Tkinter
import mtTkinter as Tkinter
import Image
import ImageTk
from robot import Robot
from robot import RobotDrawing
from network import Network
import time
import numpy
import copy
import socket
# from network import Network


class Game(object):
    """Create a game.

    :param sensor: Sensor object that detect the infrared.
    :param network: Network object that communicate with the other table
    :param name: Name of the game.
    :param test: Only use for test-driven.
    :param servers: List containing the address of the other Robot Table.

    """
    def __init__(self, robot, remote_server_object=None, addr_main_server=None, addr_remote_servers=None, remote=False, name=None):
        self.name = name
        self.robot = robot
        self.sensor = robot.sensor
        self.remote_server_object = remote_server_object

        self.x_factors = None
        self.y_factors = None

        self.addr = self.get_addr()
        self.addr_main_server = addr_main_server
        self.addr_remote_servers = addr_remote_servers
        self.servers = [self]

        # if servers is None:
        #     self.servers = []
        # else:
        #     self.servers = servers
        self.remote = remote
        if self.remote is False:
            self._init_graphic()
            self.robot.robot_drawing.canvas = self.canvas

        # if test is False:
            # self.robot = Robot(self.sensor, new_robot_drawing)
            # self.robots = []
            # self.robots.append(self.robot)
            # self.robot_drawing = RobotDrawing(self.canvas)

    def is_main_server(self):
        return addr_main_server == addr

    def get_addr(self):
        """Return the ip address of the server.

        Note: the solution was find here :
        http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib

        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com", 80))
        addr = s.getsockname()[0]
        s.close()
        return addr

    def _init_graphic(self):
        self.root = Tkinter.Tk()
        self.screen_width, self.screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self._set_full_screen()
        self.canvas = Tkinter.Canvas(self.root)

    @property
    def robot_leds(self):
        """Return the robot's leds location calibrated.

        Note: You need to do the calibration first (once).

        """
        if self.x_factors is None:
            print "The calibration was not done"
            #TODO : add throw exception
            return False
        else:
            leds = self.robot.leds
            leds['front'] = self._apply_calibration_factors(leds['front'],
                                                            self.x_factors,
                                                            self.y_factors)
            leds['left'] = self._apply_calibration_factors(leds['left'],
                                                           self.x_factors,
                                                           self.y_factors)
            leds['right'] = self._apply_calibration_factors(leds['right'],
                                                            self.x_factors,
                                                            self.y_factors)
            return leds

    def _init_servers(self):
        for addr_remote_server in self.addr_remote_servers:
            remote_server = copy.deepcopy(self.remote_server_object)
            remote_server.robot.sensor.addr = addr_remote_server
            remote_server.robot.robot_drawing.canvas = self.canvas

            # network = copy.deepcopy(self.network)
            # network.addr = addr_remote_server
            # robot = self._create_robot()
            # remote_server = Game(network, robot, addr_main_server=None, sensor=None, remote=False, name=None):
            self.servers.append(remote_server)

    # def add_robots(self):
    #     for server in self.servers:
    #         new_robot_drawing = RobotDrawing(self.canvas)
    #         network = Network(server)
    #         new_robot = Robot(network, robot_drawing=new_robot_drawing)
    #         self.robots.append(new_robot)

    def draw_robots(self):
        for server in self.servers:
            robot = server.robot
            leds = robot.leds
            leds['front'] = self._apply_calibration_factors(leds['front'],
                                                            self.x_factors,
                                                            self.y_factors)
            leds['left'] = self._apply_calibration_factors(leds['left'],
                                                           self.x_factors,
                                                           self.y_factors)
            leds['right'] = self._apply_calibration_factors(leds['right'],
                                                            self.x_factors,
                                                            self.y_factors)
            robot.draw(leds)

    def _apply_calibration_factors(self, led, x_factors, y_factors):
        """Return the led's location calibrated."""
        led['X'] = (led['X'] * x_factors[0]
                    + led['Y'] * x_factors[1]
                    + x_factors[2])
        led['Y'] = (led['X'] * y_factors[0]
                    + (self.sensor.height_resolution - led['Y']) * y_factors[1]
                    + y_factors[2])
        return led

    def _create_board(self, rows, columns):
        """Return a list that simulate a map"""
        board = []
        for i in range(rows):
            board.append([0] * columns)
        return board

    def _set_full_screen(self):
        """Set the window in full screen"""
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (self.screen_width, self.screen_height))

    def load_map(self, path):
        """Load the map"""
        im = Image.open(path)
        im = im.resize((self.screen_width, self.screen_height), Image.ANTIALIAS)
        # Convert the Image object into a TkPhoto object
        self.tkimage = ImageTk.PhotoImage(im)
        self.canvas.create_image(self.screen_width/2, self.screen_height/2, image=self.tkimage)

    def add_robot(self):
        pass

    def start(self):
        """Launch the game.

        Note: This is the method to override when creating your own game.

        """
        #debug
        print "Width " + str(self.screen_width)
        print "height " + str(self.screen_height)

        # Calibration
        self.x_factors, self.y_factors = self.do_calibration()

        #debug
        print "X factors:"
        print "alpha: " + str(self.x_factors[0])
        print "beta: " + str(self.x_factors[1])
        print "delta: " + str(self.x_factors[2])

        print "Y factors:"
        print "alpha: " + str(self.y_factors[0])
        print "beta: " + str(self.y_factors[1])
        print "delta: " + str(self.y_factors[2])

        # Define the width and height of a rectangle on the map,
        # and then create an array that represent the map
        self.rec_width = self.screen_width / 10
        self.rec_height = self.screen_height / 5
        self.board = self._create_board(5, 10)

        # self.robot_drawing.draw(self.robot_leds)
        self._init_servers()
        self.draw_robots()
        self.canvas.pack(fill=Tkinter.BOTH, expand=1)

        self.canvas.after(100, self._update_map)
        self.root.mainloop()

    def stop(self):
        """Stop the game."""
        self.root.quit()

    def do_calibration(self):
        """Draw three crosshairs and then return the calibration's factors
        (x_factors and y_factors) using the _calculate_calibration method.
        """

        offset = 50
        # Top left crosshair
        x_crosshair = offset
        y_crosshair = offset
        crosshair = Crosshair(self.root, self.canvas, x_crosshair, y_crosshair)
        top_left_led = crosshair.get_led(self.sensor)
        x1_screen, y1_screen = x_crosshair, y_crosshair
        x1_wiimote, y1_wiimote = top_left_led['X'], top_left_led['Y']
        #debug
        print "Screen: X: " + str(x1_screen) + " Y: " + str(y1_screen)
        print "Wiimote: X: " + str(x1_wiimote) + " Y: " + str(y1_wiimote)

        # Bottom left crosshair
        x_crosshair = offset
        y_crosshair = self.screen_height - offset
        crosshair = Crosshair(self.root, self.canvas, x_crosshair, y_crosshair)
        bottom_left_led = crosshair.get_led(self.sensor)
        x2_screen, y2_screen = x_crosshair, y_crosshair
        x2_wiimote, y2_wiimote = bottom_left_led['X'], bottom_left_led['Y']
        #debug
        print "Screen: X: " + str(x2_screen) + " Y: " + str(y2_screen)
        print "Wiimote: X: " + str(x2_wiimote) + " Y: " + str(y2_wiimote)

        # Third crosshair
        x_crosshair = self.screen_width - offset*10
        y_crosshair = self.screen_height / 2.
        crosshair = Crosshair(self.root, self.canvas, x_crosshair, y_crosshair)
        mid_right_led = crosshair.get_led(self.sensor)
        x3_screen, y3_screen = x_crosshair, y_crosshair
        x3_wiimote, y3_wiimote = mid_right_led['X'], mid_right_led['Y']
        #debug
        print "Screen: X: " + str(x3_screen) + " Y: " + str(y3_screen)
        print "Wiimote: X: " + str(x3_wiimote) + " Y: " + str(y3_wiimote)

        leds_location_screen = [[x1_screen, y1_screen],
                                [x2_screen, y2_screen],
                                [x3_screen, y3_screen]]

        leds_location_wiimote = [[x1_wiimote, self.sensor.height_resolution-y1_wiimote],
                                 [x2_wiimote, self.sensor.height_resolution-y2_wiimote],
                                 [x3_wiimote, self.sensor.height_resolution-y3_wiimote]]

        return(self._calculate_calibration(leds_location_screen,
                                           leds_location_wiimote))

    def _calculate_calibration(self, leds_location_screen,
                               leds_location_wiimote):
        """Return the calibration's factors (x_factors and y_factors)

        :param leds_location_screen: e.g [[x1, y1], [x2, y2], [x3, y3]]
        :param leds_location_wiimote: e.g [[x1, y1], [x2, y2], [x3, y3]]

        For the calculation, see the pdf at the address :
        http://www.ti.com/lit/an/slyt277/slyt277.pdf, equation (8)

        """
        A = copy.deepcopy(leds_location_wiimote)
        for row in A:
            row.append(1)
        delta = numpy.linalg.det(A)

        A_x1 = copy.deepcopy(leds_location_screen)
        i = 0
        for row in A_x1:
            row[1] = leds_location_wiimote[i][1]
            row.append(1)
            i += 1
        delta_x1 = numpy.linalg.det(A_x1)

        A_x2 = copy.deepcopy(leds_location_wiimote)
        i = 0
        for row in A_x2:
            row[1] = leds_location_screen[i][0]
            row.append(1)
            i += 1
        delta_x2 = numpy.linalg.det(A_x2)

        A_x3 = copy.deepcopy(leds_location_wiimote)
        i = 0
        for row in A_x3:
            row.append(leds_location_screen[i][0])
            i += 1
        delta_x3 = numpy.linalg.det(A_x3)

        A_y1 = copy.deepcopy(leds_location_screen)
        i = 0
        for row in A_y1:
            row[0] = row[1]
            row[1] = leds_location_wiimote[i][1]
            row.append(1)
            i += 1
        delta_y1 = numpy.linalg.det(A_y1)

        A_y2 = copy.deepcopy(leds_location_wiimote)
        i = 0
        for row in A_y2:
            row[1] = leds_location_screen[i][1]
            row.append(1)
            i += 1
        delta_y2 = numpy.linalg.det(A_y2)

        A_y3 = copy.deepcopy(leds_location_wiimote)
        i = 0
        for row in A_y3:
            row.append(leds_location_screen[i][1])
            i += 1
        delta_y3 = numpy.linalg.det(A_y3)

        alpha_x = delta_x1 / delta
        beta_x = delta_x2 / delta
        delta_x = delta_x3 / delta

        alpha_y = delta_y1 / delta
        beta_y = delta_y2 / delta
        delta_y = delta_y3 / delta

        x_factors = [alpha_x, beta_x, delta_x]
        y_factors = [alpha_y, beta_y, delta_y]

        #debug
        print 'X :'
        print x_factors
        print 'Y :'
        print y_factors
        # time.sleep(10)

        return x_factors, y_factors

    def _update_map(self):
        """Update the map. e.g Update circles' location and
        draw rectangles when needed.

        """
        leds = self.robot_leds
        #debug
        print leds
        #debug
        r = RobotDrawing(self.canvas)

        # Front led
        x1 = leds['front']['X']
        y1 = leds['front']['Y']

        if self._is_led_on_screen(x1, y1):
            num_column = int(x1 / self.rec_width)
            num_row = int(y1 / self.rec_height)
            x = self.rec_width * num_column
            y = self.rec_height * num_row
            #if not self._is_rec_already_drawn(num_row, num_column):
                #self._draw_rec(x, y, self.rec_width, self.rec_height, fill_color='#fb0')
                #self.board[num_row][num_column] = 1

        # Update the drawing of the robot
        # self.robot_drawing.draw(leds, self.width_offset, self.height_offset)
        # self.robot_drawing.draw(leds)

        #debug : I simulate the drawing of two other robots
        # self.robot_drawing.draw(leds)
        # self.robot_drawing.draw(leds)

        self.draw_robots()

        #debug : the delay is shorter
        self.canvas.after(100, self._update_map)

    def _is_rec_already_drawn(self, num_row, num_column):
        """Return True if a rectangle is already drawn."""
        return self.board[num_row][num_column] == 1

    def _is_led_on_screen(self, x, y):
        """Return if the led is on the screen.
        """
        is_x_on_screen = ((x > -1) and (x < self.screen_width))
        is_y_on_screen = ((y > -1) and (y < self.screen_height))
        return is_x_on_screen and is_y_on_screen

    def _draw_rec(self, x, y, width, height, outline_color='#fb0', fill_color=None):
        """Draw a rectangle."""
        self.canvas.create_rectangle(x, y, x+width, y+height, outline=outline_color, fill=fill_color)


class Crosshair(object):
    """Create a Crosshair object.

    :param root: Main window of the application.
    :param canvas: Canvas of the application.
    :param x: x location of the Crosshair.
    :param y: y location of the Crosshair.
    :param rad: Crosshair's radius.
    :param color: Crosshair's color.

    """
    def __init__(self, root, canvas, x, y, rad=30, color="red"):
        super(Crosshair, self).__init__()
        self.root = root
        self.canvas = canvas
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        self.circle = None
        self.horizontal_line = None
        self.vertical_line = None

    def get_led(self, sensor):
        """Draw a crosshair, set and return the location of the led."""
        self.sensor = sensor
        self.draw()
        self.canvas.after(500, self._get_led)
        self.canvas.pack(fill=Tkinter.BOTH, expand=1)
        self.root.mainloop()
        return self.led

    def _get_led(self):
        """This method wait until a led is detected,
        then set self.led = led.

        Confusing because of the way Tkinter works.

        """
        leds = self.sensor.get_leds()
        led = leds[0]
        while led['X'] == -1:
            time.sleep(0.5)
            leds = self.sensor.get_leds()
            led = leds[0]
        self.delete()
        self.root.quit()
        self.led = led

    def draw(self):
        """Draw the Crosshair on the screen."""
        # Before drawing, we make sure that the crosshair
        # is not drawn somewhere else
        if self.circle is not None:
            self.delete
        self._create_oval()
        self._create_cross()

    def _create_oval(self):
        """Draw an oval."""
        self.circle = self.canvas.create_oval(self.x-self.rad, self.y-self.rad,
                                              self.x+self.rad, self.y+self.rad,
                                              outline=self.color, width=2)

    def _create_cross(self):
        """Draw a cross."""
        self.horizontal_line = self.canvas.create_line(self.x-self.rad, self.y,
                                                       self.x+self.rad, self.y,
                                                       width=2, fill=self.color)
        self.vertical_line = self.canvas.create_line(self.x, self.y-self.rad,
                                                     self.x, self.y+self.rad,
                                                     width=2, fill=self.color)

    def delete(self):
        """Delete the crosshair on the canvas."""
        self.canvas.delete(self.circle)
        self.canvas.delete(self.horizontal_line)
        self.canvas.delete(self.vertical_line)
