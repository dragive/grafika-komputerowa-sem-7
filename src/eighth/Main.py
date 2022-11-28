import tkinter as tk
from abc import abstractmethod
from tkinter import filedialog, messagebox, HORIZONTAL
from typing import Tuple

import PIL.ImageTk
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


class MorphologySettingsTopLevel(tk.Toplevel):

    def __init__(self, master: MainWindow) -> None:
        super().__init__(master=master)

        self.master: MainWindow = master
        self.entry_value: tk.Entry

        self._row = 0
        self.wrapper = ImageWrapper(master.image_from_pixels)
        x = self.wrapper.get_access_matrix
        self._init_button_array()

    @property
    def row(self):
        self._row += 1
        return self._row

    def _init_button_array(self):
        self.entry_value: tk.Entry = tk.Entry(self, width=100)
        self.entry_value.grid(row=self.row, column=0, sticky='nesw')

        self.add_button(lambda *args, **kwargs: print("11111"), "Test")

    def add_button(self, command, label: str):
        button: tk.Button = tk.Button(self,
                                      text=label,
                                      width=WIDTH_OF_BUTTONS,
                                      command=command)
        button.grid(row=self.row, column=0, sticky='nesw')
        return button

    # def get_command_pixel_transformation(self, name_of_tool: type(PointTransformation)) -> Callable[[Any], Any]:
    #     return lambda *args, **kwargs: (
    #         name_of_tool()
    #         .apply(self.master, self.master.image_from_pixels, self.entry_value.get()),
    #         self.master.redraw(self.master.image_from_pixels)
    #     )
    #
    # def get_command_filter_transformation(self, name_of_tool: type(ThreeXThreeTransformation)) -> Callable[[Any], Any]:
    #     return lambda *args, **kwargs: (
    #         name_of_tool()
    #         .apply(self.master, self.master.image_from_pixels),
    #         self.master.redraw(self.master.image_from_pixels)
    #     )


if __name__ == '__main__':
    MainWindow.run()
