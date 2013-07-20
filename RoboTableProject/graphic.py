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

    def init_graphic(self):
        """Initialize the graphical part using Tkinter."""
        self.root = Tkinter.Tk()
        self.screen_width, self.screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.set_full_screen()
        self.canvas = Tkinter.Canvas(self.root)

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
