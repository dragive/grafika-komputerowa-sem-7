import enum
import tkinter as tk
from tkinter import Button
from tkinter import messagebox
from typing import Callable, Union

from src.first.tools.AbstractTool import AbstractTool
from src.first.tools.LineTool import LineTool
from src.first.tools.OvalTool import OvalTool
from src.first.tools.PickTool import PickTool
from src.first.tools.RectangleTool import RectangleTool


class Tools(enum.Enum):
    PICK: tuple[str, AbstractTool] = ("PICK", PickTool)
    LINE: tuple[str, AbstractTool] = ("LINE", LineTool)
    OVAL: tuple[str, AbstractTool] = ("OVAL", OvalTool)
    SQUARE: tuple[str, AbstractTool] = ("SQUARE", RectangleTool)


class MainWindow:
    def __init__(self):
        self.side_settings_text_field_button_submit: Union[None, tk.Button] = None
        self.side_settings_text_field_params: Union[None, tk.Button] = None
        self.side_settings_button_pick: Union[None, tk.Button] = None
        self.side_settings_button_square: Union[None, tk.Button] = None
        self.side_settings_button_line: Union[None, tk.Button] = None
        self.side_settings_button_oval: Union[None, tk.Button] = None

        self.main = tk.Tk()

        self.canvas = tk.Canvas(self.main, bg="white", height=300, width=400)
        self.canvas.grid(row=2, column=1)

        self.side_settings = tk.Frame(self.main)
        self.side_settings.grid(row=1, column=1)

        self.tool: tuple[str, AbstractTool] = Tools.PICK

        self.add_side_settings_contents()
        self.__set_tool_pick()

        self.parsing_args_def = self.___parsing_text_area_creating_object_4_args_from_tools_impl

        self.main.mainloop()

    def __set_tool(self):
        print(f"{self.tool.value[0]=}")
        if self.tool == Tools.PICK:
            self.disable_button(self.side_settings_text_field_button_submit)
            self.__set_impl_none()
        else:
            self.enable_button(self.side_settings_text_field_button_submit)
            self.__set_impl_4_args_creating_object()

        for k, v in self.__get_buttons_dict.items():
            if not self.tool == k:
                self.enable_button(v)
            else:
                self.disable_button(v)

    @property
    def __get_buttons_dict(self) -> dict[tuple[str, AbstractTool], Button]:
        return {
            Tools.PICK: self.side_settings_button_pick,
            Tools.LINE: self.side_settings_button_line,
            Tools.OVAL: self.side_settings_button_oval,
            Tools.SQUARE: self.side_settings_button_square,
        }

    def __set_tool_pick(self):
        self.tool = Tools.PICK
        self.__set_tool()

    def __set_tool_oval(self):
        self.tool = Tools.OVAL
        self.__set_tool()

    def __set_tool_square(self):
        self.tool = Tools.SQUARE
        self.__set_tool()

    def __set_tool_line(self):
        self.tool = Tools.LINE
        self.__set_tool()

    def __submit_side_settings_text_field_params(self):
        abstract_tool: Callable = self.tool.value[1]
        if abstract_tool is not None:
            abstract_tool: AbstractTool = abstract_tool()
            values = self.side_settings_text_field_params.get().split(',')
            try:
                values = tuple(int(i) for i in values)
            except ValueError as ex:
                tk.messagebox.showerror("Value Error", "Only int values can be parsed!")
                print(ex)

            self.parsing_args_def(abstract_tool, values)

    def ___parsing_text_area_creating_object_4_args_from_tools_impl(self, abstract_tool, values):
        if len(values) == 4:
            abstract_tool.generate_object(self.canvas, *values,width = 2)

    def ___parsing_text_area_none_impl(self, abstract_tool, values):
        pass

    def __set_impl_4_args_creating_object(self):
        self.parsing_args_def = self.___parsing_text_area_creating_object_4_args_from_tools_impl

    def __set_impl_none(self):
        self.parsing_args_def = self.___parsing_text_area_none_impl

    def add_side_settings_contents(self):
        self.side_settings_button_pick = tk.Button(self.side_settings, text="Pick", command=self.__set_tool_pick)
        self.side_settings_button_pick.pack(side=tk.LEFT)

        self.side_settings_button_line = tk.Button(self.side_settings, text="Line", command=self.__set_tool_line)
        self.side_settings_button_line.pack(side=tk.LEFT)

        self.side_settings_button_oval = tk.Button(self.side_settings, text="Oval", command=self.__set_tool_oval)
        self.side_settings_button_oval.pack(side=tk.LEFT)

        self.side_settings_button_square = tk.Button(self.side_settings, text="Square", command=self.__set_tool_square)
        self.side_settings_button_square.pack(side=tk.LEFT)

        self.side_settings_text_field_params = tk.Entry(self.side_settings)
        self.side_settings_text_field_params.pack(side=tk.LEFT)

        self.side_settings_text_field_button_submit = tk.Button(self.side_settings,
                                                                command=self.__submit_side_settings_text_field_params,
                                                                text="Submit")
        self.side_settings_text_field_button_submit.pack(side=tk.LEFT)


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


def main():
    top = tk.Tk()

    C = tk.Canvas(top, bg="white", height=300, width=400)
    button = tk.Button(top, text="123", command=lambda: print("hii"))
    button.pack()
    C.bind("<B1-Motion>", log)
    C.bind("<ButtonRelease-first>", log)
    arc = C.create_line(10, 20, 30, 40, fill="black")

    C.pack()
    top.mainloop()


if __name__ == '__main__':
    MainWindow()
