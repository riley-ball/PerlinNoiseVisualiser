import tkinter as tk
import math
import view
import random


class PerlinNoise(object):
    """Object that represents properties of the perlin noise to be drawn"""

    def __init__(self, master):
        self._master = master
        self.seed_length = 512
        self.octave_count = 9

    def generate_seed(self):
        return [random.random() for i in range(int(self.seed_length))]

    def change_octave_count(self, change):
        if change == 1:
            if 2**self.octave_count < self.seed_length:
                self.octave_count += 1
        else:
            if self.octave_count > 1:
                self.octave_count -= 1

    def change_seed_length(self, change):
        if change == 1:
            self.seed_length *= 2
            self.generate_seed()
        else:
            if self.seed_length/2 > 1:
                self.seed_length /= 2
                self.generate_seed()

    def get_octave_count(self):
        return self.octave_count

    def get_seed_length(self):
        return self.seed_length


class App(object):
    """Top-level GUI application for PerlinNoiseVisualiser app"""

    def __init__(self, master, width, height):
        """Construct PerlinNoiseVisualiser app in root window

        Arguments:
            master {tk.Tk} -- Window to place the game into
        """

        self._master = master
        self._canvas = tk.Canvas(self._master)
        self._canvas.pack()
        self._perlin_noise = PerlinNoise(self._master)
        self._view = view.AppView(
            self._canvas, self._perlin_noise, width, height)
        self._view.pack()
        self._view.create_seed_graph()

        self._canvas.bind_all("<Key>", self._callback)

    def _callback(self, event):
        self._refresh_view(event)

    def _refresh_view(self, event):
        self._view.refresh_view(event)


def main():
    root = tk.Tk()
    root.config(bg="#ffe6f9")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    # root.state('zoomed')
    root.attributes("-fullscreen", True)
    app = App(root, w, h)
    root.title("PerlinNoiseVisualiser")
    root.mainloop()


if __name__ == "__main__":
    main()
