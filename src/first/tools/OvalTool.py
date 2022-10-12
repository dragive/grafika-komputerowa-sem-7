import tkinter as tk

from src.first.tools.AbstractDrawingTool import AbstractDrawingTool


class OvalTool(AbstractDrawingTool):


    def __init__(self, *args, main_window=None, **kwargs):
        super().__init__(*args, main_window=main_window, **kwargs)

    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        return canvas.create_oval(x1, y1, x2, y2, *args, **self.get_tags(), **kwargs)
