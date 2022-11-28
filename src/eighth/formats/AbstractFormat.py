import abc


class AbstractFormat(abc.ABC):

    @staticmethod
    def read_from_file(self, name: str, *args, **kwargs):
        """Abstract method for reading from files using parser specific to some format"""
        pass

    @staticmethod
    def write_to_file(self, name: str, *args, **kwargs):
        """Abstract method for writing to file using parser specific to some format"""
        pass


class Pixel:
    def __init__(self, red: int, green: int, blue: int, scale: int | None = None):
        self.red = red
        self.green = green
        self.blue = blue
        self.scale = scale

    @staticmethod
    def __to_hex(value: int):
        ret = hex(value)[2:]
        if len(ret) == 1:
            return '0' + ret
        return ret

    @property
    def to_RGB(self):
        scale = 255 / self.scale
        return f'#{self.__to_hex(int(self.red * scale))}{self.__to_hex(int(self.green * scale))}{self.__to_hex(int(self.blue * scale))}'

    @property
    def to_tuple(self):
        scale = 255 / self.scale
        return int(self.red * scale), int(self.green * scale), int(self.blue * scale)
