import Tkinter
import Image
import ImageTk
from tracking.wiimote import Wiimote
from robot.robot import Robot
import time
import numpy
import copy


class Game(object):
    """docstring for Game"""
    def __init__(self, name):
        self.name = name
        self.root = Tkinter.Tk()
        self.screen_width, self.screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self._set_full_screen()
        self.sensor = Wiimote(1024, 768)
        self.robot = Robot(self.sensor)
        self.canvas = Tkinter.Canvas(self.root)
        self.robot_drawing = RobotDrawing(self.canvas, self.screen_height)

        self.x_factors = None
        self.y_factors = None

    @property
    def robot_leds(self):
        """Return the robot's leds location calibrated
           Note: You need to do the calibration first (once)
        """
        if self.x_factors is None:
            print "The calibration was not done"
            #TODO : add throw exception
            return False
        else:
            leds = self.robot.leds
            leds['front']['X'] = (leds['front']['X'] * self.x_factors[0]
                                  + leds['front']['Y'] * self.x_factors[1]
                                  + self.x_factors[2])
            leds['front']['Y'] = (leds['front']['X'] * self.y_factors[0]
                                  + (self.sensor.height_resolution - leds['front']['Y']) * self.y_factors[1]
                                  + self.y_factors[2])

            leds['left']['X'] = (leds['left']['X'] * self.x_factors[0]
                                 + leds['left']['Y'] * self.x_factors[1]
                                 + self.x_factors[2])
            leds['left']['Y'] = (leds['left']['X'] * self.y_factors[0]
                                 + (self.sensor.height_resolution - leds['left']['Y']) * self.y_factors[1]
                                 + self.y_factors[2])

            leds['right']['X'] = (leds['right']['X'] * self.x_factors[0]
                                  + leds['right']['Y'] * self.x_factors[1]
                                  + self.x_factors[2])
            leds['right']['Y'] = (leds['right']['X'] * self.y_factors[0]
                                  + (self.sensor.height_resolution - leds['right']['Y']) * self.y_factors[1]
                                  + self.y_factors[2])
            return leds

    def create_board(self, rows, columns):
        board = []
        for i in range(rows):
            board.append([0] * columns)
        return board

    def _set_full_screen(self):
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
        Note: Method to override when creating your own game
        """
        # Calibration
        self.x_factors, self.y_factors = self.do_calibration()

        # Define the width and height of a rectangle on the map,
        # and then create an array that represent the map
        self.rec_width = self.screen_width / 10
        self.rec_height = self.screen_height / 5
        self.board = self.create_board(5, 10)

        self.robot_drawing.draw(self.robot_leds)
        self.canvas.pack(fill=Tkinter.BOTH, expand=1)

        self.canvas.after(100, self._update_map)
        self.root.mainloop()

    def do_calibration(self):
        """Draw three crosshairs and then return x_factors and y_factors
           using the calculate_calibration method
        """

        offset = 50
        # Top left crosshair
        x_crosshair = offset
        y_crosshair = offset
        crosshair = Crosshair(self.root, self.canvas, x_crosshair, y_crosshair)
        top_left_led = crosshair.get_led(self.sensor)
        x1_screen, y1_screen = x_crosshair, y_crosshair
        x1_wiimote, y1_wiimote = top_left_led['X'], top_left_led['Y']

        # Bottom left crosshair
        x_crosshair = offset
        y_crosshair = self.screen_height - offset
        crosshair = Crosshair(self.root, self.canvas, x_crosshair, y_crosshair)
        bottom_left_led = crosshair.get_led(self.sensor)
        x2_screen, y2_screen = x_crosshair, y_crosshair
        x2_wiimote, y2_wiimote = bottom_left_led['X'], bottom_left_led['Y']

        # Third crosshair
        x_crosshair = self.screen_width - offset*10
        y_crosshair = self.screen_height / 2.
        crosshair = Crosshair(self.root, self.canvas, x_crosshair, y_crosshair)
        mid_right_led = crosshair.get_led(self.sensor)
        x3_screen, y3_screen = x_crosshair, y_crosshair
        x3_wiimote, y3_wiimote = mid_right_led['X'], mid_right_led['Y']

        leds_location_screen = [[x1_screen, y1_screen],
                                [x2_screen, y2_screen],
                                [x3_screen, y3_screen]]

        leds_location_wiimote = [[x1_wiimote, self.sensor.height_resolution-y1_wiimote],
                                 [x2_wiimote, self.sensor.height_resolution-y2_wiimote],
                                 [x3_wiimote, self.sensor.height_resolution-y3_wiimote]]

        return(self.calculate_calibration(leds_location_screen,
                                          leds_location_wiimote))

    def calculate_calibration(self, leds_location_screen,
                              leds_location_wiimote):
        """leds_location e.g [[x1, y1], [x2, y2], [x3, y3]],
           see the do_calibration method for the format.
           For the calculation, see the pdf at the address :
           http://www.ti.com/lit/an/slyt277/slyt277.pdf, equation (8)
           Return x_factors and y_factors
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
        time.sleep(10)

        return x_factors, y_factors

    def _update_map(self):
        """Update the map. e.g Update circles' location and
           draw rectangles when needed
        """
        leds = self.robot_leds
        print leds

        # Front led
        x1 = leds['front']['X']
        y1 = leds['front']['Y']

        if self.is_led_on_screen(x1, y1):
            num_column = int(x1 / self.rec_width)
            num_row = int(y1 / self.rec_height)
            x = self.rec_width * num_column
            y = self.rec_height * num_row
            # if not self._is_rec_already_drawn(num_row, num_column):
            #     self.draw_rec(x, y, self.rec_width, self.rec_height, fill_color='#fb0')
            #     self.board[num_row][num_column] = 1

        # Update the drawing of the robot
        # self.robot_drawing.draw(leds, self.width_offset, self.height_offset)
        self.robot_drawing.draw(leds)

        self.canvas.after(500, self._update_map)

    def _is_rec_already_drawn(self, num_row, num_column):
        return self.board[num_row][num_column] == 1

    def is_led_on_screen(self, x, y):
        """Return if the led is on the screen.
        Note: Don't forget to use the update_y_coordinate(self, y) method before
        """
        is_x_on_screen = ((x > -1) and (x < self.screen_width))
        is_y_on_screen = ((y > -1) and (y < self.screen_height))
        return is_x_on_screen and is_y_on_screen

    def draw_rec(self, x, y, width, height, outline_color='#fb0', fill_color=None):
        self.canvas.create_rectangle(x, y, x+width, y+height, outline=outline_color, fill=fill_color)


class Crosshair(object):
    """docstring for Crosshair"""
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
        self.sensor = sensor
        self.draw()
        self.canvas.after(500, self._get_led)
        self.canvas.pack(fill=Tkinter.BOTH, expand=1)
        self.root.mainloop()
        return self.led

    def _get_led(self):
        leds = self.sensor.get_leds()
        led = leds[0]
        while led['X'] == -1:
            time.sleep(0.5)
            leds = self.sensor.get_leds()
            led = leds[0]
        self.delete()
        self.root.quit()
        print led
        self.led = led

    def draw(self):
        # Before drawing, we make sure that the crosshair
        # is not drawn somewhere else
        if self.circle is not None:
            self.delete
        self._create_oval()
        self._create_lines()

    def _create_oval(self):
        self.circle = self.canvas.create_oval(self.x-self.rad, self.y-self.rad,
                                              self.x+self.rad, self.y+self.rad,
                                              outline=self.color, width=2)

    def _create_lines(self):
        self.horizontal_line = self.canvas.create_line(self.x-self.rad, self.y,
                                                       self.x+self.rad, self.y,
                                                       width=2, fill=self.color)
        self.vertical_line = self.canvas.create_line(self.x, self.y-self.rad,
                                                     self.x, self.y+self.rad,
                                                     width=2, fill=self.color)

    def delete(self):
        self.canvas.delete(self.circle)
        self.canvas.delete(self.horizontal_line)
        self.canvas.delete(self.vertical_line)


class RobotDrawing(object):
    """docstring for RobotDrawing"""
    def __init__(self, canvas, screen_height, rad=10, outline_color="red", fill_color="green"):
        self.canvas = canvas
        self.screen_height = screen_height
        self.rad = rad
        self.outline_color = outline_color
        self.fill_color = fill_color

        # Represent the leds drawing on the canvas:
        self._circle1 = None
        self._circle2 = None
        self._circle3 = None

    def draw(self, leds):

        # Front led
        x1 = leds['front']['X']
        y1 = leds['front']['Y']

        # Left led
        x2 = leds['left']['X']
        y2 = leds['left']['Y']

        # Right led
        x3 = leds['right']['X']
        y3 = leds['right']['Y']

        if not self._circle1:
            self._circle1 = self.canvas.create_oval(x1-self.rad, y1-self.rad, x1+self.rad, y1+self.rad,
                                                    outline=self.outline_color, fill=self.fill_color, width=2)
            self._circle2 = self.canvas.create_oval(x2-self.rad, y2-self.rad, x2+self.rad, y2+self.rad,
                                                    outline=self.outline_color, fill=self.fill_color, width=2)
            self._circle3 = self.canvas.create_oval(x3-self.rad, y3-self.rad, x3+self.rad, y3+self.rad,
                                                    outline=self.outline_color, fill=self.fill_color, width=2)
        else:
            self.canvas.coords(self._circle1, x1-self.rad, y1-self.rad, x1+self.rad, y1+self.rad)
            self.canvas.coords(self._circle2, x2-self.rad, y2-self.rad, x2+self.rad, y2+self.rad)
            self.canvas.coords(self._circle3, x3-self.rad, y3-self.rad, x3+self.rad, y3+self.rad)
