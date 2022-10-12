import tkinter as tk
from typing import Dict, Callable

from src.first.tools.AbstractDrawingTool import AbstractDrawingTool


class LineTool(AbstractDrawingTool):

    def __init__(self, *args, main_window=None, **kwargs):
        super().__init__(*args, main_window=main_window, **kwargs)

    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        super().generate_object(canvas, x1, y1, x2, y2, *args, **kwargs)
        return canvas.create_line(x1, y1, x2, y2, *args, **self.get_tags(), **kwargs)

