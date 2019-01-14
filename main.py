import tkinter as tk
import math
import view
import random

Game_Window = "1536x960"


class PerlinNoise(object):
    """Object that represents properties of the perlin noise to be drawn"""

    def __init__(self, master):
        self._master = master
        self.seed_length = 128
        self.seed = [round(random.random(), 2)
                     for i in range(self.seed_length)]


class App(object):
    """Top-level GUI application for PerlinNoiseVisualiser app"""

    def __init__(self, master):
        """Construct PerlinNoiseVisualiser app in root window

        Arguments:
            master {tk.Tk} -- Window to place the game into
        """

        self._master = master
        self._canvas = tk.Canvas(self._master)
        self._canvas.pack()
        self._perlin_noise = PerlinNoise(self._master)
        self._view = view.AppView(self._canvas, self._perlin_noise)
        self._view.pack()
        self._view.create_seed_graph()


def main():
    root = tk.Tk()
    # root.geometry(Game_Window)
    app = App(root)
    root.title("PerlinNoiseVisualiser")
    root.mainloop()


if __name__ == "__main__":
    main()
