from abc import ABC
from tkinter import PhotoImage

from src.second.formats.AbstractFormat import AbstractFormat, Pixel


def de_hex(data: bytes):
    try:
        return int(data.hex(), 16)
    except ValueError:
        return 0


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
    def read_data(file: bytes | None = None, scale: int = 255):
        assert file is not None
        parsed_file = b'\n'.join(file)
        pixels = []
        for index in range(0, len(parsed_file), 3):
            pixels.append(Pixel(parsed_file[index], parsed_file[index + 1],
                                parsed_file[index + 2], scale))
        return pixels
        pass


class PPM(AbstractFormat):
    @staticmethod
    def __draw(main_window: 'MainWindow',
               pixels: list[Pixel],
               data_width: int,
               data_height: int):
        for x in range(data_width):
            for y in range(data_height):
                main_window.canvas_drawn_image_obj.put(pixels[y * data_width + x].to_RGB, (x, y))

    @staticmethod
    def read_from_file(name: str, main_window: 'MainWindow', *args, **kwargs):
        pixels = []
        t: str
        height: int | None = None
        width: int | None = None
        pixels: list[Pixel]
        with open(name, 'rb') as file:
            read_lines = file.readline()
            if read_lines[:2] == b'P3':
                t = 'P3'

            elif read_lines[:2] == b'P6':
                t = 'P6'

        if t == 'P3':
            height, pixels, width = PPM.read_p3(name)
        elif t == 'P6':
            height, pixels, width = PPM.read_p6(name)

        if t in ('P3', 'P6'):
            WIDTH = main_window.WIDTH
            HEIGHT = main_window.HEIGHT
            main_window.canvas_drawn_image_obj = PhotoImage(width=width, height=height)
            _scale = min(HEIGHT / height, WIDTH / width)
            if _scale < 1:
                main_window.WIDTH = int(main_window.WIDTH / _scale + 2)
                main_window.HEIGHT = int(main_window.HEIGHT / _scale + 2)

                main_window.canvas.config(width=main_window.WIDTH, height=main_window.HEIGHT, )
            _scale = max(1, _scale)

            PPM.__draw(main_window,
                       # (WIDTH, HEIGHT),
                       pixels,
                       width,
                       height)
            print('draw')
            main_window.canvas_drawn_image_obj = main_window.canvas_drawn_image_obj.zoom(_scale)  # todo fixme
            print('zoom')
            main_window.canvas_drawn_image = main_window.canvas.create_image(
                ((width * _scale + 1) // 2, (1 + height * _scale) // 2),
                image=main_window.canvas_drawn_image_obj,
                state='normal')
            print('end')

    @staticmethod
    def read_p6(name):
        read_lines: list[bytes] | bytes
        with open(name, 'rb') as file:
            read_lines = file.read()
        print('read')
        read_lines = read_lines.split(b'\n')
        print('split')
        read_lines = read_lines[1:]
        width, height, scale, read_lines = PPM.__read_params(read_lines)
        width = int(width)
        height = int(height)
        scale = int(scale)
        print('params')
        pixels = BinaryPpm.read_data(read_lines, scale)
        print('pixels')
        return height, pixels, width

    @staticmethod
    def read_p3(name):
        read_lines: list[str] | str

        with open(name, 'r') as file:
            read_lines = file.read()
        read_lines = read_lines.split('\n')
        read_lines = [line.split('#')[0] for line in read_lines]
        read_lines = read_lines[1:]
        width, height, scale, read_lines = PPM.__read_params(read_lines)
        width = int(width)
        height = int(height)
        scale = int(scale)
        pixels = AsciiPpm.read_data(read_lines, scale)
        return height, pixels, width

    @staticmethod
    def __read_params(file: list[str] | list[bytes]) -> list[list[str]] | list[list[bytes]]:
        last = 0
        ret = []
        for i, v in enumerate(file):
            last = i
            l: str | bytes
            if isinstance(v, bytes):
                l = v.split(b'#')[0]
            else:
                l = v.split('#')[0]
            d = l.split()
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
