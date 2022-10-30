from PIL import Image, ImageTk


class JPEGParser:
    @staticmethod
    def read_from_file(name: str, main_window: 'MainWindow', *args, **kwargs):

        if name:
            main_window.image_from_pixels = Image.open(name)
            main_window.image_tk_from_raw = ImageTk.PhotoImage(main_window.image_from_pixels)
            main_window.canvas_drawn_image_id = main_window.canvas.create_image(
                (main_window.image_tk_from_raw.width() + 5) // 2,
                (main_window.image_tk_from_raw.height() + 5) // 2,
                image=main_window.image_tk_from_raw)

            if main_window.WIDTH_OF_BUTTONS < main_window.image_from_pixels.width:
                main_window.WIDTH_OF_BUTTONS = main_window.image_from_pixels.width
                main_window.canvas.config(width=main_window.image_from_pixels.width)
            if main_window.HEIGHT < main_window.image_from_pixels.height:
                main_window.HEIGHT = main_window.image_from_pixels.height
                main_window.canvas.config(height=main_window.image_from_pixels.height)