from RoboTableProject.tracking.sensorInterface import SensorInterface
from RoboTableProject.robot.robotInterface import RobotInterface
from Tkinter import *

root = Tk()

# label = Label(root, text=datetime.time(datetime.now()))
# label.grid(row=0, sticky=W)


# def update_label():
#     label.config(text=datetime.time(datetime.now()))
#     label.after(1000, update_label)

# label.after(1000, update_label)
robot = RobotInterface(SensorInterface())
i = 0

canvas = Canvas(root)
circle = canvas.create_oval(10, 50, 50, 80, outline="red", fill="green", width=2)
canvas.pack(fill=BOTH, expand=1)


def update_circle():
    rad = 10
    global i
    # x = i * 10
    # y = i * 10
    leds = robot.leds
    x1 = leds['front']['X']
    y1 = leds['front']['Y']

    x2 = leds['left']['X']
    y2 = leds['left']['Y']

    x3 = leds['right']['X']
    y3 = leds['right']['Y']

    canvas.coords(circle, x1-rad, y1-rad, x1+rad, y1+rad)
    canvas.coords(circle, x2-rad, y2-rad, x2+rad, y2+rad)
    canvas.coords(circle, x3-rad, y3-rad, x3+rad, y3+rad)
    # circle.itemconfigure(x0=i*10, y0=i*10)
    i += 1
    canvas.after(250, update_circle)

canvas.after(250, update_circle)
root.mainloop()
