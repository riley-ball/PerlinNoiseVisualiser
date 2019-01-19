import tkinter as tk
import math
import random
from tkinter.font import Font
from PIL import Image, ImageTk


class AppView(tk.Canvas):

    def __init__(self, master, width, height):
        self._master = master
        # Width of screen
        self._width = width
        # Height of screen
        self._height = height
        tk.Canvas.__init__(self, master, width=self._width,
                           height=self._height, bg="#ffe6f9")

        self._images = []
        self._images.append(ImageTk.PhotoImage(Image.open(
            "./images/water.png").resize((50, 50), Image.ANTIALIAS)))
        self._images.append(ImageTk.PhotoImage(Image.open(
            "./images/sand.png").resize((50, 50), Image.ANTIALIAS)))
        self._images.append(ImageTk.PhotoImage(Image.open(
            "./images/grass.png").resize((50, 50), Image.ANTIALIAS)))
        self._images.append(ImageTk.PhotoImage(Image.open(
            "./images/snow.png").resize((50, 50), Image.ANTIALIAS)))
        self._images.append(ImageTk.PhotoImage(Image.open(
            "./images/moon.png").resize((70, 70), Image.ANTIALIAS)))

        self._props_fill = "sky blue"
        self._seed_fill = "tan2"
        self._text_font = Font(family="Consolas", size=18)

        '''
        Variables for measurements for view
        '''

        # Spacing from right and left
        self._right_space = 40
        self._left_space = 80

        # Spacing from top and bottom and divide
        self._top_space = 40
        self._bottom_space = 80
        self._divide_space = 80

        # Length of lower vert
        self._length_lower_vert = (
            self._height-(self._top_space+self._bottom_space+self._divide_space))/4
        # Length of upper vert
        self._length_upper_vert = 3 * \
            ((self._height-(self._top_space+self._bottom_space+self._divide_space))/4)
        # Length of horizontal width
        self._length_horiz = self._width-(self._left_space+self._right_space)

        # Start and end of width pos
        self._start_width = self._width-(self._length_horiz+self._right_space)
        self._end_width = self._width-self._right_space

        # Start and end of upper pos
        self._start_upper_vert = self._height - \
            (self._bottom_space+self._length_lower_vert +
             self._divide_space+self._length_upper_vert)
        self._end_upper_vert = self._height - \
            (self._bottom_space+self._length_lower_vert+self._divide_space)

        # Start and end of lower pos
        self._start_lower_vert = self._height - \
            (self._bottom_space+self._length_lower_vert)
        self._end_lower_vert = self._height-self._bottom_space

        # Spacing between horizontal markers
        self._dw_markers = self._length_horiz/5
        # Spacing between vertical markers
        self._dh_lower = self._length_lower_vert/5
        self._dh_upper = self._length_upper_vert/5

    def draw_graph(self, perlin_noise):
        self.delete("graph")

        # Horizontal and Vertical axes for lower
        self.create_line(self._left_space, self._end_lower_vert, self._end_width+1, self._end_lower_vert,
                         fill=self._props_fill, tag="graph", width=2)
        self.create_line(self._left_space, self._start_lower_vert-1, self._left_space, self._end_lower_vert,
                         fill=self._props_fill, tag="graph", width=2)

        # Horizontal and Vertical markers for lower
        for x in range(6):
            self.create_line(self._left_space+self._dw_markers*x, self._end_lower_vert, self._left_space+self._dw_markers*x, self._end_lower_vert+5,
                             fill=self._props_fill, tag="graph", width=2)
        for y in range(6):
            self.create_line(self._left_space, self._end_lower_vert-self._dh_lower*y, self._left_space-5, self._end_lower_vert-self._dh_lower*y,
                             fill=self._props_fill, tag="graph", width=2)

        # Horizontal and Vertical markers for upper
        for x in range(6):
            self.create_line(self._left_space+self._dw_markers*x, self._end_upper_vert, self._left_space+self._dw_markers*x, self._end_upper_vert+5,
                             fill=self._props_fill, tag="graph", width=2)
        for y in range(6):
            self.create_line(self._left_space, self._end_upper_vert-self._dh_upper*y, self._left_space-5, self._end_upper_vert-self._dh_upper*y,
                             fill=self._props_fill, tag="graph", width=2)

        # Draw upper images
        for i in range(len(self._images)):
            self.create_image(self._left_space/2, self._end_upper_vert -
                              (self._dh_upper*i) - self._dh_upper/2, image=self._images[i], tag="graph")

        # Horizontal and Vertical axes for upper
        self.create_line(self._left_space, self._end_upper_vert, self._end_width+1, self._end_upper_vert,
                         fill=self._props_fill, tag="graph", width=2)
        self.create_line(self._left_space, self._start_upper_vert-1, self._left_space, self._end_upper_vert,
                         fill=self._props_fill, tag="graph", width=2)

        # Text to screen

        self.create_text(self._width/2, self._end_upper_vert+self._top_space,
                         text="Generated Seed", font=self._text_font, fill=self._seed_fill, tag="graph")

        self.create_text(self._width/2, self._top_space/2, text="Generated Terrain",
                         font=self._text_font, fill=self._seed_fill, tag="graph")

    def refresh_view(self, perlin_noise):
        seed_length = perlin_noise.get_seed_length()
        seed = perlin_noise.get_seed()
        generations = perlin_noise.get_octaves()
        num_octaves = perlin_noise.get_octave_count()

        self.draw_graph(perlin_noise)
        self.draw_seed(seed_length, seed)
        self.draw_terrain(seed_length, generations, num_octaves)

    def draw_seed(self, seed_length, seed):
        self._dw_seed = self._length_horiz/(seed_length-1)
        self.delete("seed")

        # Draw seed to screen
        for x in range(seed_length):
            if x != seed_length-1:
                self.create_line(
                    self._left_space+self._dw_seed*x, self._end_lower_vert -
                    seed[x]*self._length_lower_vert,
                    self._left_space+self._dw_seed*(x+1), self._end_lower_vert -
                    seed[x+1]*self._length_lower_vert,
                    tag="seed", fill=self._seed_fill, width=1.5)

    def draw_terrain(self, seed_length, generations, num_octaves):
        dx = self._length_horiz/(seed_length-1)
        self.delete("terrain")

        # Draw terrain to screen
        for octave in range(num_octaves):
            for x in range(seed_length):
                if x != seed_length-1:
                    self.create_line(self._left_space+dx*x, self._end_upper_vert-generations[octave][x]*self._length_upper_vert, self._left_space+dx*(
                        x+1), self._end_upper_vert-generations[octave][x+1]*self._length_upper_vert, tag="terrain", width=1.5, fill=self._seed_fill)
