import tkinter as tk
from typing import Dict, Callable

from src.seventh.tools.AbstractTool import AbstractTool


class PickTool(AbstractTool):

    def __init__(self, *args, main_window: 'MainWindow' = None, **kwargs) -> None:
        self._moved_object: int | None = None
        self._first_click_cords: tuple[int] | list[int] | None = None
        super().__init__(*args, main_window=main_window, **kwargs)

    @property
    def get_initial_mapping(self):
        from src.seventh.utils import Buttons
        return {
            Buttons.LEFT_BUTTON: self.fist_click_in_canvas,
            Buttons.RIGHT_BUTTON_DOUBLE: self.double_click_in_canvas,
        }

    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        return None

    def fist_click_in_canvas(self, main_window, event: tk.Event, *args, **kwargs) -> Dict['Buttons', Callable]:
        d = super().fist_click_in_canvas(*args, **kwargs)

        cords = event.x, event.y
        ids = main_window.canvas.find_overlapping(*cords, *cords)


        intersection_with_box_points = main_window.items_to_be_deleted_at_changing_tools.intersection(ids)
        if intersection_with_box_points:
            return d

        identifier = None
        self.reset(main_window)

        if len(ids) >= 1:
            identifier = ids[0]

        if identifier:
            self._moved_object = identifier
            self._first_click_cords = cords
            self.check_item(identifier, main_window)
            self.generate_box_points(identifier, main_window)
        else:
            self.reset(main_window)
        return d

    def reset(self, main_window):
        self.uncheck_item(main_window)
        main_window.delete_items_to_be_deleted()

    def generate_box_points(self, identifier, main_window):
        raw_coords = main_window.canvas.coords(identifier)
        xs, ys = raw_coords[::2], raw_coords[1::2]

        min_x = min(xs)
        max_x = max(xs)

        min_y = min(ys)
        max_y = max(ys)

        for x in [min_x, max_x]:
            for y in [min_y, max_y]:
                main_window.items_to_be_deleted_at_changing_tools = main_window.canvas \
                    .create_oval(x - 5, y - 5,
                                 x + 5, y + 5,
                                 fill="blue")

    def check_item(self, ids, main_window):
        main_window.checked_item = ids
        main_window.canvas.itemconfig(ids, outline="red")

    def uncheck_item(self, main_window):
        if main_window.checked_item:
            main_window.canvas.itemconfig(main_window.checked_item, outline="black")
            main_window.checked_item = None

    def after_first_click_motion(self, main_window, event: tk.Event, *args, **kwargs) -> Dict['Buttons', Callable]:
        if self._moved_object is not None:
            cords = event.x, event.y
            delta = -self._first_click_cords[0] + cords[0], -self._first_click_cords[1] + cords[1]
            self._first_click_cords = cords
            main_window.canvas.move(self._moved_object, *delta)

            main_window.delete_items_to_be_deleted()
            self.generate_box_points(self._moved_object, main_window)
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
        from src.seventh.utils import Buttons
        d.update({
            Buttons.RIGHT_BUTTON: None,
        })

        return d
