import tkinter as tk
from abc import abstractmethod
from typing import Callable, Dict


class AbstractTool:

    def __init__(self, *args, main_window=None, **kwargs) -> None:
        super().__init__()

    @abstractmethod
    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        pass

    def fist_click_in_canvas(self, *args, **kwargs) -> Dict['Buttons', Callable]:
        from src.sixth.utils import Buttons
        return {
            Buttons.LEFT_BUTTON_MOTION: self.after_first_click_motion,
            Buttons.LEFT_BUTTON_RELEASE: self.second_click_in_canvas,
        }

    def after_first_click_motion(self, *args, **kwargs) -> Dict['Buttons', Callable]:
        return {
        }

    def second_click_in_canvas(self, window: 'MainWindow', *args, **kwargs):
        from src.sixth.utils import Buttons

        return {
            Buttons.LEFT_BUTTON: self.fist_click_in_canvas,
            Buttons.LEFT_BUTTON_MOTION: self.after_first_click_motion,
            Buttons.LEFT_BUTTON_RELEASE: None,
        }

    def _get_clicked_object(self):
        pass

    @staticmethod
    def get_tags():
        return {"tags": "selectable"}

    @property
    def get_initial_mapping(self):
        from src.sixth.utils import Buttons
        return {
            Buttons.LEFT_BUTTON: self.fist_click_in_canvas,
        }
