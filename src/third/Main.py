import tkinter as tk


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.button_picker = tk.Button(self, text="Picker", command=self.run_picker)
        self.button_cube = tk.Button(self, text="Cube", command=self.run_cube)

        self.button_picker.pack()
        self.button_cube.pack()
    def run_picker(self):
        import colorPicker.pickMe
        colorPicker.pickMe.MainWindow().mainloop()

    def run_cube(self):
        import cube.pygameTest
        cube.pygameTest.App()

if __name__ == '__main__':
    MainWindow().mainloop()
