from tracking.sensorInterface import SensorInterface
from robot.robotInterface import RobotInterface
from Tkinter import *

root = Tk()

# make it cover the entire screen
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (width, height))

# label = Label(root, text=datetime.time(datetime.now()))
# label.grid(row=0, sticky=W)


# def update_label():
#     label.config(text=datetime.time(datetime.now()))
#     label.after(1000, update_label)

# label.after(1000, update_label)
robot = RobotInterface(SensorInterface())
i = 0

canvas = Canvas(root)
circle1 = canvas.create_oval(10, 50, 50, 80, outline="red", fill="green", width=2)
circle2 = canvas.create_oval(10, 50, 50, 80, outline="red", fill="green", width=2)
circle3 = canvas.create_oval(10, 50, 50, 80, outline="red", fill="green", width=2)
canvas.pack(fill=BOTH, expand=1)


def update_circle():
    rad = 10
    global i
    # x = i * 10
    # y = i * 10
    leds = robot.leds
    print leds
    distanceFront = (leds['right']['Y'] - leds['front']['Y'])
    distanceLeft = leds['right']['Y'] - leds['left']['Y']
    print distanceFront
    x1 = leds['front']['X']
    # y1 = leds['front']['Y'] + distanceFront * 2
    y1 = width - leds['front']['Y']

    x2 = leds['left']['X']
    # y2 = leds['left']['Y'] + distanceLeft * 2
    y2 = width - leds['left']['Y']

    x3 = leds['right']['X']
    y3 = width - leds['right']['Y']

    canvas.coords(circle1, x1-rad, y1-rad, x1+rad, y1+rad)
    canvas.coords(circle2, x2-rad, y2-rad, x2+rad, y2+rad)
    canvas.coords(circle3, x3-rad, y3-rad, x3+rad, y3+rad)


    # circle.itemconfigure(x0=i*10, y0=i*10)
    i += 1
    canvas.after(50, update_circle)

canvas.after(50, update_circle)
root.mainloop()
