import tkinter as tk

from src.first.tools.AbstractTool import AbstractTool


class RectangleTool(AbstractTool):

    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        return canvas.create_rectangle(x1, y1, x2, y2, *args, **kwargs)

    def __init__(self):
        super().__init__()
