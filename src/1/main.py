import enum
import tkinter as tk


class Tools(enum.Enum):
    PICK = "PICK"
    LINE = "LINE"
    OVAL = "OVAL"
    SQUARE = "SQUARE"


class MainWindow:
    def __init__(self):
        self.main = tk.Tk()

        self.canvas = tk.Canvas(self.main, bg="white", height=300, width=400)
        self.canvas.grid(row=1, column=1)

        self.side_settings = tk.Frame(self.main)
        self.side_settings.grid(row=1, column=2)

        self.tool = Tools.PICK

    def __set_tool(self):
        print(f"{self.tool=}")
        self.side_settings_label_tool_info.config(text=self.tool.value)

    def __set_tool_pick(self):
        self.tool = Tools.PICK
        self.__set_tool()

    def __set_tool_oval(self):
        self.tool = Tools.OVAL
        self.__set_tool()

    def __set_tool_square(self):
        self.tool = Tools.SQUARE
        self.__set_tool()

    def __set_tool_line(self):
        self.tool = Tools.LINE
        self.__set_tool()

    def add_side_settings_contents(self):
        self.side_settings_label_tool_info = tk.Label(self.side_settings,text=self.tool.value)
        self.side_settings_label_tool_info.pack()

        self.side_settings_button_pick = tk.Button(self.side_settings, text="Pick", command=self.__set_tool_pick)
        self.side_settings_button_pick.pack()

        self.side_settings_button_line = tk.Button(self.side_settings, text="Line", command=self.__set_tool_line)
        self.side_settings_button_line.pack()

        self.side_settings_button_oval = tk.Button(self.side_settings, text="Oval", command=self.__set_tool_oval)
        self.side_settings_button_oval.pack()

        self.side_settings_button_square = tk.Button(self.side_settings, text="Square", command=self.__set_tool_square)
        self.side_settings_button_square.pack()

    def run(self):
        self.add_side_settings_contents()
        self.main.mainloop()


def log(*args, **kwargs):
    print(f"{args=}")
    print(f"{kwargs=}")


def main():
    top = tk.Tk()

    C = tk.Canvas(top, bg="white", height=300, width=400)
    button = tk.Button(top, text="123", command=lambda: print("hii"))
    button.pack()
    C.bind("<B1-Motion>", log)
    C.bind("<ButtonRelease-1>", log)
    arc = C.create_line(10, 20, 30, 40, fill="black")

    C.pack()
    top.mainloop()


if __name__ == '__main__':
    MainWindow().run()
