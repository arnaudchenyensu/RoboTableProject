import Tkinter
import Image
import ImageTk
from tracking.wiimote import Wiimote
from robot.robot import Robot
import time


class Game(object):
    """docstring for Game"""
    def __init__(self, name):
        self.name = name
        self.root = Tkinter.Tk()
        self.screen_width, self.screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self._set_full_screen()
        self.sensor = Wiimote()
        self.robot = Robot(self.sensor)
        self.canvas = Tkinter.Canvas(self.root)
        self.robot_drawing = RobotDrawing(self.canvas, self.screen_height)

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
        self.do_calibration()

        # Define the width and height of a rectangle on the map,
        # and then create an array that represent the map
        self.rec_width = self.screen_width / 10
        self.rec_height = self.screen_height / 5
        self.board = self.create_board(5, 10)

        self.robot_drawing.draw(self.robot.leds, self.screen_width, self.screen_height)
        self.canvas.pack(fill=Tkinter.BOTH, expand=1)

        self.canvas.after(100, self._update_map)
        self.root.mainloop()

    def do_calibration(self):

        offset = 50
        # Top left crosshair
        x_crosshair = offset
        y_crosshair = offset
        crosshair = Crosshair(self.root, self.canvas, x_crosshair, y_crosshair)
        top_left = crosshair.get_led(self.sensor)

        # Top right crosshair
        x_crosshair = self.screen_width - offset
        y_crosshair = offset
        crosshair = Crosshair(self.root, self.canvas, x_crosshair, y_crosshair)
        top_right = crosshair.get_led(self.sensor)

        # Bottom left crosshair
        x_crosshair = offset
        y_crosshair = self.screen_height - offset
        crosshair = Crosshair(self.root, self.canvas, x_crosshair, y_crosshair)
        bottom_left = crosshair.get_led(self.sensor)

        # Bottom right crosshair
        x_crosshair = self.screen_width - offset
        y_crosshair = self.screen_height - offset
        crosshair = Crosshair(self.root, self.canvas, x_crosshair, y_crosshair)
        bottom_right = crosshair.get_led(self.sensor)

        self.sx = self.get_scaling_factor(self.screen_width - offset, offset,
                                          top_right['X'], top_left['X'])
        self.sy = self.get_scaling_factor(self.screen_height - offset, offset,
                                          top_left['Y'], bottom_left['Y'])

    def get_scaling_factor(self, screen_max, screen_min, wii_max, wii_min):
        screen_max = float(screen_max)
        wii_max = float(wii_max)
        # return ((screen_max - screen_min) / (wii_max - wii_min))
        return ((wii_max - wii_min) / (screen_max - screen_min))
        # self.canvas.pack(fill=Tkinter.BOTH, expand=1)
        # self.canvas.after(500, crosshair.draw)
        # self.root.after(10000, self.root.quit)
        # self.root.mainloop()

        # leds = self.sensor.get_leds()
        # led = leds[0]
        # print leds
        # while led['X'] == -1:
        #     leds = self.sensor.get_leds()
        #     led = leds[0]
        # self.width_offset, self.height_offset = self.calculate_offset(led['X'], led['Y'], x_crosshair, y_crosshair)
        # print "width_offset: " + str(self.width_offset) + " height_offset: " + str(self.height_offset)
        # crosshair.delete()

    def calculate_offset(self, x_led, y_led, x_crosshair, y_crosshair):
        width_offset = x_crosshair - x_led
        height_offset = y_led + y_crosshair - self.screen_height
        return width_offset, height_offset

    def _update_map(self):
        """Update the map. e.g Update circles' location and draw rectangles when needed"""
        leds = self.robot.leds
        print leds

        # Front led
        x1 = leds['front']['X']
        y1 = self.update_y_coordinate(leds['front']['Y'])

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
        self.robot_drawing.draw(leds, self.sx, self.sy)

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

    def update_y_coordinate(self, y):
        """Update the y coordinate for Tkinter because (0, 0) correspond at the top left corner for Tkinter
        but correspond at the bottom left corner for the Wiimote
        """
        return self.screen_height - y

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
        # self.draw()
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
        self.circle = self.canvas.create_oval(self.x-self.rad, self.y-self.rad, self.x+self.rad, self.y+self.rad, outline=self.color, width=2)

    def _create_lines(self):
        self.horizontal_line = self.canvas.create_line(self.x-self.rad, self.y, self.x+self.rad, self.y, width=2, fill=self.color)
        self.vertical_line = self.canvas.create_line(self.x, self.y-self.rad, self.x, self.y+self.rad, width=2, fill=self.color)

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

    def draw(self, leds, sx, sy, width_offset=0, height_offset=0):
        # sx = screen_width / 1024.
        # self.sy = screen_height / 768.
        self.sy = sy
        # debug
        print "sx: " + str(sx) + " sy: " + str(self.sy)

        # Front led
        x1 = leds['front']['X'] / sx
        y1 = self._update_y_coordinate(leds['front']['Y'])

        #debug
        print "sx_X1: " + str(x1) + " sy_Y1: " + str(y1)

        # Left led
        x2 = leds['left']['X'] / sx
        y2 = self._update_y_coordinate(leds['left']['Y'])

        # Right led
        x3 = leds['right']['X'] / sx
        y3 = self._update_y_coordinate(leds['right']['Y'])

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

    def _update_y_coordinate(self, y):
        """Update the y coordinate for Tkinter because (0, 0) correspond at the top left corner for Tkinter
        but correspond at the bottom left corner for the Wiimote
        """
        return (768 - y) / self.sy
        # return y * self.sy
        # return y * self.sy
        # return (768 - y) * self.sy
