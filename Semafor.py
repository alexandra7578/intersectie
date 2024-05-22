import tkinter as tk
from tkinter import Canvas
class Semafor:
    def __init__(self, root, x, y, initial_color='red'):
        self.root = root
        self.x = x
        self.y = y
        self.canvas = Canvas(root, width=60, height=180, bg='white')
        self.canvas.place(x=x, y=y)
        self.colors = {'red': 'gray', 'yellow': 'gray', 'green': 'gray'}
        self.colors[initial_color] = initial_color
        self.draw()

    def draw(self):
        self.canvas.create_oval(10, 10, 50, 50, fill=self.colors['red'], outline='black')
        self.canvas.create_oval(10, 65, 50, 105, fill=self.colors['yellow'], outline='black')
        self.canvas.create_oval(10, 120, 50, 160, fill=self.colors['green'], outline='black')

    def set_color(self, color):
        if color in self.colors:
            self.colors = {k: 'gray' for k in self.colors}  # Reset all to gray
            self.colors[color] = color  # Set the specified color
            self.draw()