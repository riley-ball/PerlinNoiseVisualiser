import tkinter as tk
import math
import view

Game_Window = "1280x384"


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
        self._view = view.AppView(self._canvas)
        self._view.pack()
        self._view.create_graph()


def main():
    root = tk.Tk()
    # root.geometry(Game_Window)
    app = App(root)
    root.title("PerlinNoiseVisualiser")
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.mainloop()


if __name__ == "__main__":
    main()
