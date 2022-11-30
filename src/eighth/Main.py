import abc
import tkinter as tk
from abc import abstractmethod
from tkinter import filedialog, messagebox, HORIZONTAL
from typing import Tuple, Any, Callable

import PIL.ImageTk
import numpy as np
from PIL import ImageTk
from PIL.Image import Image, NEAREST

from src.eighth.ImageWrapper import ImageWrapper
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

    def set_image_from_pixels(self, img):
        self.image_from_pixels = img
        return img

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

        self._buttons_array_morphology_button = tk.Button(master=self._buttons_array,
                                                          text="Morphology",
                                                          command=self.__lunch_on_top_morphology)

        self._buttons_array_morphology_button.pack(side=tk.LEFT)

        self._buttons_array_label_pixel_value_text_variable = tk.StringVar()
        self._buttons_array_label_pixel_value = tk.Label(self._buttons_array,
                                                         textvariable=self._buttons_array_label_pixel_value_text_variable)
        self._buttons_array_label_pixel_value.pack(side=tk.LEFT)

    def __lunch_on_top_morphology(self):
        self.top_level_morphology = MorphologySettingsTopLevel(self)
        GrayScalePointTransformation().apply(self, self.image_from_pixels, "1")
        self.redraw(self.image_from_pixels)

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


class FilterMedian:
    def filter(self, im: PIL.Image.Image):
        im.rankfilter()


class ThreeXThreeTransformation:
    @abstractmethod
    def transform_pixel(self, pixel: Tuple[
        tuple[Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int]],
        tuple[Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int]],
        tuple[Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int]],
    ]) -> tuple[int, int, int]:
        pass

    def apply(self, master, image: PIL.Image.Image):
        data = image.load()

        width, height = image.width, image.height

        def get_pixels(w, h):
            if w == 0:
                if h == 0:
                    return (
                        (
                            data[w, h],
                            data[w + 1, h],
                        ),
                        (
                            data[w, (h + 1)],
                            data[w + 1, (h + 1)],
                        ),
                    )
                elif h >= height - 1:
                    return (
                        (
                            data[w, (h - 1)],
                            data[w + 1, (h - 1)],
                        ),
                        (
                            data[(w, h)],
                            data[(w + 1, h)],
                        ),
                    )
                else:
                    return (
                        (
                            data[w, (h - 1)],
                            data[w + 1, (h - 1)],
                        ),
                        (
                            data[w, h],
                            data[w + 1, h],
                        ),
                        (
                            data[w, (h + 1)],
                            data[w + 1, (h + 1)],
                        ),
                    )
            elif w >= width - 1:
                if h == 0:
                    return (
                        (
                            data[w - 1, h],
                            data[w, h],
                        ),
                        (
                            data[w - 1, h + 1,],
                            data[w, h + 1],
                        ),
                    )
                elif h >= height - 1:
                    return (
                        (
                            data[w - 1, (h - 1)],
                            data[w, (h - 1)],
                        ),
                        (
                            data[w - 1, h],
                            data[w, h],
                        ),
                    )
                else:
                    return (
                        (
                            data[w - 1, h - 1],
                            data[w, h - 1],
                        ),
                        (
                            data[w - 1, h],
                            data[w, h],
                        ),
                        (
                            data[w - 1, h + 1],
                            data[w, h + 1],
                        ),
                    )

            if h == 0:
                return (
                    (
                        data[w - 1, h],
                        data[w, h],
                        data[w + 1, h],
                    ),
                    (
                        data[w - 1, h + 1,],
                        data[w, h + 1],
                        data[w + 1, h + 1],
                    ),

                )
            elif h >= height - 1:
                return (
                    (
                        data[w - 1, h - 1],
                        data[w, h - 1],
                        data[w + 1, h - 1],
                    ),
                    (
                        data[w - 1, h],
                        data[w, h],
                        data[w + 1, h],
                    )

                )

            return (
                (
                    data[w - 1, h - 1],
                    data[w, h - 1],
                    data[w + 1, h - 1],
                ),
                (
                    data[w - 1, h],
                    data[w, h],
                    data[w + 1, h],
                ),
                (
                    data[w - 1, h + 1,],
                    data[w, h + 1],
                    data[w + 1, h + 1],
                ),

            )

        data = [
            self.transform_pixel(get_pixels(w, h))
            for h in range(height)
            for w in range(width)

        ]
        image.putdata(data)


class SquareTransform:
    R = 1

    def get_matrix_of_pixel(self, data: np.ndarray, x: int, y: int, r: int) -> np.ndarray | int:
        Y = len(data)
        X = len(data[0])

        if x - r < 0 or y - r < 0 or x + r > X or y + r > Y:
            return None
        ret = np.array(tuple(
            data[max(0, min(_y + y, Y - 1))][max(0, min(_x + x, X - 1))]
            for _y in range(-r, r + 1)
            for _x in range(-r, r + 1)
        ))

        if ret.ndim:
            ret = list(ret)

        return ret

    @abstractmethod
    def transform(self, matrix: np.ndarray):
        pass

    def apply(self, img: PIL.Image.Image):
        data = ImageWrapper(img).get_access_matrix
        X = len(data[0])
        new_image = PIL.Image.new("RGB", (data.shape[0], data.shape[1]))
        # new_img_data = [[0,0,0]]*(len(data)*len(data[0]))
        for _y, y in enumerate(data):
            for _x, x in enumerate(y):
                new_pixel = self.get_matrix_of_pixel(data, x=_x, y=_y, r=self.R)
                if new_pixel is not None:
                    new_pixel = self.transform(new_pixel)
                    if new_pixel.ndim > 0:
                        new_pixel = tuple(new_pixel)
                    else:
                        new_pixel = (new_pixel,) * 3
                    # new_img_data[X*(int(_y)-self.R)+(int(_x)-self.R)] = new_pixel
                    new_image.putpixel((_x,_y),new_pixel)
                # else:
                #     print(end="x")
                else:
                    new_image.putpixel((_x, _y), 0 if data.ndim == 2 else (0, 0, 0))
        #
        # new_image.putdata(data= new_img_data)

        new_image.show()
        return new_image


class Erosion(SquareTransform):

    def transform(self, matrix: np.ndarray):
        # return np.array([0,0,0])
        return np.min(matrix, axis=(0, 1))


class Dilatation(SquareTransform):

    def transform(self, matrix: np.ndarray):
        return np.max(matrix, axis=(0, 1))


class Opening(SquareTransform):

    def apply(self, img: PIL.Image.Image):
        return Dilatation().apply(Erosion().apply(img))


class Closing(SquareTransform):
    def apply(self, img: PIL.Image.Image):
        return Erosion().apply(Dilatation().apply(img))


class MorphologySettingsTopLevel(tk.Toplevel):

    def __init__(self, master: MainWindow) -> None:
        super().__init__(master=master)

        self.master: MainWindow = master
        self.entry_value: tk.Entry

        self._row = 0
        self._init_button_array()

    @property
    def row(self):
        self._row += 1
        return self._row

    def _init_button_array(self):
        self.entry_value: tk.Entry = tk.Entry(self, width=100)
        self.entry_value.grid(row=self.row, column=0, sticky='nesw')

        self.add_button(Erosion, "Erosion")
        self.add_button(Dilatation, "Dilatation")
        self.add_button(Opening, "Opening")
        self.add_button(Closing, "Closing")

    def add_button(self, command, label: str):
        button: tk.Button = tk.Button(self,
                                      text=label,
                                      width=WIDTH_OF_BUTTONS,
                                      command=self.get_command_square_transform(command))
        button.grid(row=self.row, column=0, sticky='nesw')
        return button

    def get_command_square_transform(self, name_of_tool: type(SquareTransform)) -> Callable[[Any], Any]:
        return lambda *args, **kwargs: (

            self.master.redraw(
                self.master.set_image_from_pixels(
                    name_of_tool().apply(self.master.image_from_pixels)
                )
            )
        )

    # def get_command_filter_transformation(self, name_of_tool: type(ThreeXThreeTransformation)) -> Callable[[Any], Any]:
    #     return lambda *args, **kwargs: (
    #         name_of_tool()
    #         .apply(self.master, self.master.image_from_pixels),
    #         self.master.redraw(self.master.image_from_pixels)
    #     )


class PointTransformation:
    @abstractmethod
    def transform_pixel(self, pixel: tuple[int, int, int], value: tuple[float, float, float]) -> tuple[int, int, int]:
        pass

    def apply(self, master, image: PIL.Image.Image, raw_value: str):
        try:
            value: tuple[float, float, float] | tuple[float] | Any = raw_value.split(',')
            value = tuple(float(x) for x in value)
            assert len(value) in (1, 3)
        except Exception as ex:
            raise ex
        if len(value) == 1:
            value *= 3
        loaded = image.load()
        for x in range(image.width):
            for y in range(image.height):
                loaded[x, y] = self.transform_pixel(loaded[x, y], value)


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


if __name__ == '__main__':
    MainWindow.run()
