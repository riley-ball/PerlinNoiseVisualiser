import tkinter as tk
import math
import view
import random


class PerlinNoise(object):
    """Object that represents properties of the perlin noise to be drawn"""

    def __init__(self, master):

        self._master = master
        self._scaling_factor = 2
        self._seed_length = 256
        self._octave_count = 8
        self._seed = [random.random() for i in range(int(self._seed_length))]
        self._generations = []
        self.generate_octaves()

    def generate_seed(self):
        '''
        Function that generates a new seed
        '''
        self._seed = [random.random() for i in range(int(self._seed_length))]

    def get_seed(self):
        '''
        Getter function that returns seed length
        '''
        return self._seed

    def change_octave_count(self, change):
        '''
        Function that changes octave count
        '''
        if change == 1:
            if 2**self._octave_count < self._seed_length:
                self._octave_count += 1
        else:
            if self._octave_count > 1:
                self._octave_count -= 1

    def change_scaling_factor(self, change):
        '''
        Function that changes scaling factor
        '''
        if change == 1:
            if self._scaling_factor + 0.1 <= 3.5:
                self._scaling_factor += 0.1
        else:
            if self._scaling_factor - 0.1 >= 0.5:
                self._scaling_factor -= 0.1

    def change_seed_length(self, change):
        '''
        Function that changes seed length
        '''
        if change == 1:
            self._seed_length *= 2
            self.generate_seed()
        else:
            if self._seed_length/2 > 1:
                self._seed_length /= 2
                self.generate_seed()

    def get_octave_count(self):
        '''
        Getter function that returns octave count
        '''
        return int(self._octave_count)

    def get_seed_length(self):
        '''
        Getter function that returns seed length
        '''
        return int(self._seed_length)

    def get_scaling_factor(self):
        '''
        Getter function that returns seed length
        '''
        return self._scaling_factor

    def generate_octaves(self):
        '''
        Function that generates all octaves
        '''
        self._generations = []
        total_octaves = int(math.log10(self.get_seed_length())/math.log10(2))
        scale_acc = 0
        scale = 1
        for i in range(total_octaves):
            scale_acc += 1/(self.get_scaling_factor()**i)

        # Create octaves
        for octave in range(total_octaves):
            current_gen = []
            pitch = int(self.get_seed_length() / 2**(octave))
            for x in range(self.get_seed_length()):
                sample1 = int(int((x / pitch)) * pitch)
                sample2 = int(int((sample1 + pitch)) % self.get_seed_length())

                pos = (x-sample1) / pitch
                sample = (1-pos) * \
                    self._seed[sample1] + pos * self._seed[sample2]

                noise = sample * scale
                if octave != 0:
                    current_gen.append(self._generations[-1][x] + noise)
                else:
                    current_gen.append(noise)
            self._generations.append(current_gen)
            scale /= self._scaling_factor

        # Scale between 0 and 1
        self._generations = [[i/scale_acc for i in octave]
                             for octave in self._generations]

    def get_octaves(self):
        '''
        Getter function that returns generated octaves
        '''
        return self._generations


class App(object):
    '''
    Top-level GUI application for PerlinNoiseVisualiser app
    '''

    def __init__(self, master, width, height):
        '''
        Construct PerlinNoiseVisualiser app in root window

        Arguments:
            master {tk.Tk} -- Window to place the game into
        '''

        self._master = master
        self._canvas = tk.Canvas(self._master)
        self._canvas.pack()
        self._perlin_noise = PerlinNoise(self._master)
        self._view = view.AppView(
            self._canvas, width, height)
        self._view.pack()
        self._canvas.bind_all("<Key>", self._callback)
        self._setup()

    def _setup(self):
        '''Function that sets up the display for a Perlin Noise object
        '''
        self._view.refresh_view(self._perlin_noise)

    def _callback(self, event):
        if event.keysym == "space":
            self._perlin_noise.generate_seed()
            self._refresh_seed()
            self._perlin_noise.generate_octaves()
            self._refresh_terrain()
        elif event.keysym == "u":
            self._perlin_noise.change_octave_count(1)
            self._refresh_terrain()
        elif event.keysym == "j":
            self._perlin_noise.change_octave_count(-1)
            self._refresh_terrain()
        elif event.keysym == "i":
            self._perlin_noise.change_seed_length(1)
            self._refresh_seed()
            self._perlin_noise.change_octave_count(1)
            self._perlin_noise.generate_octaves()
            self._refresh_terrain()
        elif event.keysym == "k":
            self._perlin_noise.change_seed_length(-1)
            self._refresh_seed()
            self._perlin_noise.change_octave_count(-1)
            self._perlin_noise.generate_octaves()
            self._refresh_terrain()
        elif event.keysym == "o":
            self._perlin_noise.change_scaling_factor(1)
            self._perlin_noise.generate_octaves()
            self._refresh_terrain()
        elif event.keysym == "l":
            self._perlin_noise.change_scaling_factor(-1)
            self._perlin_noise.generate_octaves()
            self._refresh_terrain()

    def _refresh_terrain(self):
        self._view.draw_terrain(
            self._perlin_noise.get_seed_length(), self._perlin_noise.get_octaves(), self._perlin_noise.get_octave_count())

    def _refresh_seed(self):
        self._view.draw_seed(
            self._perlin_noise.get_seed_length(), self._perlin_noise.get_seed())


def main():
    root = tk.Tk()
    root.config(bg="#ffe6f9")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.state('zoomed')
    app = App(root, w, h)
    root.title("PerlinNoiseVisualiser")
    root.mainloop()


if __name__ == "__main__":
    main()
