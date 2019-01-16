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

        self.create_text(self._width/2, top_space/2, text="Generated Terrain",
                         font=text_font, fill=seed_fill, tag="seed_graph")

        # Draw terrain to screen
        total_octaves = int(math.log10(seed_length)/math.log10(2))
        scale_acc = 0
        for i in range(total_octaves):
            scale_acc += 1/(2**i)
        print(scale_acc)
        octave_generations = [0] * seed_length
        fill = seed_fill

        scale = 1
        for octave in range(total_octaves):
            pitch = int(seed_length / 2**(octave+1))
            for x in range(seed_length):
                sample1 = int(int((x / pitch)) * pitch)
                sample2 = int(int((sample1 + pitch)) % seed_length)

                pos = (x-sample1) / pitch
                sample = (1-pos) * \
                    self._seed[sample1] + pos * self._seed[sample2]

                noise = sample * scale
                octave_generations[x] += noise

            dx = length_horiz/(seed_length-1)
            draw_generation = [i/scale_acc for i in octave_generations]
            for x in range(seed_length):
                if x != seed_length-1:
                    self.create_line(left_space+dx*x, end_upper_vert-draw_generation[x]*length_upper_vert, left_space+dx*(
                        x+1), end_upper_vert-draw_generation[x+1]*length_upper_vert, tag="seed_graph", width=1.5, fill=fill)

            scale /= 2

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
