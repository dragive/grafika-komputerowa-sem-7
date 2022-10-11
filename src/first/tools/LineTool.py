import tkinter as tk

from src.first.tools.AbstractTool import AbstractTool


class LineTool(AbstractTool):

    def __init__(self):
        super().__init__()

    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        return canvas.create_line(x1, y1, x2, y2, *args, **kwargs)

