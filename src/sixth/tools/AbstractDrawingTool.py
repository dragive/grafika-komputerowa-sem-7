import tkinter as tk
from abc import abstractmethod
from typing import Callable, Dict, List

from src.sixth.tools.AbstractTool import AbstractTool


class AbstractDrawingTool(AbstractTool):
    def __init__(self, *args, main_window=None, **kwargs):
        self._drawn_object: int | None = None
        self._initial_cords: tuple[int, int] | None = None
        super().__init__(*args, main_window=None, **kwargs)

    @abstractmethod
    def generate_object(self, canvas: tk.Canvas, x1, y1, *args, **kwargs):
        pass

    def fist_click_in_canvas(self, main_window: 'MainWindow', *args, **kwargs) -> Dict['Buttons', Callable]:

        if self._drawn_object is not None:
            main_window.canvas.delete(self._drawn_object)

        self._initial_cords = args[0].x, args[0].y
        old = self._drawn_object

        self._drawn_object = self.generate_object(main_window.canvas,
                                                  *self._initial_cords,
                                                  *self._initial_cords,
                                                  **kwargs)
        points: List = main_window.points

        if old is not None:
            points[points.index(old)] = self._drawn_object
        else:
            points.append(self._drawn_object)
        main_window.redraw_bezier()
        return super().fist_click_in_canvas(*args, **kwargs)

    def after_first_click_motion(self, main_window: 'MainWindow', *args, **kwargs) -> Dict['Buttons', Callable]:


        return super().after_first_click_motion(*args, **kwargs)

    def second_click_in_canvas(self, window: 'MainWindow', *args, **kwargs):
        self._drawn_object = None
        self._initial_cords = None
        return super().second_click_in_canvas(window, *args, **kwargs)
