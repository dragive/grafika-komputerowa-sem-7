import tkinter as tk
from abc import abstractmethod
from typing import Callable, Dict


class AbstractTool:
    def __init__(self):
        self.object: tk.Widget
        self.cords: tuple[int, int]

    @abstractmethod
    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        pass

    def fist_click_in_canvas(self, *args, **kwargs) -> Dict['Buttons', Callable]:
        from src.first.utils import Buttons
        print("first_click" + str(type(self)))
        return {
            # Buttons.LEFT_BUTTON_MOTION: self.after_first_click_motion,
            Buttons.LEFT_BUTTON: self.second_click_in_canvas,
        }

    def after_first_click_motion(self, *args, **kwargs) -> Dict['Buttons', Callable]:
        from src.first.utils import Buttons
        # event: tk.Event = args[0]
        # cords = event.x, event.y
        # print('motion '+str(cords))
        print("after_first_click_motion")
        return {
            # Buttons.LEFT_BUTTON: self.second_click_in_canvas,
            Buttons.LEFT_BUTTON_MOTION:self.after_first_click_motion,
        }
    def none(self, *args,**kwargs):
        pass
        return {}
    def second_click_in_canvas(self, window: 'MainWindow', *args, **kwargs):
        from src.first.utils import Buttons
        event: tk.Event = args[0]
        cords = event.x, event.y
        print("second_click" + str(type(self)))
        return {
            Buttons.LEFT_BUTTON: self.fist_click_in_canvas,
            Buttons.LEFT_BUTTON_MOTION: None,
        }
