import tkinter as tk
import math
import random
from tkinter.font import Font
from PIL import Image, ImageTk


class AppView(tk.Canvas):

    def __init__(self, master, perlin_noise, width, height):
        self._master = master
        self._perlin_noise = perlin_noise
        self._seed = perlin_noise.generate_seed()
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

    def create_seed_graph(self):
        num_octaves = self._perlin_noise.get_octave_count()
        seed_length = int(self._perlin_noise.get_seed_length())
        props_fill = "sky blue"
        seed_fill = "tan2"
        text_font = Font(family="Consolas", size=18)

        # Spacing from right and left
        right_space = 40
        left_space = 80

        # Spacing from top and bottom and divide
        top_space = 40
        bottom_space = 80
        divide_space = 80

        # Length of lower vert
        length_lower_vert = (
            self._height-(top_space+bottom_space+divide_space))/4
        # Length of upper vert
        length_upper_vert = 3 * \
            ((self._height-(top_space+bottom_space+divide_space))/4)
        # Length of horizontal width
        length_horiz = self._width-(left_space+right_space)

        # Start and end of width pos
        start_width = self._width-(length_horiz+right_space)
        end_width = self._width-right_space

        # Start and end of upper pos
        start_upper_vert = self._height - \
            (bottom_space+length_lower_vert+divide_space+length_upper_vert)
        end_upper_vert = self._height - \
            (bottom_space+length_lower_vert+divide_space)

        # Start and end of lower pos
        start_lower_vert = self._height-(bottom_space+length_lower_vert)
        end_lower_vert = self._height-bottom_space

        # Spacing between horizontal markers
        dw = length_horiz/(seed_length-1)
        # Spacing between vertical markers
        dh_lower = length_lower_vert/5
        dh_upper = length_upper_vert/5

        # Horizontal and Vertical axes for lower
        self.create_line(left_space, end_lower_vert, end_width+1, end_lower_vert,
                         fill=props_fill, tag="seed_graph", width=2)
        self.create_line(left_space, start_lower_vert-1, left_space, end_lower_vert,
                         fill=props_fill, tag="seed_graph", width=2)

        # Horizontal and Vertical markers for lower
        for x in range(seed_length):
            self.create_line(left_space+dw*x, end_lower_vert, left_space+dw*x, end_lower_vert+5,
                             fill=props_fill, tag="seed_graph", width=2)
            # Draw seed to screen
            if x != seed_length-1:
                self.create_line(
                    left_space+dw*x, end_lower_vert-self._seed[x]*length_lower_vert, left_space+dw*(x+1), end_lower_vert-self._seed[x+1]*length_lower_vert, tag="seed_graph", fill=seed_fill, width=1.5)
        for y in range(6):
            self.create_line(left_space, end_lower_vert-dh_lower*y, left_space-5, end_lower_vert-dh_lower*y,
                             fill=props_fill, tag="seed_graph", width=2)

        # Horizontal and Vertical markers for upper
        for x in range(seed_length):
            self.create_line(left_space+dw*x, end_upper_vert, left_space+dw*x, end_upper_vert+5,
                             fill=props_fill, tag="seed_graph", width=2)
        for y in range(6):
            self.create_line(left_space, end_upper_vert-dh_upper*y, left_space-5, end_upper_vert-dh_upper*y,
                             fill=props_fill, tag="seed_graph", width=2)

        # Draw upper images
        for i in range(len(self._images)):
            self.create_image(left_space/2, end_upper_vert -
                              (dh_upper*i) - dh_upper/2, image=self._images[i], tag="seed_graph")

        # Horizontal and Vertical axes for upper
        self.create_line(left_space, end_upper_vert, end_width+1, end_upper_vert,
                         fill=props_fill, tag="seed_graph", width=2)
        self.create_line(left_space, start_upper_vert-1, left_space, end_upper_vert,
                         fill=props_fill, tag="seed_graph", width=2)

        # Text to screen

        self.create_text(self._width/2, end_upper_vert+top_space,
                         text="Generated Seed", font=text_font, fill=seed_fill, tag="seed_graph")

        self.create_text(self._width/2, top_space, text="Generated Terrain",
                         font=text_font, fill=seed_fill, tag="seed_graph")

        # Draw terrain to screen
        octave_count = 0
        multiplier_sum = 0
        for i in range(num_octaves):
            multiplier_sum += 1/(2**i)
        old_output = []

        while octave_count != num_octaves:
            # fill = "#" + "%06x" % random.randint(0, 0xFFFFFF)
            fill = seed_fill
            generator = seed_length / (2**octave_count)
            plots = []
            new_output = []
            for i in range(seed_length):
                if i % generator == 0:
                    value = (1/(2**octave_count) *
                             self._seed[i]) / multiplier_sum
                    plots.append(value)
                elif octave_count == 0:
                    value = (1/(2**octave_count) *
                             self._seed[0]) / multiplier_sum
                    plots.append(value)
            # wrap around
            plots.append(plots[0])

            if octave_count == 0:
                new_output = [plots[0]/multiplier_sum] * seed_length
            else:
                num_points = len(plots)
                num_to_skip = (seed_length/(num_points-1))-1
                point_count = 1
                skip_count = 0
                while point_count < num_points:
                    while skip_count <= num_to_skip:
                        if skip_count == 0:
                            start_point = plots.pop(0)
                            new_value = (
                                start_point + old_output.pop(0))
                            new_output.append(new_value)
                        else:
                            if point_count == num_points-1:
                                dv = (plots[0]-start_point)/(generator-1)
                            else:
                                dv = (plots[0]-start_point)/generator
                            new_value = (start_point + dv *
                                         skip_count + old_output.pop(0))
                            new_output.append(new_value)
                        skip_count += 1
                    skip_count = 0
                    point_count += 1

            dx = length_horiz/(len(new_output)-1)

            for x in range(len(new_output)):
                if x != len(new_output)-1:
                    self.create_line(left_space+dx*x, end_upper_vert-new_output[x]*length_upper_vert, left_space+dx*(
                        x+1), end_upper_vert-new_output[x+1]*length_upper_vert, tag="seed_graph", width=1.5, fill=fill)

            octave_count += 1
            old_output = new_output

    def refresh_view(self, event):
        if event.keysym == "space":
            self._change_state(True)
        elif event.keysym == "Right":
            self._perlin_noise.change_octave_count(1)
            self._change_state(False)
        elif event.keysym == "Left":
            self._perlin_noise.change_octave_count(-1)
            self._change_state(False)
        elif event.keysym == "Up":
            self._perlin_noise.change_seed_length(1)
            self._change_state(True)
        elif event.keysym == "Down":
            self._perlin_noise.change_seed_length(-1)
            self._change_state(True)

    def _change_state(self, reset):
        self.delete("seed_graph")
        if reset:
            self._seed = self._perlin_noise.generate_seed()
        self.create_seed_graph()
