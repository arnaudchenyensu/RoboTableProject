# import Tkinter
import mtTkinter as Tkinter
import time
import numpy
import copy
import socket


class Game(object):
    """Create a game.

    :param robot: Robot object used on the table.
    :param gui: (optional) GUI object.
    :param remote_server_object: (optional) This object will be copied and used
        to simulate each other remote RoboTable.
    :param main_server: (optional) True if this is the main server.
    :param addr_remote_servers: (optional) A list containing the address
        of the other RoboTables.
    :param remote: (optional) If true, indicates that the object is a remote server.
        If false, the initialisation of the screen is performed.
    :param name: (optional) Name of the game.

    **Note:** most of the arguments are optionals to facilitate the creation of the
    remote_server_object (but have to be provided if remote=false).

    """
    def __init__(self, robot, gui=None, game_management=None,
                 remote_server_object=None,
                 main_server=True, addr_remote_servers=None,
                 remote=False, name=None):
        self.name = name
        self.robot = robot
        self.sensor = robot.sensor
        self.game_management = game_management
        self.remote_server_object = remote_server_object
        self.ready = False

        self.x_factors = None
        self.y_factors = None

        self.addr = self.get_addr()
        self.main_server = main_server
        self.addr_remote_servers = addr_remote_servers
        self.remote_servers = []
        self.servers_ready = False

        self.remote = remote
        # Graphic variables. Initialized only if the method
        # self._init_graphic is called
        self.gui = gui
        if self.gui is not None:
            self.root = self.gui.root
            self.screen_width = self.gui.screen_width
            self.screen_height = self.gui.screen_height
            self.canvas = self.gui.canvas
            self.robot.robot_drawing.canvas = self.canvas

    def load_map(self, path):
        self.gui.load_map(path)

    def is_main_server(self):
        """Return if the server is the main server."""
        return self.main_server

    def get_addr(self):
        """Return the ip address of the server.

        **Note**: the solution was find on `Stackoverflow <http://goo.gl/D6FKrq>`_.

        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com", 80))
        addr = s.getsockname()[0]
        s.close()
        return addr

    def draw_robots(self):
        """Draw robots on the table."""
        for server in self.remote_servers:
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
        """Return a list that simulate a map."""
        board = []
        for i in range(rows):
            board.append([0] * columns)
        return board

    def start(self):
        """Launch the game.

        **Note:** This is the method to override when creating your own game.

        """

        self.game_management.start()
        self.x_factors = self.game_management.x_factors
        self.y_factors = self.game_management.y_factors
        #debug
        # print "Width " + str(self.screen_width)
        # print "height " + str(self.screen_height)

        #debug
        # print "X factors:"
        # print "alpha: " + str(self.x_factors[0])
        # print "beta: " + str(self.x_factors[1])
        # print "delta: " + str(self.x_factors[2])

        # print "Y factors:"
        # print "alpha: " + str(self.y_factors[0])
        # print "beta: " + str(self.y_factors[1])
        # print "delta: " + str(self.y_factors[2])

        # Define the width and height of a rectangle on the map,
        # and then create an array that represent the map
        self.rec_width = self.screen_width / 10
        self.rec_height = self.screen_height / 5
        self.board = self._create_board(5, 10)

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
        self.robot.draw(leds)

        # self.draw_robots()
        self.canvas.pack(fill=Tkinter.BOTH, expand=1)

        self.canvas.after(100, self._update_map)
        self.root.mainloop()

    def stop(self):
        """Stop the game."""
        self.root.quit()

    def _update_map(self):
        """Update the map. e.g Update circles' location and
        draw rectangles when needed.

        """
        #debug
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
        self.robot.draw(leds)

        # if self._is_led_on_screen(x1, y1):
        #     num_column = int(x1 / self.rec_width)
        #     num_row = int(y1 / self.rec_height)
        #     x = self.rec_width * num_column
        #     y = self.rec_height * num_row
            #if not self._is_rec_already_drawn(num_row, num_column):
                #self._draw_rec(x, y, self.rec_width, self.rec_height, fill_color='#fb0')
                #self.board[num_row][num_column] = 1
        self.draw_robots()

        #debug : the delay is shorter
        self.canvas.after(100, self._update_map)

    def _is_rec_already_drawn(self, num_row, num_column):
        """Return True if a rectangle is already drawn."""
        return self.board[num_row][num_column] == 1

    def _is_led_on_screen(self, x, y):
        """Return if the led is on the screen."""
        is_x_on_screen = ((x > -1) and (x < self.screen_width))
        is_y_on_screen = ((y > -1) and (y < self.screen_height))
        return is_x_on_screen and is_y_on_screen

    def _draw_rec(self, x, y, width, height, outline_color='#fb0', fill_color=None):
        """Draw a rectangle."""
        self.canvas.create_rectangle(x, y, x+width, y+height, outline=outline_color, fill=fill_color)


class GameManagement(object):
    """docstring for GameManagement"""
    def __init__(self, sensor, gui, main_server=True):
        self.main_server = main_server
        self.gui = gui
        self.screen_width = self.gui.screen_width
        self.screen_height = self.gui.screen_height
        self.sensor = sensor
        self._x_factors = None
        self._y_factors = None

    @property
    def x_factors(self):
        if self._x_factors is None:
            #TODO Add exception
            print "The calibration was not done"
        return self._x_factors

    @property
    def y_factors(self):
        if self._y_factors is None:
            #TODO Add exception
            print "The calibration was not done"
        return self._y_factors

    def start(self):
        # Calibration
        self._x_factors, self._y_factors = self.do_calibration()
        # self.send_addr_remote_to_remote()
        # self._init_servers()
        # self.ready = True
        # if self.is_main_server():
        #     self.synchronise_servers()
        # else:
        #     self.wait_servers()

        # if self.remote is False:
        #     self._init_graphic()
        # self.robot.robot_drawing.canvas = self.canvas

    def launch_games(self):
        for server in self.remote_servers:
            server.sensor.post(action='servers_ready')

    def _init_servers(self):
        """Create the remote servers' object and
        append to the list self.remote_servers.
        """
        for addr_remote_server in self.addr_remote_servers:
            remote_server = copy.deepcopy(self.remote_server_object)
            remote_server.robot.sensor.addr = addr_remote_server
            remote_server.robot.robot_drawing.canvas = self.canvas
            self.remote_servers.append(remote_server)

    def wait_servers(self):
        while self.servers_ready is False:
            time.sleep(1)

    def synchronise_servers(self):
        print 'Waiting for the other servers...'
        while self.servers_ready is False:
            if self.is_servers_ready():
                self.launch_games()
                self.servers_ready = True
            else:
                time.sleep(1)
        print 'Game launched.'

    def is_servers_ready(self):
        for server in self.remote_servers:
            if server.sensor.get(action='is_ready') == 'False':
                return False
        return True

    def _calculate_calibration(self, leds_location_screen,
                               leds_location_wiimote):
        """Return the calibration's factors (x_factors and y_factors)

        :param leds_location_screen: e.g [[x1, y1], [x2, y2], [x3, y3]]
        :param leds_location_wiimote: e.g [[x1, y1], [x2, y2], [x3, y3]]

        For the calculation, see the pdf `here <http://goo.gl/pWYifa>`_, equation (8)

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

    def do_calibration(self):
        """Draw three crosshairs and then return the calibration's factors
        (x_factors and y_factors) using the _calculate_calibration method.
        """

        offset = 50
        # Top left crosshair
        x_crosshair = offset
        y_crosshair = offset
        top_left_led = self._get_led_crosshair(x_crosshair, y_crosshair)
        x1_screen, y1_screen = x_crosshair, y_crosshair
        x1_wiimote, y1_wiimote = top_left_led['X'], top_left_led['Y']

        # Bottom left crosshair
        x_crosshair = offset
        y_crosshair = self.screen_height - offset
        bottom_left_led = self._get_led_crosshair(x_crosshair, y_crosshair)
        x2_screen, y2_screen = x_crosshair, y_crosshair
        x2_wiimote, y2_wiimote = bottom_left_led['X'], bottom_left_led['Y']

        # Third crosshair
        x_crosshair = self.screen_width - offset*10
        y_crosshair = self.screen_height / 2.
        mid_right_led = self._get_led_crosshair(x_crosshair, y_crosshair)
        x3_screen, y3_screen = x_crosshair, y_crosshair
        x3_wiimote, y3_wiimote = mid_right_led['X'], mid_right_led['Y']

        leds_location_screen = [[x1_screen, y1_screen],
                                [x2_screen, y2_screen],
                                [x3_screen, y3_screen]]

        leds_location_wiimote = [[x1_wiimote, self.sensor.height_resolution-y1_wiimote],
                                 [x2_wiimote, self.sensor.height_resolution-y2_wiimote],
                                 [x3_wiimote, self.sensor.height_resolution-y3_wiimote]]

        return(self._calculate_calibration(leds_location_screen,
                                           leds_location_wiimote))


    def _get_led_crosshair(self, x, y):
        """Draw a crosshair and return the location of the led."""
        crosshair = self.gui.draw_crosshair(x, y)
        led = self._get_led()
        crosshair.delete()
        return led

    def _get_led(self):
        """When a led is detected, return its location."""
        leds = self.sensor.get_leds()
        led = leds[0]
        while led['X'] == -1:
            time.sleep(0.5)
            leds = self.sensor.get_leds()
            led = leds[0]
        return led
