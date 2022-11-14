import enum
import tkinter as tk
from tkinter import Button
from typing import Callable, Union, Dict, Collection

from src.sixth.tools.AbstractTool import AbstractTool
from src.sixth.tools.PickTool import PickTool
from src.sixth.tools.RectangleTool import RectangleTool
from src.sixth.utils import Buttons

BEZIER_POINTS = 500


class Tools(enum.Enum):
    PICK: type(AbstractTool) = PickTool
    POINT: type(AbstractTool) = RectangleTool


class MainWindow:
    def __init__(self):
        self.side_settings_dump_data: Union[None, tk.Button] = None
        self.side_settings_text_field_button_submit: Union[None, tk.Button] = None
        self.side_settings_text_field_params: Union[None, tk.Entry] = None
        self.side_settings_button_pick: Union[None, tk.Button] = None
        self.side_settings_button_point: Union[None, tk.Button] = None
        self.__key_mappings: Dict[Buttons, set[Callable]] = {}

        self.main = tk.Tk()

        self.canvas = tk.Canvas(self.main, bg="white", height=600, width=800)
        self.canvas.grid(row=2, column=1)

        self.side_settings = tk.Frame(self.main)
        self.side_settings.grid(row=1, column=1)

        self.point_lines = []
        self.bezier_lines = []
        self.points = []

        self.tool: AbstractTool = Tools.PICK.value(main_window=self)

        self.add_side_settings_contents()
        self.__set_tool_pick()

        self.parsing_args_def = self.___parsing_text_area_creating_object_4_args_from_tools_impl
        self.initialize_binding_handler()

        self.main.mainloop()

    def redraw_bezier(self):
        def _reduce_points_coords(coords: tuple[float, float, float, float]) -> tuple[float, float] | None:
            return (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2

        def _map_to_coords(identifier: int) -> tuple[float, float, float, float]:
            return self.canvas.coords(identifier)

        def map_points():
            return list(
                map(_reduce_points_coords,
                    map(_map_to_coords,
                        self.points
                        )
                    )
            )

        points = map_points()
        collection = [x for x in map(
            lambda x: list(a for b in x for a in b),
            ((points[index], points[index + 1]) for index in range(len(points) - 1))
        )]

        self._draw_lines_between_points(collection)
        self._draw_bezier(collection)

    def _draw_bezier(self, collection: Collection[tuple[float, float, float, float]]):

        def _calculate_point(c, i):
            x1, y1, x2, y2 = c
            x = (1 - i) * x1 + i * x2
            y = (1 - i) * y1 + i * y2
            return (x, y)

        pre_final_collection = []
        for _i in range(BEZIER_POINTS):
            i = _i / (BEZIER_POINTS - 1)
            coll = collection
            while len(coll) > 1:
                coll = self.double_collection([
                    _calculate_point(c, i) for c in coll
                ])

            if coll:
                pre_final_collection.append(coll[0])

        final_collection = []
        for _i, element in enumerate(pre_final_collection):
            i = _i / (BEZIER_POINTS - 1)

            final_collection.append(_calculate_point(element, i))
        final_collection = self.double_collection(final_collection)

        for i in self.bezier_lines:
            self.canvas.delete(i)

        self.bezier_lines = [
            self.canvas.create_line(*line, width=2)
            for line in final_collection
        ]

    def double_collection(self, _points_for_processing):
        _double_points = []
        for i in range(len(_points_for_processing) - 1):
            temp = [] + list(_points_for_processing[i]) + list(_points_for_processing[i + 1])
            _double_points.append(temp)
        return _double_points

    def _draw_lines_between_points(self, collection):
        for i in self.point_lines:
            self.canvas.delete(i)

        self.point_lines = [
            self.canvas.create_line(*pair, fill='red')
            for pair in collection
        ]

    def __set_tool(self):
        # if isinstance(self.tool, Tools.PICK.value):
        #     self.disable_button(self.side_settings_text_field_button_submit)
        #     self.__set_impl_none()
        # else:
        #     self.enable_button(self.side_settings_text_field_button_submit)
        #     self.__set_impl_4_args_creating_object()

        for k, v in self.__get_buttons_dict.items():
            if not isinstance(self.tool, k.value):
                self.enable_button(v)
            else:
                self.disable_button(v)

        self.__reset_bindings_in_canvas()
        self.bind_buttons(self.tool.get_initial_mapping)

    def __reset_bindings_in_canvas(self):
        key_mappings: Dict[Buttons, set[Callable]] = self.__key_mappings
        for b in Buttons:
            key_mappings[b] = set()

    @property
    def __get_buttons_dict(self) -> dict[type(AbstractTool), Button]:
        return {
            Tools.PICK: self.side_settings_button_pick,
            Tools.POINT: self.side_settings_button_point,
        }

    def __set_tool_pick(self):
        self.tool = Tools.PICK.value(main_window=self)
        self.__set_tool()

    def __set_tool_point(self):
        self.tool = Tools.POINT.value(main_window=self)
        self.__set_tool()

    def __submit_side_settings_text_field_params(self):
        abstract_tool: AbstractTool = self.tool
        if abstract_tool is not None:
            values = self.side_settings_text_field_params.get().split(';')

            values = list(map(lambda x: tuple(map(float, x)), map(lambda x: x.split(','), values)))

            for coords in values:
                self.create_point(coords)

    def create_point(self, coords: tuple[float, ...]) -> None:
        self.points.append(RectangleTool(self).generate_object(self.canvas, *coords))
        self.redraw_bezier()

    def ___parsing_text_area_creating_object_4_args_from_tools_impl(self, abstract_tool, values):
        if len(values) == 4:
            abstract_tool.generate_object(self.canvas, *values, width=2)

    def ___parsing_text_area_none_impl(self, abstract_tool, values):
        pass

    def __set_impl_4_args_creating_object(self):
        self.parsing_args_def = self.___parsing_text_area_creating_object_4_args_from_tools_impl

    def __set_impl_none(self):
        self.parsing_args_def = self.___parsing_text_area_none_impl

    def add_side_settings_contents(self):
        self.side_settings_button_pick = tk.Button(self.side_settings, text="Pick", command=self.__set_tool_pick)
        self.side_settings_button_pick.pack(side=tk.LEFT)

        self.side_settings_button_point = tk.Button(self.side_settings, text="Point",
                                                    command=self.__set_tool_point)
        self.side_settings_button_point.pack(side=tk.LEFT)

        self.side_settings_text_field_params = tk.Entry(self.side_settings)
        self.side_settings_text_field_params.pack(side=tk.LEFT)

        self.side_settings_text_field_button_submit = tk.Button(self.side_settings,
                                                                command=self.__submit_side_settings_text_field_params,
                                                                text="Submit")
        self.side_settings_text_field_button_submit.pack(side=tk.LEFT)

    def clear_canvas(self):
        for i in self.canvas.find_all():
            self.canvas.delete(i)

    def bind_buttons(self, bindings: Dict[Buttons, Callable]):
        for k, v in bindings.items():
            if v is not None:
                self.__manage_binding(k, v)
            else:
                self.__manage_binding(k, remove=True)

    def __manage_binding(self, button: Buttons, exec=None, remove=False):
        if remove:
            self.__key_mappings[button] = set()
            return
        self.__key_mappings[button] = set()
        if exec is not None:
            self.__key_mappings[button].add(exec)

    def initialize_binding_handler(self):

        self.canvas.bind(Buttons.LEFT_BUTTON.value, self.return_handler(Buttons.LEFT_BUTTON), add=True)
        self.canvas.bind(Buttons.LEFT_BUTTON_MOTION.value, self.return_handler(Buttons.LEFT_BUTTON_MOTION), add=True)
        self.canvas.bind(Buttons.LEFT_BUTTON_RELEASE.value, self.return_handler(Buttons.LEFT_BUTTON_RELEASE), add=True)
        self.canvas.bind(Buttons.RIGHT_BUTTON_DOUBLE.value, self.return_handler(Buttons.RIGHT_BUTTON_DOUBLE), add=True)

    def ___execute_in_set(self, button: Buttons, *args, **kwargs):
        a = {}
        for i in self.__key_mappings[button]:
            x = i(self, *args, **kwargs, width=2)
            a.update(x)

        self.bind_buttons(a)

    def return_handler(self, button: Buttons):
        return lambda *args, **kwargs: self.___execute_in_set(button, *args, **kwargs)

    @staticmethod
    def enable_button(b: tk.Button):
        b['state'] = 'normal'

    @staticmethod
    def disable_button(b: tk.Button):
        b['state'] = 'disabled'

    @staticmethod
    def active_button(b: tk.Button):
        b['state'] = 'active'


def log(*args, **kwargs):
    print(f"{args=}")
    print(f"{kwargs=}")


if __name__ == '__main__':
    MainWindow()
