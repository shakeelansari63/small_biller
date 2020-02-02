import tkinter as tk
from PIL import Image
import io

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        scrollbary = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbarx = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scroll_frame = tk.Frame(self.canvas, *args, **kwargs)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scroll_frame)

        self.canvas.configure(yscrollcommand = scrollbary.set, xscrollcommand = scrollbarx.set)

        scrollbary.pack(side = "right", fill = "y")
        scrollbarx.pack(side = "bottom", fill = "x")
        self.canvas.pack(side = "left", fill = "both", expand = "yes")

    def generate_pdf(self):
        self.canvas.postscript(file = "tmp.ps", colormode="color")
