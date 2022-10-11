import tkinter as tk


def onclick(event):

    item = cv.find_closest(event.x, event.y)
    if 'rect' in cv.gettags(item):
        current_color = cv.itemcget(item, 'fill')

        if current_color == 'black':
            cv.itemconfig(item, fill='white')
        else:
            cv.itemconfig(item, fill='black')



root = tk.Tk()
cv = tk.Canvas(root, height=800, width=800)
cv.pack()
cv.bind('<Button-first>', onclick)

id_a = cv.create_line(50, 50, 60, 60, width=2)
id_b = cv.create_rectangle(80, 80, 100, 100, tags=('rect'))

root.mainloop()

if __name__ == '__main__':
    pass