import enum
import tkinter as tk
from json import dumps, loads
from tkinter import Button
from tkinter import filedialog
from tkinter import messagebox
from typing import Callable, Union, Dict, Set

import numpy as np

from src.seventh.tools.AbstractTool import AbstractTool
from src.seventh.tools.DeleteTool import DeleteTool
from src.seventh.tools.DrawingTool import DrawingTool
from src.seventh.tools.OvalTool import OvalTool
from src.seventh.tools.PickTool import PickTool
from src.seventh.tools.RectangleTool import RectangleTool
from src.seventh.utils import Buttons


class Tools(enum.Enum):
    DELETE: type(AbstractTool) = DeleteTool
    PICK: type(AbstractTool) = PickTool
    DRAWING: type(AbstractTool) = DrawingTool
    OVAL: type(AbstractTool) = OvalTool
    SQUARE: type(AbstractTool) = RectangleTool


class MainWindow:
    def __init__(self):
        self.side_settings_dump_data: Union[None, tk.Button] = None
        self.side_settings_text_field_button_submit: Union[None, tk.Button] = None
        self.side_settings_text_field_params: Union[None, tk.Entry] = None
        self.side_settings_button_pick: Union[None, tk.Button] = None
        self.side_settings_button_square: Union[None, tk.Button] = None
        # self.side_settings_button_line: Union[None, tk.Button] = None
        self.side_settings_button_oval: Union[None, tk.Button] = None
        self.side_settings_button_drawing: Union[None, tk.Button] = None

        self.__key_mappings: Dict[Buttons, set[Callable]] = {}

        self.main = tk.Tk()

        self.canvas = tk.Canvas(self.main, bg="white", height=600, width=800)
        self.canvas.grid(row=2, column=1)

        self.side_settings = tk.Frame(self.main)
        self.side_settings.grid(row=1, column=1)

        self.checked_item: None | int = None
        self._items_to_be_deleted_at_changing_tools: None | Set[int] = set()

        self.tool: AbstractTool = Tools.PICK.value(main_window=self)

        self.add_side_settings_contents()
        self.__set_tool_pick()

        self.parsing_args_def = self.___parsing_text_area_creating_object_4_args_from_tools_impl
        self.initialize_binding_handler()

        self.main.mainloop()

    @property
    def items_to_be_deleted_at_changing_tools(self) -> None:
        return self._items_to_be_deleted_at_changing_tools

    @items_to_be_deleted_at_changing_tools.setter
    def items_to_be_deleted_at_changing_tools(self, value: int) -> None:
        self._items_to_be_deleted_at_changing_tools.add(value)

    def __set_tool(self):
        self.delete_items_to_be_deleted()

        if isinstance(self.tool, Tools.PICK.value):
            self.disable_button(self.side_settings_text_field_button_submit)
            self.__set_impl_none()
        else:
            self.enable_button(self.side_settings_text_field_button_submit)
            self.__set_impl_4_args_creating_object()

        for k, v in self.__get_buttons_dict.items():
            if not isinstance(self.tool, k.value):
                self.enable_button(v)
            else:
                self.disable_button(v)

        self.__reset_bindings_in_canvas()
        self.bind_buttons(self.tool.get_initial_mapping)

    def delete_items_to_be_deleted(self):
        for item in self._items_to_be_deleted_at_changing_tools:
            self.canvas.delete(item)
        self._items_to_be_deleted_at_changing_tools.clear()

    def __reset_bindings_in_canvas(self):
        key_mappings: Dict[Buttons, set[Callable]] = self.__key_mappings
        for b in Buttons:
            key_mappings[b] = set()

    @property
    def __get_buttons_dict(self) -> dict[type(AbstractTool), Button]:
        return {
            Tools.PICK: self.side_settings_button_pick,
            Tools.OVAL: self.side_settings_button_oval,
            Tools.DRAWING: self.side_settings_button_drawing,
            Tools.SQUARE: self.side_settings_button_square,
            Tools.DELETE: self.side_settings_button_delete,
        }

    def __set_tool_pick(self):
        self.pre_set_tool()
        self.tool = Tools.PICK.value(main_window=self)
        self.__set_tool()

    def __set_tool_drawing(self):
        self.pre_set_tool()
        self.tool = Tools.DRAWING.value(main_window=self)
        self.__set_tool()

    def __set_tool_delete(self):
        self.pre_set_tool()
        self.tool = Tools.DELETE.value(main_window=self)
        self.__set_tool()

    def __set_tool_oval(self):
        self.pre_set_tool()
        self.tool = Tools.OVAL.value(main_window=self)
        self.__set_tool()

    def __set_tool_square(self):
        self.pre_set_tool()
        self.tool = Tools.SQUARE.value(main_window=self)
        self.__set_tool()

    def pre_set_tool(self):
        if isinstance(self.tool, DrawingTool):
            tool: DrawingTool = self.tool
            tool.clear_drawn_points()

    def __submit_side_settings_text_field_params(self):
        def create_polygon(points_raw):
            points = tuple(float(x) for x in points_raw.split(','))
            print(self.canvas.create_polygon(*points, fill="black"))

        def move_polygon(id_and_translation_raw):
            content = tuple(int(x) for x in id_and_translation_raw.split(','))
            self.canvas.move(*content)

        def rotate_polygon(id_reference_point_degrees):
            id, x, y, degrees = tuple(int(x) for x in id_reference_point_degrees.split(','))

            coords = self.canvas.coords(id)

            sin = np.sin(((degrees + 360) % 360) / 360 * 2 * np.pi)
            cos = np.cos(((degrees + 360) % 360) / 360 * 2 * np.pi)

            def map_to_new_coords(x, y, ref_x, ref_y):
                x -= ref_x
                y -= ref_y

                y *= -1
                new_x, new_y = (x * cos - y * sin, x * sin + y * cos)

                new_y *= -1

                new_x += ref_x
                new_y += ref_y

                return round(new_x), round(new_y)

            new_coords = tuple(
                a for x_1, y_1 in zip(coords[::2], coords[1::2]) for a in map_to_new_coords(x_1, y_1, x, y))
            self.canvas.coords(id, *new_coords)

        def scale_polygon(id_reference_point_scale_x_y):
            id, ref_x, ref_y, scale_x, scale_y = tuple(int(x) for x in id_reference_point_scale_x_y.split(','))

            coords = self.canvas.coords(id)

            xs = coords[::2]
            ys = coords[1::2]

            normalized_xs = tuple(_x - ref_x for _x in xs)
            normalized_ys = tuple(_y - ref_y for _y in ys)

            scaled_xs = tuple(_x * scale_x for _x in normalized_xs)
            scaled_ys = tuple(_y * scale_y for _y in normalized_ys)

            unnormalized_xs = tuple(_x + ref_x for _x in scaled_xs)
            unnormalized_ys = tuple(_y + ref_y for _y in scaled_ys)

            final_coords = tuple(a for _a in zip(unnormalized_xs, unnormalized_ys) for a in _a)

            self.canvas.coords(id, *final_coords)

        values = self.side_settings_text_field_params.get().split(' ')
        match values[0]:
            case 'c':
                create_polygon(values[1])
            case 'm':
                move_polygon(values[1])
            case 'r':
                rotate_polygon(values[1])
            case 's':
                scale_polygon(values[1])
            case 'c*':
                for i in self.canvas.find_all():
                    create_polygon(f'{i},{values[1]}')
            case 'm*':
                for i in self.canvas.find_all():
                    move_polygon(f'{i},{values[1]}')
            case 'r*':
                for i in self.canvas.find_all():
                    rotate_polygon(f'{i},{values[1]}')
            case 's*':
                for i in self.canvas.find_all():
                    scale_polygon(f'{i},{values[1]}')

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

        self.side_settings_button_delete = tk.Button(self.side_settings, text="Delete", command=self.__set_tool_delete)
        self.side_settings_button_delete.pack(side=tk.LEFT)

        self.side_settings_button_oval = tk.Button(self.side_settings, text="Oval", command=self.__set_tool_oval)
        self.side_settings_button_oval.pack(side=tk.LEFT)

        self.side_settings_button_square = tk.Button(self.side_settings, text="Square",
                                                     command=self.__set_tool_square)
        self.side_settings_button_square.pack(side=tk.LEFT)

        self.side_settings_button_drawing = tk.Button(self.side_settings, text="Draw",
                                                      command=self.__set_tool_drawing)
        self.side_settings_button_drawing.pack(side=tk.LEFT)

        self.side_settings_text_field_params = tk.Entry(self.side_settings)
        self.side_settings_text_field_params.pack(side=tk.LEFT)

        self.side_settings_text_field_button_submit = tk.Button(self.side_settings,
                                                                command=self.__submit_side_settings_text_field_params,
                                                                text="Submit")
        self.side_settings_text_field_button_submit.pack(side=tk.LEFT)

        self.side_settings_dump_data = tk.Button(self.side_settings,
                                                 command=self.dump_data,
                                                 text="Dump")
        self.side_settings_dump_data.pack(side=tk.LEFT)

        self.side_settings_clear_canvas = tk.Button(self.side_settings,
                                                    command=self.clear_canvas,
                                                    text="Clear Canvas")
        self.side_settings_clear_canvas.pack(side=tk.LEFT)

        self.side_settings_read_state_from_file = tk.Button(self.side_settings,
                                                            command=self.read_state_from_file,
                                                            text="Read from file")
        self.side_settings_read_state_from_file.pack(side=tk.LEFT)

    def read_state_from_file(self):
        dialog = filedialog.askopenfile(mode='r', defaultextension=".json",
                                        filetypes=(("json file extension", "*.json"), ("All Files", "*.*")))

        data = None
        if dialog is not None:

            try:
                data = loads(dialog.read())
            finally:
                dialog.close()

        if data is not None:
            try:
                # print(data)
                for i in data['data'].values():
                    if i['type'] == 'rectangle':
                        self.canvas.create_rectangle(*i['coords'], width=2)
                    if i['type'] == 'oval':
                        self.canvas.create_oval(*i['coords'], width=2)
                    if i['type'] == 'polygon':
                        self.canvas.create_polygon(*i['coords'], width=2)
            except Exception:
                messagebox.showerror("Error while parsing a file!")

        else:
            messagebox.showinfo("File Not Found!", "File was not found")

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
        # if button in self.__key_mappings.keys():
        self.__key_mappings[button] = set()
        if exec is not None:
            self.__key_mappings[button].add(exec)

    def initialize_binding_handler(self):

        self.canvas.bind(Buttons.LEFT_BUTTON.value, self.return_handler(Buttons.LEFT_BUTTON), add=True)
        self.canvas.bind(Buttons.LEFT_BUTTON_MOTION.value, self.return_handler(Buttons.LEFT_BUTTON_MOTION), add=True)
        self.canvas.bind(Buttons.MOTION.value, self.return_handler(Buttons.MOTION), add=True)
        self.canvas.bind(Buttons.LEFT_BUTTON_RELEASE.value, self.return_handler(Buttons.LEFT_BUTTON_RELEASE), add=True)
        self.canvas.bind(Buttons.RIGHT_BUTTON_DOUBLE.value, self.return_handler(Buttons.RIGHT_BUTTON_DOUBLE), add=True)
        self.canvas.bind(Buttons.RIGHT_BUTTON.value, self.return_handler(Buttons.RIGHT_BUTTON), add=True)

    def ___execute_in_set(self, button: Buttons, *args, **kwargs):
        # print(button)
        a = {}
        for i in self.__key_mappings[button]:
            x = i(self, *args, **kwargs, width=2)
            a.update(x)
            pass

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

    def dump_data(self):
        dialog = filedialog.asksaveasfile(confirmoverwrite=True, mode='w', defaultextension=".json",
                                          filetypes=(("json file extention", "*.json"), ("All Files", "*.*")))
        if dialog is not None:
            data = {
                "data": {
                    identifier: {
                        "coords": self.canvas.coords(identifier),
                        "type": self.canvas.type(identifier)
                    } for identifier in self.canvas.find_all()
                    if identifier not in self.items_to_be_deleted_at_changing_tools}
            }
            try:
                dialog.write(dumps(data))
            finally:
                dialog.close()


def log(*args, **kwargs):
    print(f"{args=}")
    print(f"{kwargs=}")


if __name__ == '__main__':
    MainWindow()
