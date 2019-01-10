import tkinter as tk
import math
from main import Game_Window


class AppView(tk.Canvas):

    def __init__(self, master, perlin_noise):
        self._master = master
        self._perlin_noise = perlin_noise
        self._seed_length = perlin_noise.seed_length
        self._seed = perlin_noise.seed
        self.width = int(Game_Window.split("x")[0])
        self.height = int(Game_Window.split("x")[1])
        tk.Canvas.__init__(self, master, width=self.width, height=self.height)

    def create_seed_graph(self):
        width = int(Game_Window.split("x")[0])-40
        height = int(Game_Window.split("x")[1])-40
        dw = (width-40)/(self._seed_length-1)
        dh = (height-(576+40))/5
        vertical = (height-(576+40))
        horizontal = height-40

        # Horizontal and Vertical axes
        self.create_line(40, height, width+1, height,
                         fill="black", tag="seed_graph", width=2)
        self.create_line(40, height, 40, height-384+39,
                         fill="black", tag="seed_graph", width=2)

        # Horizontal and Vertical markers
        for x in range(self._seed_length):
            self.create_line(40+dw*x, height, 40+dw*x, height+5,
                             fill="black", tag="seed_graph", width=2)
            if x != self._seed_length-1:
                self.create_line(
                    40+dw*x, height-self._seed[x]*vertical, 40+dw*(x+1), height-self._seed[x+1]*vertical, tag="seed_graph", fill="red", width=1.3)
        for y in range(6):
            self.create_line(40, height-dh*y, 40-5, height-dh*y,
                             fill="black", tag="seed_graph", width=2)

        # Divider
        self.create_line(20, height-384+20, width+20, height-384+20,
                         fill="black", tag="seed_graph", width=2)

        # # Horizontal and Vertical axes
        # self.create_line(40, height, width+1, height,
        #                  fill="black", tag="seed_graph", width=2)
        # self.create_line(40, height, 40, height-384+39,
        #                  fill="black", tag="seed_graph", width=2)
