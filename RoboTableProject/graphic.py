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

    def draw_crosshair(self, x, y):
        crosshair = Crosshair(self, x, y)
        crosshair.draw()
        return crosshair

    def create_oval(self, x, y, rad, outline_color="red", width=2):
        oval = self.canvas.create_oval(x-rad, y-rad,
                                       x+rad, y+rad,
                                       outline=outline_color, width=width)
        self.root.after(100, self.root.quit)
        self.root.mainloop()
        return oval

    def create_line(self, x_origin, y_origin,
                          x_end, y_end,
                          fill_color="red", width=2):
        line = self.canvas.create_line(x_origin, y_origin,
                                       x_end, y_end,
                                       width=width, fill=fill_color)
        self.root.after(100, self.root.quit)
        self.root.mainloop()
        return line

    def delete(self, object_id):
        self.canvas.delete(object_id)

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
        self._create_oval()
        self._create_cross()

    def _create_oval(self):
        """Draw an oval."""
        self.circle = self.gui.create_oval(self.x, self.y, self.rad,
                                           outline_color=self.color, width=self.width)

    def _create_cross(self):
        """Draw a cross."""
        self.horizontal_line = self.gui.create_line(self.x-self.rad, self.y,
                                                    self.x+self.rad, self.y,
                                                    width=2, fill_color=self.color)
        self.vertical_line = self.gui.create_line(self.x, self.y-self.rad,
                                                  self.x, self.y+self.rad,
                                                  width=2, fill_color=self.color)

    def delete(self):
        """Delete the crosshair on the canvas."""
        self.gui.delete(self.circle)
        self.gui.delete(self.horizontal_line)
        self.gui.delete(self.vertical_line)
