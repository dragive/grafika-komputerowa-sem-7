from abc import ABC
from tkinter import PhotoImage
from typing import BinaryIO

from src.second.formats.AbstractFormat import AbstractFormat, Pixel


class AsciiPpm(ABC):
    @staticmethod
    def read_data(file: str | None = None, scale: int = 255):
        assert file is not None

        parsed_file = []
        for i in file:
            ii = i
            try:
                index = ii.index('#')
                ii = i[:index]
            except ValueError:
                pass
            finally:
                parsed_file.append(ii)

        parsed_file = [int(i) for f in parsed_file for i in f.split()]
        assert len(parsed_file) % 3 == 0
        pixels = []
        for index in range(0, len(parsed_file), 3):
            pixels.append(Pixel(parsed_file[index], parsed_file[index + 1], parsed_file[index + 2], scale))
        return pixels


class BinaryPpm(ABC):
    @staticmethod
    def read_data(file):
        pass


class PPM(AbstractFormat):
    @staticmethod
    def __draw(main_window: 'MainWindow',
               # size: tuple[int, int],
               pixels: list[Pixel],
               data_width: int,
               data_height: int):
        # pixel_size = size[0] // max(data_width, data_height)
        pixel_size = 1  # max(pixel_size, 1)
        for x in range(data_width):
            xx = x // pixel_size
            for y in range(data_height):
                yy = y // pixel_size
                main_window.canvas_drawn_image_obj.put(pixels[xx * data_width + yy].to_RGB,
                                                       (x, y))  # pixels[xx * data_width + yy].to_RGB

    @staticmethod
    def read_from_file(name: str, main_window: 'MainWindow', *args, **kwargs):
        with open(name, 'r') as file:
            read_lines = file.read()
            read_lines = read_lines.split('\n')
            read_lines = [line.split('#')[0] for line in read_lines]
            header = read_lines[0][:3]
            read_lines = read_lines[1:]
            width, height, scale, read_lines = PPM.__read_params(read_lines)
            width = int(width)
            height = int(height)
            scale = int(scale)
            pixels = []
            if header == 'P3':
                pixels = AsciiPpm.read_data(read_lines, scale)
            elif header == 'P6':
                BinaryIO.read_data()
        WIDTH = main_window.WIDTH
        HEIGHT = main_window.HEIGHT
        main_window.canvas_drawn_image_obj = PhotoImage(width=width, height=height)
        _scale = int(max(1, min(HEIGHT / height, WIDTH / width)))
        # _scale = 10
        PPM.__draw(main_window,
                   # (WIDTH, HEIGHT),
                   pixels,
                   width,
                   height)
        main_window.canvas_drawn_image_obj = main_window.canvas_drawn_image_obj.zoom(_scale)  # todo fixme
        main_window.canvas_drawn_image = main_window.canvas.create_image(
            ((width * _scale + 1) // 2, (1 + height * _scale) // 2),
            image=main_window.canvas_drawn_image_obj,
            state='normal')

    @staticmethod
    def __read_params(file: list[str]) -> list[list[str]]:
        last = 0
        ret = []
        for i, v in enumerate(file):
            last = i
            d = v.split()
            if len(d) > 0:
                ret += d
            if len(ret) >= 3:
                break
        if len(ret) > 3:
            raise ValueError()

        ret.append(file[last + 1:])
        return ret

    @staticmethod
    def write_to_file(name: str, *args, **kwargs):
        pass


if __name__ == '__main__':
    AsciiPpm.read_data()
