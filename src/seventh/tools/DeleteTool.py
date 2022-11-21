import tkinter as tk
from typing import Dict, Callable

from src.seventh.tools.AbstractTool import AbstractTool


class DeleteTool(AbstractTool):

    def __init__(self, *args, main_window: 'MainWindow' = None, **kwargs) -> None:
        super().__init__(*args, main_window=main_window, **kwargs)

    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        return None

    def fist_click_in_canvas(self, main_window, event: tk.Event, *args, **kwargs) -> Dict['Buttons', Callable]:
        cords = event.x, event.y
        ids = main_window.canvas.find_overlapping(*cords, *cords)

        if len(ids) >= 1:
            main_window.canvas.delete(ids[0])
        return {}

