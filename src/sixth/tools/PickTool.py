import tkinter as tk
from typing import Dict, Callable, Any

from src.sixth.tools.AbstractTool import AbstractTool


class PickTool(AbstractTool):

    def __init__(self, *args, main_window: 'MainWindow' = None, **kwargs) -> None:
        self._moved_object: int | None = None
        self._first_click_cords: tuple[int] | list[int] | None = None
        super().__init__(*args, main_window=main_window, **kwargs)

    @property
    def get_initial_mapping(self):
        from src.sixth.utils import Buttons
        return {
            Buttons.LEFT_BUTTON: self.fist_click_in_canvas,
            Buttons.RIGHT_BUTTON_DOUBLE: self.double_click_in_canvas,
        }

    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        return None

    def fist_click_in_canvas(self, main_window, event: tk.Event, *args, **kwargs) -> Dict['Buttons', Callable]:
        cords = event.x, event.y
        ids = main_window.canvas.find_overlapping(*cords, *cords)

        if len(ids) >= 1:
            self._moved_object = ids[0]
            self._first_click_cords = cords
            # print(self._moved_object)

        d = super().fist_click_in_canvas(*args, **kwargs)
        # from src.s.utils import Buttons
        # d.update({
        #     Buttons.LEFT_BUTTON_DOUBLE:
        # })
        return d

    def after_first_click_motion(self, main_window, event: tk.Event, *args, **kwargs) -> Dict['Buttons', Callable]:
        if self._moved_object is not None:
            cords = event.x, event.y
            delta = -self._first_click_cords[0] + cords[0], -self._first_click_cords[1] + cords[1]
            self._first_click_cords = cords
            main_window.canvas.move(self._moved_object, *delta)
        return super().after_first_click_motion(*args, **kwargs)

    def double_click_in_canvas(self, main_window: 'MainWindow', event: tk.Event, *args, **kwargs):
        cords = event.x, event.y
        ids = main_window.canvas.find_overlapping(*cords, *cords)
        if len(ids) > 0:
            i = ids[0]
            from tkinter.simpledialog import askstring
            name = askstring('Name', 'What is your name?',
                             initialvalue=str([int(c) for c in main_window.canvas.coords(i)])[1:-1])
            name = name.split(',')

            try:
                assert len(name) == 4
                name = [int(x) for x in name]
                main_window.canvas.coords(i, *name)
            except Exception:
                from tkinter import messagebox
                messagebox.showerror("Param error reading", "Incorrect param format!")
        return {}

    def second_click_in_canvas(self, window: 'MainWindow', *args, **kwargs):
        self._moved_object: int | None = None
        self._first_click_cords: tuple[int] | list[int] | None = None
        d = super().second_click_in_canvas(window, *args, **kwargs)
        from src.sixth.utils import Buttons
        d.update({
            Buttons.RIGHT_BUTTON: None,
        })

        return d
