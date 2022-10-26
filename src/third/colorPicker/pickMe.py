import tkinter as tk
from tkinter import HORIZONTAL
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageTk
from tkinter import colorchooser


class MainWindow(tk.Tk):

    def __init__(self) -> None:
        super().__init__()

        self.WIDTH = 255
        self.HEIGHT = 255
        # self.canvas_image_picker = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT)
        # self.canvas_image_picker.grid(row=1, column=0)
        # self.COLOR_FROM = 0
        # self.COLOR_TO = len(self.colors) - 1
        # self.color_scale = tk.Scale(self,
        #                             from_=self.COLOR_FROM,
        #                             to=self.COLOR_TO,
        #                             orient=HORIZONTAL,
        #                             command=self.generate_new_pixels)
        # self.color_scale.grid(row=2, column=0)
        # self.img: Image.Image|None = None
        # self.img_tk = None
        # self.array = None
        # self.canvas_img = None
        #
        # self.generate_new_pixels()
        # self.canvas_image_picker.bind('<Button-1>', self.canvas_click_handler)
        self.initial_color = (0, 0, 0)
        self.lock_rgb = False
        self.lock_cmyk = False
        self.color_indicator = tk.Label(self, bg="#000000", width=40, height=5)
        self.color_indicator.grid(row=1, column=1, columnspan=2)
        self.color_label_text_var_rgb = tk.StringVar()
        self.color_label_text_var_rgb.set(self.format_to_rgb((0, 0, 0)))
        self.color_label_text_var_cmyk = tk.StringVar()
        self.color_label_text_var_cmyk.set(self.format_to_cmyk(self.convert_from_rgb((0, 0, 0))))
        self.color_label_rgb = tk.Entry(self, textvariable=self.color_label_text_var_rgb, width=40)
        self.color_label_rgb.grid(row=2, column=1, columnspan=2)
        self.color_label_cmyk = tk.Entry(self, textvariable=self.color_label_text_var_cmyk, width=40)
        self.color_label_cmyk.grid(row=3, column=1, columnspan=2)
        self.color_rgb_submit = tk.Button(self, text="Submit or convert rgb", command=self.parse_from_text_var_rgb)
        self.color_rgb_submit.grid(row=4, column=1)
        self.color_rgb_submit = tk.Button(self, text="Submit or convert cmyk", command=self.parse_from_text_var_cmyk)
        self.color_rgb_submit.grid(row=4, column=2)

        self.scale_red = tk.Scale(self, from_=0,label="R", to=255, orient=HORIZONTAL, command=self.update_rgb)
        self.scale_green = tk.Scale(self, from_=0,label="G", to=255, orient=HORIZONTAL, command=self.update_rgb)
        self.scale_blue = tk.Scale(self, from_=0,label="B", to=255, orient=HORIZONTAL, command=self.update_rgb)

        self.scale_red.grid(row=5, column=1)
        self.scale_green.grid(row=6, column=1)
        self.scale_blue.grid(row=7, column=1)

        self.scale_cyan_cmyk = tk.Scale(self,label="C", from_=0, to=255, showvalue=0, orient=HORIZONTAL, command=self.update_cmyk)
        self.scale_magenta_cmyk = tk.Scale(self,label="M", from_=0, to=255, showvalue=0, orient=HORIZONTAL, command=self.update_cmyk)
        self.scale_yellow_cmyk = tk.Scale(self,label="Y", from_=0, to=255, showvalue=0, orient=HORIZONTAL, command=self.update_cmyk)
        self.scale_black_cmyk = tk.Scale(self,label="K", from_=0, to=255, showvalue=0, orient=HORIZONTAL, command=self.update_cmyk)

        self.scale_cyan_cmyk.grid(row=5, column=2)
        self.scale_magenta_cmyk.grid(row=6, column=2)
        self.scale_yellow_cmyk.grid(row=7, column=2)
        self.scale_black_cmyk.grid(row=8, column=2)

        self.palete = tk.Button(self, text="choose from palete",command=self._palete)
        self.palete.grid(column=1,row=9,columnspan=2)

    def _palete(self):
        rgb,hex = tk.colorchooser.askcolor()
        self.update_rgb_scales(rgb)
    def update_cmyk(self, *args):

        cyan = self.scale_cyan_cmyk.get() / 255
        magenta = self.scale_magenta_cmyk.get() / 255
        yellow = self.scale_yellow_cmyk.get() / 255
        black = self.scale_black_cmyk.get() / 255
        self.color_label_text_var_cmyk.set(self.format_to_cmyk((cyan, magenta, yellow, black)))
        self.parse_from_text_var_cmyk()

    def update_rgb(self, *args):

        red = self.scale_red.get()
        green = self.scale_green.get()
        blue = self.scale_blue.get()

        self.color_label_text_var_rgb.set(self.format_to_rgb((red, green, blue)))
        self.parse_from_text_var_rgb()

    def parse_from_text_var_rgb(self):
        if self.lock_rgb:
            return
        self.lock_rgb = True
        try:
            val = self.color_label_text_var_rgb.get()
            assert val[:3].lower() == 'rgb'
            val = val[4:-1]
            val = val.split(',')
            val = tuple([int(i) for i in val])
            assert len(val) == 3
            for i in val:
                assert i >= 0
                assert i < 256
            self.initial_color = val
            # self.update_rgb_scales(self.initial_color)
            self.update_cmyk_scales((x*255 for x in self.convert_from_rgb(self.initial_color)))
            self.color_label_text_var_cmyk.set(self.format_to_cmyk(self.convert_from_rgb(self.initial_color)))
        except Exception as e:
            messagebox.showerror("error while parsing data!")
            raise e
        finally:
            self.paint()
            self.lock_rgb = False

    def parse_from_text_var_cmyk(self):
        if self.lock_cmyk:
            return
        self.lock_cmyk = True
        try:
            val = self.color_label_text_var_cmyk.get()
            assert val[:4].lower() == 'cmyk'
            val = val[5:-1]
            val = val.split(',')
            val = tuple([float(i) for i in val])
            assert len(val) == 4
            for i in val:
                assert i >= 0
                assert i <= 1
                self.initial_color = self.convert_from_cmyk(val)
            self.update_rgb_scales(self.initial_color)
            # self.update_cmyk_scales(val)
        except Exception as e:
            messagebox.showerror("error while parsing data!")
            raise e
        finally:
            self.paint()
            self.lock_cmyk = False

    def convert_from_cmyk(self, data):
        c, m, y, k = data
        return (
            int(255 * (1 - c) * (1 - k)),
            int(255 * (1 - m) * (1 - k)),
            int(255 * (1 - y) * (1 - k)),
        )

    def update_rgb_scales(self, rgb):
        r, g, b = rgb
        self.scale_red.set(r)
        self.scale_blue.set(b)
        self.scale_green.set(g)

    def update_cmyk_scales(self, cmyk):
        c, m, y, k = cmyk
        self.scale_cyan_cmyk.set(c)
        self.scale_magenta_cmyk.set(m)
        self.scale_yellow_cmyk.set(y)
        self.scale_black_cmyk.set(k)

    def convert_from_rgb(self, data):
        r, g, b = data
        r /= 255
        g /= 255
        b /= 255

        k = 1 - max(r, max(g, b))

        if k == 1 and r == 0 and g == 0 and b == 0:
            return (0,0,0,1)
        return (

            (1 - r - k) / (1 - k),
            (1 - g - k) / (1 - k),
            (1 - b - k) / (1 - k),
            k,
        )

    def paint(self):
        color_hex = '#' + ''.join(self._to_hex(i) for i in self.initial_color)
        self.color_indicator.config(bg=color_hex)

    def _to_hex(self, data):
        ret = hex(data)[2:]
        if len(ret) == 1:
            return '0' + ret
        return ret

    def canvas_click_handler(self, *args, **kwargs):
        x = args[0].x
        y = args[0].y

        self.color_label_text_var_rgb.set(self.format_to_rgb(self.img.getpixel((x, y))))

    def format_to_rgb(self, data):
        return "RGB" + str(tuple(data))

    def format_to_cmyk(self, data):
        return "CMYK" + str(tuple(data))

    @property
    def colors(self, cache=[]):
        if not cache:
            cache = [np.array((255, i, 0), dtype=np.uint8) for i in range(0, 255)] \
                    + [np.array((0, 255, i), dtype=np.uint8) for i in range(0, 255)] \
                    + [np.array((i, 0, 255,), dtype=np.uint8) for i in range(0, 256)]

        return cache

    def generate_new_pixels(self, *args):
        color_base = self.colors[self.color_scale.get()]
        w = self.WIDTH
        h = self.HEIGHT
        self.array = np.array(
            [
                [
                    # (color_base*i/w) *
                    _calculate_saturation((color_base), x / h) * i / w
                    for i in range(0, w + 1)
                    # for value in color_base
                ]
                for x in range(0, h)
            ], dtype=np.uint8)
        self.img = Image.fromarray(self.array, "RGB")
        self.img_tk = ImageTk.PhotoImage(image=self.img)
        if not self.canvas_img:
            self.canvas_img = self.canvas_image_picker.create_image(127, 127, image=self.img_tk)
        else:
            self.canvas_image_picker.itemconfig(self.canvas_img, image=self.img_tk)


def _calculate_saturation(pixel, saturation):
    delta = np.array([255., 255., 255.])

    delta -= pixel
    delta *= saturation

    ret = pixel + delta
    return ret
    pass


if __name__ == '__main__':
    MainWindow().mainloop()
