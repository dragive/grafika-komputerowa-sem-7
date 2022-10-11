import tkinter as tk
from abc import abstractmethod


class AbstractTool:
    def __init__(self):
        self.object: tk.Widget
        self.cords: tuple[int, int]

    @abstractmethod
    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        pass

    def fist_click_in_canvas(self, canvas):
        print("first_click" + str(type(self)))

    def second_click(self, canvas):
        print("second_click" + str(type(self)))
