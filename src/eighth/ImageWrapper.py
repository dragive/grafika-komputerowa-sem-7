import PIL.Image
import numpy as np


class ImageWrapper:

    def __init__(self, img: PIL.Image.Image) -> None:
        super().__init__()

        self.img: PIL.Image.Image = img
        pass

    def get_rows(self):
        data = list(self.img.getdata())
        new_data = []
        for row_no in range(self.img.height):
            new_data.append(data[row_no * self.img.width:(row_no + 1) * self.img.width])

        return new_data

    @property
    def get_access_matrix(self):
        x = np.array(self.get_rows(),dtype=np.uint32)
        return x
