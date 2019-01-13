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
        lower_height = int(Game_Window.split("x")[1])-40
        dw = (width-40)/(self._seed_length-1)
        dh = (lower_height-(576+40))/5
        # Lowest point of lower axes
        lower_vert = (lower_height-(576+40))

        # Horizontal and Vertical axes
        self.create_line(40, lower_height, width+1, lower_height,
                         fill="black", tag="seed_graph", width=2)
        self.create_line(40, lower_height, 40, lower_height-384+39,
                         fill="black", tag="seed_graph", width=2)

        # Horizontal and Vertical markers
        for x in range(self._seed_length):
            self.create_line(40+dw*x, lower_height, 40+dw*x, lower_height+5,
                             fill="black", tag="seed_graph", width=2)
            if x != self._seed_length-1:
                self.create_line(
                    40+dw*x, lower_height-self._seed[x]*lower_vert, 40+dw*(x+1), lower_height-self._seed[x+1]*lower_vert, tag="seed_graph", fill="red", width=1.3)
        for y in range(6):
            self.create_line(40, lower_height-dh*y, 40-5, lower_height-dh*y,
                             fill="black", tag="seed_graph", width=2)

        # Divider
        self.create_line(20, lower_height-384, width+20, lower_height-384,
                         fill="black", tag="seed_graph", width=2)

        # Lowest point of upper axes
        upper_height = lower_height-384-40
        upper_vert = upper_height-40
        upper_horiz = width+1-40

        # Horizontal and Vertical axes
        self.create_line(40, upper_height, width+1, upper_height,
                         fill="black", tag="seed_graph", width=2)
        self.create_line(40, upper_height, 40, 40,
                         fill="black", tag="seed_graph", width=2)

        self.create_text(int(Game_Window.split(
            "x")[0])/2, upper_height+60, text="Generated Seed", font=("Purisa", 25))

        octave_count = 0
        num_octaves = 5
        multiplier_sum = 0
        for i in range(num_octaves):
            multiplier_sum += 1/(2**i)
        print(multiplier_sum)
        old_output = []

        while octave_count != num_octaves:
            generator = self._seed_length / (2**octave_count)
            plots = []
            new_output = []
            for i in range(self._seed_length):
                if i % generator == 0:
                    value = 1/(2**octave_count) * self._seed[i]
                    plots.append(value)
                elif octave_count == 0:
                    value = 1/(2**octave_count) * self._seed[0]
                    plots.append(value)
            # wrap around
            plots.append(plots[0])

            if octave_count == 0:
                new_output = [plots[0]/multiplier_sum] * self._seed_length
            else:
                num_points = len(plots)
                num_to_skip = (self._seed_length/(num_points-1))-1
                point_count = 1
                skip_count = 0
                while point_count < num_points:
                    while skip_count <= num_to_skip:
                        if skip_count == 0:
                            start_point = plots.pop(0)
                            new_value = (
                                start_point + old_output.pop(0)) / multiplier_sum
                            new_output.append(new_value)
                        else:
                            if point_count == num_points-1:
                                dv = (plots[0]-start_point)/(generator-1)
                            else:
                                dv = (plots[0]-start_point)/generator
                            new_value = (start_point + dv *
                                         skip_count + old_output.pop(0)) / multiplier_sum
                            new_output.append(new_value)
                        skip_count += 1
                    skip_count = 0
                    point_count += 1

            if octave_count == 0:
                dx = upper_horiz
            else:
                dx = upper_horiz/(len(new_output)-1)
            for x in range(len(new_output)):
                if x != len(new_output)-1:
                    self.create_line(40+dx*x, upper_height-new_output[x]*upper_vert, 40+dx*(
                        x+1), upper_height-new_output[x+1]*upper_vert, tag="seed_graph", fill="blue", width=1.3)

            octave_count += 1
            old_output = new_output
