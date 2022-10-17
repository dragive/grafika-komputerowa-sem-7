import tkinter as tk
from tkinter import filedialog, messagebox

from src.second.formats.ppm import PPM


class MainWindow(tk.Tk):
    def __init__(self, ) -> None:
        super().__init__("main screen")
        self._buttons_array: tk.Frame | None = None
        self.canvas: tk.Canvas | None = None
        self.canvas_drawn_image = None
        self.canvas_drawn_image_obj: tk.PhotoImage | None = None

        self.WIDTH = 640
        self.HEIGHT = 480

    def initialize_view(self) -> "MainWindow":
        self._buttons_array = tk.Frame(master=self)
        self._buttons_array.pack()
        self.canvas = tk.Canvas(self, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()
        self._initialize_array_button()
        return self

    def _initialize_array_button(self):
        self._buttons_array_read_file_button = tk.Button(master=self._buttons_array,
                                                         text="Read from file",
                                                         command=self.__command_read_from_file)
        self._buttons_array_read_file_button.pack(side=tk.LEFT)

        self._buttons_array_write_file_button = tk.Button(master=self._buttons_array,
                                                          text="Write to file",
                                                          command=self.__command_write_to_file)
        self._buttons_array_write_file_button.pack(side=tk.LEFT)

    def __command_read_from_file(self):
        file = filedialog.askopenfilename(filetypes=(
            ("PPM", "*.ppm"),
            ("JPG", "*.jpg"),
            ("JPEG", "*.jpeg"),
            ("All Files", "*.*"),
        ))

        if file is not None:
            self.parse_image_ppm(file)
        else:
            messagebox.showinfo("Nie wybrano pliku")

    def __command_write_to_file(self):
        pass

    def parse_image_ppm(self, filename: str):
        PPM().read_from_file(filename, self)

    @staticmethod
    def run():
        MainWindow().initialize_view().mainloop()


if __name__ == '__main__':
    MainWindow.run()
