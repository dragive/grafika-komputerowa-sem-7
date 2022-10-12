import tkinter as tk
from typing import Dict, Callable

from src.first.tools.AbstractTool import AbstractTool


class PickTool(AbstractTool):

    def __init__(self, *args, main_window: 'MainWindow' = None, **kwargs) -> None:
        from src.first.utils import Buttons
        main_window.canvas.bind(tuple(AbstractTool.get_tags().values())[0],
                                main_window.return_handler(Buttons.OBJECT_CLICKED), add=True)

        super().__init__(*args, main_window=main_window, **kwargs)

    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        return None

    def fist_click_in_canvas(self, *args, **kwargs) -> Dict['Buttons', Callable]:
        d = super().fist_click_in_canvas(*args, **kwargs)

        from src.first.utils import Buttons

        d[Buttons.OBJECT_CLICKED] = self.selected_object
        return d

    def selected_object(self, *args, **kwargs):
        print(f"SELECTED: {args=} {kwargs=}")
        return {}

    def after_first_click_motion(self, *args, **kwargs) -> Dict['Buttons', Callable]:
        return super().after_first_click_motion(*args, **kwargs)

    def second_click_in_canvas(self, window: 'MainWindow', *args, **kwargs):
        d = super().second_click_in_canvas(window, *args, **kwargs)
        from src.first.utils import Buttons
        d[Buttons.OBJECT_CLICKED] = None
        return d
