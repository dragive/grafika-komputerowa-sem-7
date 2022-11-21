import tkinter as tk

from src.seventh.tools.AbstractDrawingTool import AbstractDrawingTool


class RectangleTool(AbstractDrawingTool):

    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        super().generate_object(canvas, x1, y1, x2, y2, *args, **kwargs)
        return canvas.create_polygon(
            x1, y1,
            x1, y2,
            x2, y2,
            x2, y1,
            # x1, y1,
            *args, **kwargs)

    def __init__(self, *args, main_window=None, **kwargs):
        super().__init__(*args, main_window=main_window, **kwargs)
