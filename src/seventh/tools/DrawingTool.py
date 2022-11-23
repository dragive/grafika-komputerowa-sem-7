import tkinter as tk
from typing import Dict, Callable

from src.seventh.tools.AbstractDrawingTool import AbstractDrawingTool


class DrawingTool(AbstractDrawingTool):

    def __init__(self, *args, main_window=None, **kwargs):
        super().__init__(*args, main_window=main_window, **kwargs)
        self.drawn_points = list()
        self.main_window = main_window

    @property
    def get_initial_mapping(self):
        from src.seventh.utils import Buttons
        return {**super().get_initial_mapping, Buttons.RIGHT_BUTTON: self.submit_creating_polygon}

    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        super().generate_object(canvas, x1, y1, x2, y2, *args, **kwargs)
        return canvas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, fill="cyan")

    def submit_creating_polygon(self, *args, **kwargs):

        if len(self.drawn_points) > 0:
            coords = tuple(a for x in map(lambda x: self.get_mean_cords_of_point(self.main_window, x), self.drawn_points) for a in x)
            polygon = self.main_window.canvas.create_polygon(*coords,
                                     # *args,
                                     **self.get_tags(),
                                     **kwargs)
            print(polygon)
            pass

        self.clear_drawn_points()
        return {}

    def clear_drawn_points(self):
        for point in self.drawn_points:
            self.main_window.canvas.delete(point)
        self.drawn_points.clear()

    def get_first_click_bindings(self, args, kwargs):
        from src.seventh.utils import Buttons
        ret = {**super().get_first_click_bindings(args, kwargs), Buttons.RIGHT_BUTTON: self.submit_creating_polygon}
        return ret

    def after_first_click_motion(self, main_window: 'MainWindow', *args, **kwargs) -> Dict['Buttons', Callable]:
        return super().get_binding_after_first_click_motion(args, kwargs)

    def after_first_click_down_created_object(self):
        new_obj = self._drawn_object
        self.drawn_points.append(new_obj)
        super().after_first_click_down_created_object()
