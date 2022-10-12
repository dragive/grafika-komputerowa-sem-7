import tkinter as tk

from src.first.tools.AbstractDrawingTool import AbstractDrawingTool


class RectangleTool(AbstractDrawingTool):

    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        return canvas.create_rectangle(x1, y1, x2, y2, *args, **self.get_tags(), **kwargs)

    def __init__(self, *args, main_window=None, **kwargs):
        super().__init__(*args, main_window=main_window, **kwargs)


