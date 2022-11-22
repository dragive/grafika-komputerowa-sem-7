import tkinter as tk

import numpy as np

from src.seventh.tools.AbstractDrawingTool import AbstractDrawingTool

STEPS = 100


class OvalTool(AbstractDrawingTool):

    def __init__(self, *args, main_window=None, **kwargs):
        super().__init__(*args, main_window=main_window, **kwargs)

    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        super().generate_object(canvas, x1, y1, x2, y2, *args, **kwargs)
        # return canvas.create_oval(x1, y1, x2, y2, *args, **self.get_tags(), **kwargs)
        ry = np.divide(np.abs(np.subtract(y1, y2)),2)
        rx = np.divide(np.abs(np.subtract(x1, x2)),2)

        center = np.mean([x1, x2]), np.mean([y1, y2])
        return canvas.create_polygon(*[unpacked
                                       for i in np.arange(0, 2*np.pi, 2*np.pi / STEPS)
                                       for unpacked in (
                                           np.add(np.multiply(np.cos(i), rx), center[0]),
                                           np.add(np.multiply(np.sin(i), ry), center[1]),
                                       )],
                                     *args,
                                     **self.get_tags(),
                                     **kwargs)
