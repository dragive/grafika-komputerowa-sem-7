import tkinter as tk
from numbers import Real
from statistics import mean
from typing import Dict, Callable, Collection

import numpy as np

from src.seventh.tools.AbstractTool import AbstractTool


class PickTool(AbstractTool):

    def __init__(self, *args, main_window: 'MainWindow' = None, **kwargs) -> None:
        self._moved_object: int | None = None
        self.center_point: int | None = None
        self.rotation_point: int | None = None
        self._first_click_cords: tuple[int] | list[int] | None = None

        self.initial_polygon_coords: None | Collection = None
        self.initial_box_point_coords: None | Collection = None
        self.initial_other_box_point_coords: None | Dict[int, Collection[int, ...]] = None

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
            self._first_click_cords = cords
            self._moved_object = next(iter(intersection_with_box_points))

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
        self.center_point = None

        self.initial_polygon_coords: None | Collection = None
        self.initial_box_point_coords: None | Collection = None
        self.initial_other_box_point_coords: None | Dict[int, Collection[int, ...]] = None

    def generate_box_points(self, identifier, main_window):
        raw_coords = main_window.canvas.coords(identifier)
        xs, ys = raw_coords[::2], raw_coords[1::2]

        avg_x, avg_y, max_x, max_y, min_x, min_y = self.prepare_x_y_cords_stat(xs, ys)

        for x in [min_x, max_x]:
            for y in [min_y, max_y]:
                main_window.items_to_be_deleted_at_changing_tools = main_window.canvas \
                    .create_oval(x - 5, y - 5,
                                 x + 5, y + 5,
                                 fill="blue")
        self.center_point = main_window.canvas.create_oval(avg_x - 5, avg_y - 5,
                                                           avg_x + 5, avg_y + 5,
                                                           fill="yellow")

        main_window.items_to_be_deleted_at_changing_tools = self.center_point

        self.rotation_point = main_window.canvas.create_oval(avg_x + 10, avg_y - 5,
                                                             avg_x + 20, avg_y + 5,
                                                             fill="green")

        main_window.items_to_be_deleted_at_changing_tools = self.rotation_point

    def prepare_x_y_cords_stat(self, xs, ys):
        min_x = min(xs)
        avg_x = mean(xs)
        max_x = max(xs)
        min_y = min(ys)
        avg_y = mean(ys)
        max_y = max(ys)
        return avg_x, avg_y, max_x, max_y, min_x, min_y

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

            if self._moved_object == self.center_point:
                main_window.canvas.move(self.rotation_point, *delta)

            if self._moved_object not in main_window.items_to_be_deleted_at_changing_tools:

                for obj in main_window.items_to_be_deleted_at_changing_tools:
                    main_window.canvas.move(obj, *delta)
            else:
                if self._moved_object not in (self.center_point, self.rotation_point):
                    if self.initial_polygon_coords is None \
                            or self.initial_other_box_point_coords is None \
                            or self.initial_box_point_coords is None:
                        self.initial_polygon_coords = main_window.canvas.coords(main_window.checked_item)
                        self.initial_box_point_coords = self.get_mean_cords_of_point(main_window, self._moved_object)
                        self.initial_other_box_point_coords = {
                            o: self.get_mean_cords_of_point(main_window,o)
                            for o in main_window.items_to_be_deleted_at_changing_tools
                        }
                        pass

                    current_box_point_coords = self.get_mean_cords_of_point(main_window, self._moved_object)
                    center_point_center = self.get_mean_cords_of_point(main_window, self.center_point)

                    scale = list(
                        map(
                            (lambda tu: (tu[0] / tu[1])),
                            zip([a - b for a, b in zip(current_box_point_coords, center_point_center)],
                                [a - b for a, b in zip(self.initial_box_point_coords, center_point_center)]))
                    )

                    new_cords = []

                    for i, x in enumerate(self.initial_polygon_coords):
                        new_cords.append((x - center_point_center[i % 2]) * scale[i % 2] + center_point_center[i % 2])

                    main_window.canvas.coords(main_window.checked_item, *new_cords)

                    for point in main_window.items_to_be_deleted_at_changing_tools:
                        if point in (self._moved_object, self.rotation_point):
                            continue
                        initial_coords = self.initial_other_box_point_coords[point]
                        coords = [(x - center_point_center[i % 2]) * scale[i % 2] + center_point_center[i % 2]
                                  for i, x in enumerate(initial_coords)]
                        main_window.canvas.coords(point,
                                                  coords[0] + 5, coords[1] + 5,
                                                  coords[0] - 5, coords[1] - 5,
                                                  )
                elif self._moved_object == self.rotation_point:
                    if self.initial_polygon_coords is None:
                        self.initial_polygon_coords = main_window.canvas.coords(main_window.checked_item)

                    center_points_coords = self.get_mean_cords_of_point(main_window, self.center_point)

                    x2, y2 = [a - b for a, b in zip(self.get_mean_cords_of_point(main_window, self.rotation_point),
                                                    center_points_coords)]

                    y2 = -y2
                    sin = np.divide(y2, np.sqrt(np.add(pow(x2, 2), pow(y2, 2))))
                    cos = np.divide(x2, np.sqrt(np.add(pow(x2, 2), pow(y2, 2))))

                    def map_to_new_coords(p: tuple[Real, Real]):
                        x, y = p
                        x -= center_points_coords[0]
                        y -= center_points_coords[1]

                        y *= -1
                        new_x, new_y = (x * cos - y * sin, x * sin + y * cos)

                        new_y *= -1

                        new_x += center_points_coords[0]
                        new_y += center_points_coords[1]

                        return round(new_x), round(new_y)

                    initial_cords_of_checked_item_grouped = list(zip(
                        self.initial_polygon_coords[::2],
                        self.initial_polygon_coords[1::2]))

                    new_coords_of_checked_item = list(map(map_to_new_coords, initial_cords_of_checked_item_grouped))

                    unpacked_new_coords = [a for i in new_coords_of_checked_item for a in i]
                    main_window.canvas.coords(main_window.checked_item, *unpacked_new_coords)

                    # rotation of box points
                    if self.initial_other_box_point_coords is None:
                        self.initial_other_box_point_coords = {
                            o: self.get_mean_cords_of_point(main_window,o)
                            for o in main_window.items_to_be_deleted_at_changing_tools
                        }

                    for item, coords in self.initial_other_box_point_coords.items():
                        if item not in [self.rotation_point, self.center_point]:
                            new_point_center_coords = map_to_new_coords(coords)

                            main_window.canvas.coords(item,
                                                      new_point_center_coords[0] + 5, new_point_center_coords[1] + 5,
                                                      new_point_center_coords[0] - 5, new_point_center_coords[1] - 5)

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


        self.initial_polygon_coords: None | Collection = None
        self.initial_box_point_coords: None | Collection = None
        self.initial_other_box_point_coords: None | Dict[int, Collection[int, ...]] = None


        return d
