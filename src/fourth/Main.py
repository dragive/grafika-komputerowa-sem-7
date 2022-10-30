import abc
import tkinter as tk
from abc import abstractmethod
from statistics import median
from tkinter import filedialog, messagebox, HORIZONTAL
from typing import Any, Callable, Tuple

import PIL.ImageTk
from PIL import ImageTk
from PIL.Image import Image, NEAREST

from src.fourth.formats.JPEGParser import JPEGParser

WIDTH_OF_BUTTONS = 50


class MainWindow(tk.Tk):
    def __init__(self, ) -> None:
        super().__init__("main screen")
        self._buttons_array: tk.Frame | None = None
        self.canvas: tk.Canvas | None = None
        self.WIDTH_OF_BUTTONS = WIDTH_OF_BUTTONS
        self.image_from_pixels: PIL.Image.Image | None = None
        self.image_from_pixels_original: PIL.Image.Image | None = None
        self.image_tk_from_raw: PIL.PhotoImage | None = None
        self.canvas_drawn_image_id: int | None = None

        self.zoomcycle = 0
        self.zimg_id = None

        self.WIDTH = 640
        self.HEIGHT = 480

    def redraw(self, image: PIL.Image.Image):

        self.image_tk_from_raw = ImageTk.PhotoImage(image)
        if self.canvas_drawn_image_id is None:
            self.canvas_drawn_image_id = self.canvas.create_image((self.image_from_pixels.width + 7) // 2,
                                                                  (self.image_from_pixels.height + 7) // 2,
                                                                  image=self.image_tk_from_raw)
        else:
            self.canvas.itemconfig(self.canvas_drawn_image_id, image=self.image_tk_from_raw)

    def clear_view(self):
        self.canvas.delete('all')

        self.image_from_pixels: PIL.Image.Image | None = None
        self.image_tk_from_raw: PIL.PhotoImage | None = None
        self.canvas_drawn_image_id: int | None = None

    def initialize_view(self) -> "MainWindow":
        self._buttons_array = tk.Frame(master=self)
        self._buttons_array.pack()
        self.canvas = tk.Canvas(self, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()
        self._initialize_array_button()

        return self

    def update_label(self, event, image_to_be_drawn):
        cords = event.x, event.y
        try:
            if image_to_be_drawn:
                self._buttons_array_label_pixel_value_text_variable.set(
                    f'{event.x} {event.y}\t: {image_to_be_drawn.getpixel(cords)}')
            else:
                raise Exception()
        except Exception:
            self._buttons_array_label_pixel_value_text_variable.set(
                f'--- ---\t: (--, --, --))')

    def _initialize_array_button(self):
        self._buttons_array_read_file_button_jpeg = tk.Button(master=self._buttons_array,
                                                              text="Read from file JPEG",
                                                              command=self.__command_read_from_file_jpg)
        self._buttons_array_read_file_button_jpeg.pack(side=tk.LEFT)

        self._buttons_array_write_file_button = tk.Button(master=self._buttons_array,
                                                          text="Write to file",
                                                          command=self.__command_write_to_file)
        self._buttons_array_write_file_button.pack(side=tk.LEFT)

        self._buttons_array_scale_button = tk.Button(master=self._buttons_array,
                                                     text="Scale",
                                                     command=self.__scale)
        self._buttons_array_scale_button.pack(side=tk.LEFT)

        self._buttons_array_filters_button = tk.Button(master=self._buttons_array,
                                                       text="Filters",
                                                       command=self.__lunch_on_top_filters)

        self._buttons_array_filters_button.pack(side=tk.LEFT)

        self._buttons_array_label_pixel_value_text_variable = tk.StringVar()
        self._buttons_array_label_pixel_value = tk.Label(self._buttons_array,
                                                         textvariable=self._buttons_array_label_pixel_value_text_variable)
        self._buttons_array_label_pixel_value.pack(side=tk.LEFT)

    def __lunch_on_top_filters(self):
        self.top_level_filters = FilterSettingsTopLevel(self)

    def __scale(self):
        if self.image_from_pixels is not None:
            self.image_from_pixels = self.image_from_pixels.resize(
                (self.WIDTH, int(self.image_from_pixels.height * self.WIDTH / self.image_from_pixels.width)),
                resample=NEAREST)
            self.redraw(self.image_from_pixels)

    def __command_read_from_file_jpg(self):
        file = filedialog.askopenfilename(filetypes=(
            ("JPG", "*.jpg"),
            ("JPEG", "*.jpeg"),
            ("All Files", "*.*"),
        ))

        if file is not None:
            try:
                self.parse_image_jpg(file)
            except Exception as e:
                messagebox.showerror("Niepoprawy format pliku")
                raise e
        else:
            messagebox.showinfo("Nie wybrano pliku")

    def __command_write_to_file(self):
        new_window = tk.Toplevel(self)
        new_window.title(
            "Save file"
        )
        new_window.label_about_compression = tk.Label(new_window, text="Set compression params:")
        new_window.label_about_compression.pack()

        new_window.scale_compression = tk.Scale(new_window, from_=0, to=100, orient=HORIZONTAL)
        new_window.scale_compression.set(95)
        new_window.scale_compression.pack()

        new_window.label_about_subsampling = tk.Label(new_window, text="Set subsampling params:")
        new_window.label_about_subsampling.pack()

        new_window.scale_subsampling = tk.Scale(new_window, from_=0, to=100, orient=HORIZONTAL)
        new_window.scale_subsampling.pack()
        new_window.scale_subsampling.set(0)

        def submit_handler(*args, **kwargs):
            sub = new_window.scale_subsampling.get()
            com = new_window.scale_compression.get()

            filename = filedialog.asksaveasfilename(filetypes=(('JPEG', '*.jpg',),))
            if filename and self.image_from_pixels:
                if filename[-4:] != '.jpg' and filename[-5:] != '.jpeg':
                    filename = filename + '.jpg'
                self.image_from_pixels.save(filename, quality=com, subsampling=sub)

        new_window.button_submit = tk.Button(new_window, text='Submit',
                                             command=lambda *args, **kwargs: submit_handler(*args, **kwargs))
        new_window.button_submit.pack()

    def parse_image_jpg(self, filename: str):
        JPEGParser().read_from_file(filename, self)

    @staticmethod
    def run():
        MainWindow().initialize_view().mainloop()


class PointTransformation:
    @abstractmethod
    def transform_pixel(self, pixel: tuple[int, int, int], value: tuple[float, float, float]) -> tuple[int, int, int]:
        pass

    def apply(self, image: PIL.Image.Image, raw_value: str):
        try:
            value: tuple[float, float, float] | tuple[float] | Any = raw_value.split(',')
            value = tuple(float(x) for x in value)
            assert len(value) in (1, 3)
        except Exception as ex:
            # tk.messagebox.showerror("Cannot apply this value to pixels", "Cannot apply this value to pixels")
            raise ex
        if len(value) == 1:
            value *= 3
        data = image.getdata()
        data = [self.transform_pixel(i, value) for i in data]
        image.putdata(data)


class AddPointTransformation(PointTransformation):
    def transform_pixel(self, pixel: tuple[int, int, int], value: tuple[float, float, float]) -> tuple[int, int, int]:
        return (
            int(min(255., pixel[0] + value[0])),
            int(min(255., pixel[1] + value[1])),
            int(min(255., pixel[2] + value[2])),
        )


class SubtractPointTransformation(PointTransformation):
    def transform_pixel(self, pixel: tuple[int, int, int], value: tuple[float, float, float]) -> tuple[int, int, int]:
        return (
            int(max(0., pixel[0] - value[0])),
            int(max(0., pixel[1] - value[1])),
            int(max(0., pixel[2] - value[2])),
        )


class MultiplyPointTransformation(PointTransformation):
    def transform_pixel(self, pixel: tuple[int, int, int], value: tuple[float, float, float]) -> tuple[int, int, int]:
        return (
            int(min(255., max(0., pixel[0] * value[0]))),
            int(min(255., max(0., pixel[1] * value[1]))),
            int(min(255., max(0., pixel[2] * value[2]))),
        )


class DividePointTransformation(PointTransformation):
    def transform_pixel(self, pixel: tuple[int, int, int], value: tuple[float, float, float]) -> tuple[int, int, int]:
        return (
            int(min(255., max(0., pixel[0] / value[0]))),
            int(min(255., max(0., pixel[1] / value[1]))),
            int(min(255., max(0., pixel[2] / value[2]))),
        )


class GrayScaleAbstractPointTransformation(PointTransformation, abc.ABC):
    def apply_gray_scale_transform(self, diff, pixel, value):
        return tuple(
            int(pixel_v - (max(min(correct_v, 1.0), 0) * (pixel_v - diff)))
            for correct_v, pixel_v in zip(value, pixel))


class GrayScalePointTransformation(GrayScaleAbstractPointTransformation):
    def transform_pixel(self, pixel: tuple[int, int, int], value: tuple[float, float, float]) -> Tuple[int, ...]:
        diff = sum(pixel) // 3
        ret: Tuple[int, ...] = self.apply_gray_scale_transform(diff, pixel, value)

        return ret


class Gray2ScalePointTransformation(GrayScaleAbstractPointTransformation):
    def transform_pixel(self, pixel: tuple[int, int, int], value: tuple[float, float, float]) -> Tuple[int, ...]:
        diff = median(pixel)
        ret: Tuple[int, ...] = self.apply_gray_scale_transform(diff, pixel, value)

        return ret


class FilterSettingsTopLevel(tk.Toplevel):

    def __init__(self, master: MainWindow) -> None:
        super().__init__(master=master)

        self.master: MainWindow = master
        self.entry_value: tk.Entry

        self._init_button_array()

    def _init_button_array(self):
        self.entry_value: tk.Entry = tk.Entry(self, width=100)
        self.entry_value.grid(row=0, column=0, sticky='nesw')

        self.button_add_value: tk.Button = tk.Button(self,
                                                     text="Add value",
                                                     width=WIDTH_OF_BUTTONS,
                                                     command=
                                                     self.get_command_pixel_transformation(AddPointTransformation))
        self.button_add_value.grid(row=1, column=0, sticky='nesw')

        self.button_subtract_value: tk.Button = tk.Button(self,
                                                          text="Subract value",
                                                          width=WIDTH_OF_BUTTONS,
                                                          command=
                                                          self.get_command_pixel_transformation(
                                                              SubtractPointTransformation))
        self.button_subtract_value.grid(row=2, column=0, sticky='nesw')

        self.button_multiply_value: tk.Button = tk.Button(self,
                                                          text="Multiply value",
                                                          width=WIDTH_OF_BUTTONS,
                                                          command=
                                                          self.get_command_pixel_transformation(
                                                              MultiplyPointTransformation))
        self.button_multiply_value.grid(row=3, column=0, sticky='nesw')

        self.button_divide_value: tk.Button = tk.Button(self,
                                                        text="Divide value",
                                                        width=WIDTH_OF_BUTTONS,
                                                        command=
                                                        self.get_command_pixel_transformation(
                                                            DividePointTransformation))
        self.button_divide_value.grid(row=4, column=0, sticky='nesw')

        self.button_gray_scale_value: tk.Button = tk.Button(self,
                                                            text="Gray value",
                                                            width=WIDTH_OF_BUTTONS,
                                                            command=
                                                            self.get_command_pixel_transformation(
                                                                GrayScalePointTransformation))
        self.button_gray_scale_value.grid(row=5, column=0, sticky='nesw')

        self.button_gray_scale_value2: tk.Button = tk.Button(self,
                                                             text="Gray2 value",
                                                             width=WIDTH_OF_BUTTONS,
                                                             command=
                                                             self.get_command_pixel_transformation(
                                                                 Gray2ScalePointTransformation))
        self.button_gray_scale_value2.grid(row=6, column=0, sticky='nesw')

    def get_command_pixel_transformation(self, name_of_tool: type(PointTransformation)) -> Callable[[Any], Any]:
        return lambda *args, **kwargs: (
            name_of_tool()
            .apply(self.master.image_from_pixels, self.entry_value.get()),
            self.master.redraw(self.master.image_from_pixels)
        )


if __name__ == '__main__':
    MainWindow.run()