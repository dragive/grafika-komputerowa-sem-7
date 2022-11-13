import tkinter as tk

from src.sixth.tools.AbstractDrawingTool import AbstractDrawingTool


class RectangleTool(AbstractDrawingTool):

    def generate_object(self, canvas: tk.Canvas, x1, y1, *args, **kwargs):
        super().generate_object(canvas, x1, y1, *args, **kwargs)

        return canvas.create_oval(x1, y1, x1 + 10, y1 + 10, fill='#000000', **kwargs)

    def __init__(self, *args, main_window=None, **kwargs):
        super().__init__(*args, main_window=main_window, **kwargs)
