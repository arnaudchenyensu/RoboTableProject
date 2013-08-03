import mtTkinter as Tkinter
import Image
import ImageTk


class GUI(object):
    """docstring for GUI"""
    def __init__(self):
        self.root = None
        self.screen_width = None
        self.screen_height = None
        self.canvas = None
        self.init_graphic()
        self.set_full_screen()

    def init_graphic(self):
        """Initialize the graphical part using Tkinter."""
        self.root = Tkinter.Tk()
        self.screen_width, self.screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.set_full_screen()
        self.canvas = Tkinter.Canvas(self.root)
        self.canvas.pack(fill=Tkinter.BOTH, expand=1)

    def set_full_screen(self):
        """Set the window in full screen."""
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (self.screen_width, self.screen_height))

    def load_map(self, path):
        """Load the map.

        :param path: Path to the map.

        """
        im = Image.open(path)
        im = im.resize((self.screen_width, self.screen_height), Image.ANTIALIAS)
        # Convert the Image object into a TkPhoto object
        self.tkimage = ImageTk.PhotoImage(im)
        self.canvas.create_image(self.screen_width/2, self.screen_height/2, image=self.tkimage)

    def mainloop(self):
        """Start the graphic mainloop."""
        self.root.mainloop()

    def after(self, secs, function):
        """Call the function every secs.

        :param secs: Time interval in seconds.
        :param function: The function to call.

        """
        self.root.after(secs, function)

    def draw_crosshair(self, x, y):
        crosshair = Crosshair(self, x, y)
        crosshair.draw()
        return crosshair

    def get_robot_drawing(self, rad=10, outline_color="red", fill_color="green"):
        return RobotDrawing(self, rad, outline_color, fill_color)

    def draw_circle(self, x, y, rad, outline_color="red", width=2, fill_color=None):
        circle = self.canvas.create_oval(x-rad, y-rad,
                                         x+rad, y+rad,
                                         outline=outline_color, width=width,
                                         fill=fill_color)
        self.root.after(100, self.root.quit)
        self.root.mainloop()
        return circle

    def draw_line(self, x_origin, y_origin,
                        x_end, y_end,
                        fill_color="red", width=2):
        line = self.canvas.create_line(x_origin, y_origin,
                                       x_end, y_end,
                                       width=width, fill=fill_color)
        self.root.after(100, self.root.quit)
        self.root.mainloop()
        return line

    def coords(self, object_id, *coords):
        """Change and return the coordinates of the object.

        :param object_id: Id of the object.
        :param \*coords: (optional) List of coordinate pairs.

        **Note:** Same effect as the `Tkinter's method <http://goo.gl/1PMqtC>`_.

        """
        return self.canvas.coords(object_id, *coords)

    def delete(self, object_id):
        """Delete the object with the id object_id.

        :param object_id: Id's object.

        """
        self.canvas.delete(object_id)

    def qui(self):
        self.root.quit()

class Crosshair(object):
    """Create a Crosshair object.

    :param gui: GUI object.
    :param x: x location of the Crosshair.
    :param y: y location of the Crosshair.
    :param rad: (optional) Crosshair's radius.
    :param color: (optional) Crosshair's color.
    :param width: (optional) Width's lines.

    """
    def __init__(self, gui, x, y, rad=30, color="red", width=2):
        self.gui = gui
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        self.width = width

        self.circle = None
        self.horizontal_line = None
        self.vertical_line = None

    def draw(self):
        """Draw the Crosshair on the screen."""
        # Before drawing, we make sure that the crosshair
        # is not drawn somewhere else
        if self.circle is not None:
            self.delete
        self._draw_circle()
        self._draw_cross()

    def _draw_circle(self):
        """Draw an circle."""
        self.circle = self.gui.draw_circle(self.x, self.y, self.rad,
                                           outline_color=self.color, width=self.width)

    def _draw_cross(self):
        """Draw a cross."""
        self.horizontal_line = self.gui.draw_line(self.x-self.rad, self.y,
                                                  self.x+self.rad, self.y,
                                                  width=2, fill_color=self.color)
        self.vertical_line = self.gui.draw_line(self.x, self.y-self.rad,
                                                self.x, self.y+self.rad,
                                                width=2, fill_color=self.color)

    def delete(self):
        """Delete the crosshair on the canvas."""
        self.gui.delete(self.circle)
        self.gui.delete(self.horizontal_line)
        self.gui.delete(self.vertical_line)

class RobotDrawing(object):
    """Create a RobotDrawing object, represented by 3 dots on the screen.

    :param gui: GUI object.
    :param rad: (optional) Radius of the dots.
    :param outline_color: (optional) Outline color of the dots.
    :param fill_color: (optional) Fill color of the dots.

    """
    def __init__(self, gui, rad=10, outline_color="red", fill_color="green"):
        self.gui = gui
        self.rad = rad
        self.outline_color = outline_color
        self.fill_color = fill_color

        # Represent the leds drawing on the canvas:
        self._circle1 = None
        self._circle2 = None
        self._circle3 = None

    def draw(self, leds):
        """Draw three dots on the screen."""
        # Front led
        x1 = leds['front']['X']
        y1 = leds['front']['Y']

        # Left led
        x2 = leds['left']['X']
        y2 = leds['left']['Y']

        # Right led
        x3 = leds['right']['X']
        y3 = leds['right']['Y']

        # If circles are not already drawn
        if not self._circle1:
            self._circle1 = self.gui.draw_circle(x1, y1, self.rad,
                                                 outline_color=self.outline_color,
                                                 fill_color=self.fill_color, width=2)
            self._circle2 = self.gui.draw_circle(x2, y2, self.rad,
                                                 outline_color=self.outline_color,
                                                 fill_color=self.fill_color, width=2)
            self._circle3 = self.gui.draw_circle(x3, y3, self.rad,
                                                 outline_color=self.outline_color,
                                                 fill_color=self.fill_color, width=2)
        else:
            self.gui.coords(self._circle1, x1-self.rad, y1-self.rad, x1+self.rad, y1+self.rad)
            self.gui.coords(self._circle2, x2-self.rad, y2-self.rad, x2+self.rad, y2+self.rad)
            self.gui.coords(self._circle3, x3-self.rad, y3-self.rad, x3+self.rad, y3+self.rad)

    def delete(self):
        self.gui.delete(self._circle1)
        self.gui.delete(self._circle2)
        self.gui.delete(self._circle3)
