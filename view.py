import tkinter as tk
import math
from main import Game_Window


class AppView(tk.Canvas):

    def __init__(self, master):
        self.master = master
        tk.Canvas.__init__(self, master, width=1280, height=384)

    def create_graph(self):
        width = int(Game_Window.split("x")[0])-40
        height = int(Game_Window.split("x")[1])-40
        dw = width/127
        dh = height/5

        # Horizontal and Vertical axes
        self.create_line(20, 20+height, 20+width+1, 20+height,
                         fill="black", tag="graph", width=2)
        self.create_line(20, 20+height, 20, 19,
                         fill="black", tag="graph", width=2)

        for x in range(128):
            self.create_line(20+dw*x, 20+height, 20+dw*x, 20+height+5,
                             fill="black", tag="graph", width=2)
        for y in range(6):
            self.create_line(20, 20+height-dh*y, 20-5, 20+height-dh*y,
                             fill="black", tag="graph", width=2)
