import tkinter as tk
from abc import abstractmethod


class AbstractTool:
    def __init__(self):
        self.object = None

    @abstractmethod
    def generate_object(self, canvas: tk.Canvas, x1, y1, x2, y2, *args, **kwargs):
        pass

    def fist_click_in_canvas(self,canvas):
        pass
