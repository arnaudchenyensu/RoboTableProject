import Tkinter
import Image
import ImageTk
from tracking.wiimote import Wiimote
from robot.robot import Robot


class Game(object):
    """docstring for Game"""
    def __init__(self, name):
        self.name = name
        self.root = Tkinter.Tk()
        self.screen_width, self.screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self._set_full_screen()
        self.robot = Robot(Wiimote())
        self.canvas = Tkinter.Canvas(self.root)

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
        # Define the width and height of a rectangle on the map,
        # and then create an array that represent the map
        self.rec_width = self.screen_width / 10
        self.rec_height = self.screen_height / 5
        self.board = self.create_board(5, 10)

        # Create the three circles that represent the leds
        self.circle1 = self.canvas.create_oval(10, 50, 50, 80, outline="red", fill="green", width=2)
        self.circle2 = self.canvas.create_oval(10, 50, 50, 80, outline="red", fill="green", width=2)
        self.circle3 = self.canvas.create_oval(10, 50, 50, 80, outline="red", fill="green", width=2)
        self.canvas.pack(fill=Tkinter.BOTH, expand=1)

        self.canvas.after(50, self._update_map())
        self.root.mainloop()

    def _update_map(self):
        """Update the map. e.g Update circles' location and draw rectangles when needed"""
        rad = 10
        leds = self.robot.leds
        print leds
        # Front led
        x1 = leds['front']['X']
        y1 = self.update_y_coordinate(leds['front']['Y'])

        # Left led
        x2 = leds['left']['X']
        y2 = self.update_y_coordinate(leds['left']['Y'])

        # Right led
        x3 = leds['right']['X']
        y3 = self.update_y_coordinate(leds['right']['Y'])

        if self.is_led_on_screen(x1, y1):
            num_column = int(x1 / self.rec_width)
            num_row = int(y1 / self.rec_height)
            x = self.rec_width * num_column
            y = self.rec_height * num_row
            if not self._is_rec_already_drawn(num_row, num_column):
                self.draw_rec(x, y, self.rec_width, self.rec_height)
                self.board[num_row][num_column] = 1

        self.canvas.coords(self.circle1, x1-rad, y1-rad, x1+rad, y1+rad)
        self.canvas.coords(self.circle2, x2-rad, y2-rad, x2+rad, y2+rad)
        self.canvas.coords(self.circle3, x3-rad, y3-rad, x3+rad, y3+rad)
        self.canvas.after(50, self._update_map)

    def _is_rec_already_drawn(self, num_row, num_column):
        return self.board[num_row][num_column] == 1

    def is_led_on_screen(self, x, y):
        """Return if the led is on the screen.
        Note: Don't forget to use the update_y_coordinate(self, y) method before
        """
        is_x_on_screen = x > -1 and x < self.screen_width
        is_y_on_screen = y > -1 and y < self.screen_height
        return is_x_on_screen and is_y_on_screen

    def update_y_coordinate(self, y):
        """Update the y coordinate for Tkinter because (0, 0) correspond at the top left corner for Tkinter
        but correspond at the bottom left corner for the Wiimote
        """
        return self.screen_height - y

    def draw_rec(self, x, y, width, height, outline_color='#fb0', fill_color='#fb0'):
        self.canvas.create_rectangle(x, y, x+width, y+height, outline=outline_color, fill=fill_color)
