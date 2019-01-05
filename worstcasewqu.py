""" This code draws the tree of given height with the least amount of
    unions achievable through the weighted quick-union algorithm. """

from tkinter import *

def func(x, y, n):
    cc = n * 255 / num
    color = "#%02x%02x%02x" % (cc, cc, cc)
    if n == 1:
        draw_node(x, y)
        draw_line(x, y, x, y + 1, color)
        draw_node(x, y + 1)
        return

    func(x, y, n - 1)
    draw_line(x, y, x + thats[n], y + 1, color)
    func(x + thats[n], y + 1, n - 1)

def draw_node(x, y):
    pass
    # radius = 1
    # global color
    # canv.create_oval(x * xpad - radius, y * unit - radius, x * xpad + radius, y * unit + radius, width=0, fill=color)


def draw_line(x1, y1, x2, y2, color="#fff", thickness=1):
    canv.create_line(x1 * xpad, y1 * ypad, x2 * xpad, y2 * ypad, fill=color, width=thickness)


hot = [0, 0, 0, 0, 0, 1, 3, 8, 18, 40, 84, 175, 357, 727, 1467, 2958, 5940]
thats = []
for i in range(0, len(hot)):
    that = 2 ** (i-2) - hot[i]
    thats.append(that)

ypad = 25
xpad = 0.1

ww, hh, = 1200, 500
tk = Tk()
canv = Canvas(tk, width=ww, height=hh)
canv.grid()
canv.create_rectangle(0, 0, ww, hh, fill="#feeaec")

color = "blue"
num = 16
func(0, 1, num)
mainloop()

# ahmad asaad, ibrahim tigrek 2018
