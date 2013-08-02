import mtTkinter as Tkinter
import time
import numpy
import copy
import socket
import math


class Game(object):
    """Create a game.

    :param robot: Robot object used on the table.
    :param sensor: Sensor object used to detect IRs.
    :param network: Network object used to communicate between tables.
    :param gui: GUI object.
    :param game_management: GameManagement object.
    :param addr_main_server: Main server's IP address.

    """
    def __init__(self, robot, sensor, network, gui, game_management, addr_main_server):
        self.robot = robot
        self.sensor = sensor
        self.network = network
        self.game_management = game_management
        self.addr_main_server = addr_main_server

        self.robots = []
        self.x_factors = None
        self.y_factors = None
        self.addr = self.get_addr()
        self.servers = []

        # Graphic variables.
        self.gui = gui
        self.root = self.gui.root
        self.screen_width = self.gui.screen_width
        self.screen_height = self.gui.screen_height
        self.canvas = self.gui.canvas
        self.robot.robot_drawing.canvas = self.canvas

    def load_map(self, path):
        """Load the map on the canvas."""
        self.gui.load_map(path)

    def is_main_server(self):
        """Return if the server is the main server."""
        return self.addr == self.addr_main_server

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
        if len(self.robots) == 0:
            for i in range(len(self.servers)):
                self.robots.append(self.gui.get_robot_drawing())

        for i in range(len(self.servers)):
            leds = self.network.get_irs(self.servers[i])
            leds = self._apply_calibration_factors(leds, self.x_factors, self.y_factors)
            self.robots[i].draw(leds)

    def _apply_calibration_factors(self, leds, x_factors, y_factors):
        """Return the leds' location calibrated."""
        for led in leds:
            leds[led]['X'] = (leds[led]['X'] * x_factors[0]
                              + leds[led]['Y'] * x_factors[1]
                              + x_factors[2])
            leds[led]['Y'] = (leds[led]['X'] * y_factors[0]
                              + (self.sensor.height_resolution - leds[led]['Y']) * y_factors[1]
                              + y_factors[2])
        return leds

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

        self.game_management.start(self.addr_main_server, self.is_main_server(), self.addr)
        self.x_factors = self.game_management.x_factors
        self.y_factors = self.game_management.y_factors
        self.servers = self.game_management.servers

        # Define the width and height of a rectangle on the map,
        # and then create an array that represent the map
        self.rec_width = self.screen_width / 10
        self.rec_height = self.screen_height / 5
        self.board = self._create_board(5, 10)

        self.draw_robots()
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
    """docstring for GameManagement.

    :param sensor: Sensor object used to detect IRs.
    :param gui: GUI object.
    :param network: Network object used to communicate between tables.
    :param nb_servers: Number of player/server.

    """
    def __init__(self, sensor, gui, network, nb_servers):
        self.sensor = sensor
        self.gui = gui
        self.network = network

        self.screen_width = self.gui.screen_width
        self.screen_height = self.gui.screen_height
        self._x_factors = None
        self._y_factors = None

        self.servers = []
        self.nb_servers = nb_servers
        self.ready = False
        self.servers_ready = False

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

    def start(self, addr_main_server, is_main_server, addr):
        """Execute the needed steps before launching a game.

        :param addr_main_server: Main server's IP address.
        :param is_main_server: True if this is the main server.
        :param addr: address of the server on which this method is called.

        """
        if is_main_server:
            self.servers.append(addr)
            self.wait_addr_servers()
            self._x_factors, self._y_factors = self.do_calibration()
            self.ready = True
            self.send_list_servers()
            self.synchronise_servers()
        else:
            self.network.send_addr(addr_main_server, addr)
            self._x_factors, self._y_factors = self.do_calibration()
            self.ready = True
            self.wait_servers()

    def send_list_servers(self):
        """Send a list containing the address of all
        servers to each server.

        """
        for addr in self.servers[1:]:
            self.network.send_list_servers(addr, self.servers)

    def wait_addr_servers(self):
        """Wait that all servers have sent their address."""
        while len(self.servers) != self.nb_servers:
            time.sleep(1)

    def launch_game(self):
        """Launch the game on each server."""
        for addr in self.servers[1:]:
            self.network.launch(addr)

    def wait_servers(self):
        """Wait that all servers are ready."""
        while self.servers_ready is False:
            time.sleep(1)

    def synchronise_servers(self):
        """Synchronise each servers and launch the game."""
        print 'Waiting for the other servers...'
        while self.servers_ready is False:
            if self.is_servers_ready():
                self.launch_game()
                self.servers_ready = True
            else:
                time.sleep(1)
        print 'Game launched.'

    def is_servers_ready(self):
        """Return true if all servers are ready."""
        for addr_server in self.servers:
            if  self.network.is_ready(addr_server) == False:
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

    def _calculate_calibration_n(self, leds_location_screen,
                               leds_location_wiimote):
        """See equation (10)"""
        if len(leds_location_wiimote) != len(leds_location_screen):
            #TODO add throw exception
            print 'The two list have not the same length'
        else:
            n = len(leds_location_wiimote)

        x_k = copy.deepcopy(leds_location_screen)
        for i in range(n):
            x_k[i] = x_k[i][0]
        x_k = numpy.array(x_k)

        y_k = copy.deepcopy(leds_location_screen)
        for i in range(n):
            y_k[i] = y_k[i][1]
        y_k = numpy.array(y_k)

        x_prime_k = copy.deepcopy(leds_location_wiimote)
        for i in range(n):
            x_prime_k[i] = x_prime_k[i][0]
        x_prime_k = numpy.array(x_prime_k)

        y_prime_k = copy.deepcopy(leds_location_wiimote)
        for i in range(n):
            y_prime_k[i] = y_prime_k[i][1]
        y_prime_k = numpy.array(y_prime_k)

        a = math.fsum(x_prime_k**2)
        b = math.fsum(y_prime_k**2)
        c = math.fsum(x_prime_k * y_prime_k)
        d = math.fsum(x_prime_k)
        e = math.fsum(y_prime_k)

        X_1 = math.fsum(x_prime_k * x_k)
        X_2 = math.fsum(y_prime_k * x_k)
        X_3 = math.fsum(x_k)

        Y_1 = math.fsum(x_prime_k * y_k)
        Y_2 = math.fsum(y_prime_k * y_k)
        Y_3 = math.fsum(y_k)

        delta = n * (a*b-c**2) + 2*c*d*e - a*e**2 - b*d**2
        delta_x1 = n * (X_1*b-X_2*c) + e * (X_2*d-X_1*e) + X_3 * (c*e-b*d)
        delta_x2 = n * (X_2*a-X_1*c) + d * (X_1*e-X_2*d) + X_3 * (c*d-a*e)
        delta_x3 = X_3 * (a*b-c**2) + X_1 * (c*e-b*d) + X_2 * (c*d-a*e)

        delta_y1 = n * (Y_1*b-Y_2*c) + e * (Y_2*d-Y_1*e) + Y_3 * (c*e-b*d)
        delta_y2 = n * (Y_2*a-Y_1*c) + d * (Y_1*e-Y_2*d) + Y_3 * (c*d-a*e)
        delta_y3 = Y_3 * (a*b-c**2) + Y_1 * (c*e-b*d) + Y_2 * (c*d-a*e)

        alpha_x = delta_x1 / delta
        beta_x = delta_x2 / delta
        delta_x = delta_x3 / delta

        alpha_y = delta_y1 / delta
        beta_y = delta_y2 / delta
        delta_y = delta_y3 / delta

        x_factors = [alpha_x, beta_x, delta_x]
        y_factors = [alpha_y, beta_y, delta_y]

        return x_factors, y_factors


    def do_calibration(self):
        """Draw X crosshairs and then return the calibration's factors
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

        # Top right crosshair
        x_crosshair = self.screen_width - offset
        y_crosshair = offset
        top_right_led = self._get_led_crosshair(x_crosshair, y_crosshair)
        x3_screen, y3_screen = x_crosshair, y_crosshair
        x3_wiimote, y3_wiimote = top_right_led['X'], top_right_led['Y']

        # Bottom right crosshair
        x_crosshair = self.screen_width - offset
        y_crosshair = self.screen_height - offset
        bottom_right_led = self._get_led_crosshair(x_crosshair, y_crosshair)
        x4_screen, y4_screen = x_crosshair, y_crosshair
        x4_wiimote, y4_wiimote = bottom_right_led['X'], bottom_right_led['Y']

        # Middle crosshair
        x_crosshair = self.screen_width / 2.
        y_crosshair = self.screen_height / 2.
        middle_led = self._get_led_crosshair(x_crosshair, y_crosshair)
        x5_screen, y5_screen = x_crosshair, y_crosshair
        x5_wiimote, y5_wiimote = middle_led['X'], middle_led['Y']

        leds_location_screen = [[x1_screen, y1_screen],
                                [x2_screen, y2_screen],
                                [x3_screen, y3_screen],
                                [x4_screen, y4_screen],
                                [x5_screen, y5_screen]]

        leds_location_wiimote = [[x1_wiimote, self.sensor.height_resolution - y1_wiimote],
                                 [x2_wiimote, self.sensor.height_resolution - y2_wiimote],
                                 [x3_wiimote, self.sensor.height_resolution - y3_wiimote],
                                 [x4_wiimote, self.sensor.height_resolution - y4_wiimote],
                                 [x5_wiimote, self.sensor.height_resolution - y5_wiimote]]

        return(self._calculate_calibration_n(leds_location_screen,
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
