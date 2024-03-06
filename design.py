from tkinter import *
root=Tk()
root.geometry("1000x1000")
label=Label(root, text='Welcome')
label.pack()
label_vest=Label(root).pack()


canvas = Canvas(root, width=1000, height=1000)
canvas.pack()

def get_mouse_position(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))
canvas.bind("<Motion>", get_mouse_position)

