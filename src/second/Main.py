import tkinter as tk
from tkinter import filedialog, messagebox, HORIZONTAL

import PIL.ImageTk
from PIL import ImageTk
from PIL.Image import Image, CUBIC, ANTIALIAS, NEAREST

from src.second.formats.JPEGParser import JPEGParser
from src.second.formats.ppm import PPM


class MainWindow(tk.Tk):
    def __init__(self, ) -> None:
        super().__init__("main screen")
        self._buttons_array: tk.Frame | None = None
        self.canvas: tk.Canvas | None = None

        self._buttons_array_write_scale_zoom: tk.Scale

        self.image_from_pixels: PIL.Image.Image | None = None
        self.image_tk_from_raw: PIL.PhotoImage | None = None
        self.canvas_drawn_image_id: int | None = None

        self.zoomcycle = 0
        self.zimg_id = None

        self.WIDTH = 640
        self.HEIGHT = 480

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

        self.bind("<MouseWheel>", self.zoomer)
        self.canvas.bind("<Motion>", self.crop)

        return self

    def zoomer(self, event):
        if event.delta > 0:
            if self.zoomcycle < 5:
                self.zoomcycle += 1
        elif event.delta < 0:
            if self.zoomcycle > 0:
                self.zoomcycle -= 1
        self.crop(event)

    def update_label(self, event, image_to_be_drawn):
        # self.image_tk_from_raw.
        x, y = cords = event.x, event.y
        try:
            if image_to_be_drawn:
                self._buttons_array_label_pixel_value_text_variable.set(
                    f'{event.x} {event.y}\t: {image_to_be_drawn.getpixel(cords)}')
            else:
                raise Exception()
        except Exception:
            self._buttons_array_label_pixel_value_text_variable.set(
                f'--- ---\t: (--, --, --))')

    def crop(self, event):
        img_to_be_drawn = None
        if self.canvas_drawn_image_id:
            self.canvas.delete(self.canvas_drawn_image_id)
            # if self.zoomcycle != 0:
            tmp = None
            x, y = event.x, event.y
            if self.zoomcycle == 1:
                tmp = self.image_from_pixels.crop((x - 45, y - 30, x + 45, y + 30))
            elif self.zoomcycle == 2:
                tmp = self.image_from_pixels.crop((x - 30, y - 20, x + 30, y + 20))
            elif self.zoomcycle == 3:
                tmp = self.image_from_pixels.crop((x - 15, y - 10, x + 15, y + 10))
            elif self.zoomcycle == 4:
                tmp = self.image_from_pixels.crop((x - 6, y - 4, x + 6, y + 4))
            elif self.zoomcycle == 5:
                tmp = self.image_from_pixels.crop((x - 3, y - 2, x + 3, y + 2))
            elif self.zoomcycle == 0:
                tmp = self.image_from_pixels
            size = (self.WIDTH, self.HEIGHT)
            if self.zoomcycle != 0:
                img_to_be_drawn = tmp.resize(size, resample=NEAREST)

                self.image_tk_from_raw = ImageTk.PhotoImage(img_to_be_drawn)
                self.canvas_drawn_image_id = self.canvas.create_image(event.x, event.y, image=self.image_tk_from_raw)
            else:
                img_to_be_drawn = tmp
                self.image_tk_from_raw = ImageTk.PhotoImage(img_to_be_drawn)
                self.canvas_drawn_image_id = self.canvas.create_image((self.image_from_pixels.width + 5) // 2,
                                                                      (self.image_from_pixels.height + 5) // 2,
                                                                      image=self.image_tk_from_raw)

            self.update_label(event, self.image_from_pixels)

    def _initialize_array_button(self):
        self._buttons_array_read_file_button_ppm = tk.Button(master=self._buttons_array,
                                                             text="Read from file PPM",
                                                             command=self.__command_read_from_file_ppm)
        self._buttons_array_read_file_button_ppm.pack(side=tk.LEFT)

        self._buttons_array_read_file_button_jpeg = tk.Button(master=self._buttons_array,
                                                              text="Read from file JPEG",
                                                              command=self.__command_read_from_file_jpg)
        self._buttons_array_read_file_button_jpeg.pack(side=tk.LEFT)

        self._buttons_array_write_file_button = tk.Button(master=self._buttons_array,
                                                          text="Write to file",
                                                          command=self.__command_write_to_file)
        self._buttons_array_write_file_button.pack(side=tk.LEFT)

        self._buttons_array_label_pixel_value_text_variable = tk.StringVar()
        self._buttons_array_label_pixel_value = tk.Label(self._buttons_array,
                                                         textvariable=self._buttons_array_label_pixel_value_text_variable)
        self._buttons_array_label_pixel_value.pack(side=tk.LEFT)

    def __command_read_from_file_ppm(self):
        file = filedialog.askopenfilename(filetypes=(
            ("PPM", "*.ppm"),
            ("All Files", "*.*"),
        ))

        if file is not None:
            self.parse_image_ppm(file)
        else:
            messagebox.showinfo("Nie wybrano pliku")

    def __command_read_from_file_jpg(self):
        file = filedialog.askopenfilename(filetypes=(
            ("JPG", "*.jpg"),
            ("JPEG", "*.jpeg"),
            ("All Files", "*.*"),
        ))

        if file is not None:
            self.parse_image_jpg(file)
        else:
            messagebox.showinfo("Nie wybrano pliku")

    def __command_write_to_file(self):
        new_window = tk.Toplevel(self)
        new_window.title(
            "Save file"
        )
        new_window.label_about_compression = tk.Label(new_window, text="Set compression params:")
        new_window.label_about_compression.pack()

        new_window.scale_compression = tk.Scale(new_window, from_= 0, to=100, orient=HORIZONTAL)
        new_window.scale_compression.set(95)
        new_window.scale_compression.pack()

        new_window.label_about_subsampling = tk.Label(new_window, text="Set subsampling params:")
        new_window.label_about_subsampling.pack()

        new_window.scale_subsampling = tk.Scale(new_window, from_= 0, to=100, orient=HORIZONTAL)
        new_window.scale_subsampling.pack()
        new_window.scale_subsampling.set(0)
        def submit_handler(*args,**kwargs):
            sub = new_window.scale_subsampling.get()
            com = new_window.scale_compression.get()

            filename = filedialog.asksaveasfilename(filetypes=(( 'JPEG','*.jpg',),))
            if filename and self.image_from_pixels:
                if filename[-4:] != '.jpg' and filename[-5:] != '.jpeg':
                    filename = filename+'.jpg'
                self.image_from_pixels.save(filename, quality=com, subsampling=sub)

        new_window.button_submit = tk.Button(new_window, text='Submit', command= lambda *args,**kwargs: submit_handler(*args,**kwargs) )
        new_window.button_submit.pack()


    def parse_image_ppm(self, filename: str):
        PPM().read_from_file(filename, self)

    def parse_image_jpg(self, filename: str):
        JPEGParser().read_from_file(filename, self)

    @staticmethod
    def run():
        MainWindow().initialize_view().mainloop()


if __name__ == '__main__':
    MainWindow.run()
