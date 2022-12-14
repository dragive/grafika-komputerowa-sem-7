import enum
import tkinter as tk
from json import dumps, loads
from tkinter import Button
from tkinter import filedialog
from tkinter import messagebox
from typing import Callable, Union, Dict

from src.first.tools.AbstractTool import AbstractTool
from src.first.tools.DeleteTool import DeleteTool
from src.first.tools.LineTool import LineTool
from src.first.tools.OvalTool import OvalTool
from src.first.tools.PickTool import PickTool
from src.first.tools.RectangleTool import RectangleTool
from src.first.utils import Buttons


class Tools(enum.Enum):
    DELETE: type(AbstractTool) = DeleteTool
    PICK: type(AbstractTool) = PickTool
    LINE: type(AbstractTool) = LineTool
    OVAL: type(AbstractTool) = OvalTool
    SQUARE: type(AbstractTool) = RectangleTool


class MainWindow:
    def __init__(self):
        self.side_settings_dump_data: Union[None, tk.Button] = None
        self.side_settings_text_field_button_submit: Union[None, tk.Button] = None
        self.side_settings_text_field_params: Union[None, tk.Entry] = None
        self.side_settings_button_pick: Union[None, tk.Button] = None
        self.side_settings_button_square: Union[None, tk.Button] = None
        self.side_settings_button_line: Union[None, tk.Button] = None
        self.side_settings_button_oval: Union[None, tk.Button] = None

        self.__key_mappings: Dict[Buttons, set[Callable]] = {}

        self.main = tk.Tk()

        self.canvas = tk.Canvas(self.main, bg="white", height=600, width=800)
        self.canvas.grid(row=2, column=1)

        self.side_settings = tk.Frame(self.main)
        self.side_settings.grid(row=1, column=1)

        self.tool: AbstractTool = Tools.PICK.value(main_window=self)

        self.add_side_settings_contents()
        self.__set_tool_pick()

        self.parsing_args_def = self.___parsing_text_area_creating_object_4_args_from_tools_impl
        self.initialize_binding_handler()

        self.main.mainloop()

    def __set_tool(self):
        # log(self.tool)
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
            Tools.LINE: self.side_settings_button_line,
            Tools.OVAL: self.side_settings_button_oval,
            Tools.SQUARE: self.side_settings_button_square,
            Tools.DELETE: self.side_settings_button_delete,
        }

    def __set_tool_pick(self):
        self.tool = Tools.PICK.value(main_window=self)
        self.__set_tool()

    def __set_tool_delete(self):
        self.tool = Tools.DELETE.value(main_window=self)
        self.__set_tool()

    def __set_tool_oval(self):
        self.tool = Tools.OVAL.value(main_window=self)
        self.__set_tool()

    def __set_tool_square(self):
        self.tool = Tools.SQUARE.value(main_window=self)
        self.__set_tool()

    def __set_tool_line(self):
        self.tool = Tools.LINE.value(main_window=self)
        self.__set_tool()

    def __submit_side_settings_text_field_params(self):
        abstract_tool: AbstractTool = self.tool
        if abstract_tool is not None:
            values = self.side_settings_text_field_params.get().split(',')
            try:
                values = tuple(int(i) for i in values)
            except ValueError as ex:
                tk.messagebox.showerror("Value Error", "Only int values can be parsed!")
                print(ex)

            self.parsing_args_def(abstract_tool, values)

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

        self.side_settings_button_line = tk.Button(self.side_settings, text="Line", command=self.__set_tool_line)
        self.side_settings_button_line.pack(side=tk.LEFT)

        self.side_settings_button_oval = tk.Button(self.side_settings, text="Oval", command=self.__set_tool_oval)
        self.side_settings_button_oval.pack(side=tk.LEFT)

        self.side_settings_button_square = tk.Button(self.side_settings, text="Square",
                                                     command=self.__set_tool_square)
        self.side_settings_button_square.pack(side=tk.LEFT)

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
                for i in data['data'].items():
                    if i[1]['type'] == 'rectangle':
                        self.canvas.create_rectangle(*i[1]['coords'], width=2)
                    if i[1]['type'] == 'oval':
                        self.canvas.create_oval(*i[1]['coords'], width=2)
                    if i[1]['type'] == 'line':
                        self.canvas.create_line(*i[1]['coords'], width=2)
                    # print(i)
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

    def ___execute_in_set(self, button: Buttons, *args, **kwargs):
        # print(button)
        a = {}
        for i in self.__key_mappings[button]:
            x = i(self, *args, **kwargs, width = 2)
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

    def dump_data(self):
        dialog = filedialog.asksaveasfile(confirmoverwrite=True, mode='w', defaultextension=".json",
                                          filetypes=(("json file extention", "*.json"), ("All Files", "*.*")))
        if dialog is not None:
            data = {
                "data": {
                    identifier: {
                        "coords": self.canvas.coords(identifier),
                        "type": self.canvas.type(identifier)
                    } for identifier in self.canvas.find_all()}
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
