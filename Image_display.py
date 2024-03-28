import time
import tkinter
from tkinter import *
import os
import pandas as pd
from PIL import Image, ImageTk, ImageDraw, ImageFont
from os import walk
import re
import time
from time import sleep
import cv2
import pandas as pd
from ultralytics import YOLO
import numpy as np
import torch
from tracker import *
from Image_tracker import *
from Boundin_Boxes import *
_nsre = re.compile('([0-9]+)')
model = YOLO("yolov8n.pt")
my_file=open("model.txt", "r")
data=my_file.read()
class_list=data.split("\n")
BLUE_LINE = [(980, 780), (1225, 780)]
GREEN_LINE = [(980, 800), (1270, 800)]
RED_LINE = [(980, 820), (1310, 820)]

PINK_LINE = [(600, 860), (910, 860)]
YELLOW_LINE = [(580, 880), (910, 880)]
ORANGE_LINE = [(560, 900), (910, 900)]
class ImageDisplay:
    def __init__(self, root, pathtofiles, bounding_box_extractor):
        self.root = root
        self.pathtofiles = pathtofiles
        self.image_label = tkinter.Label(root)
        self.image_label.pack()
        self.filenames = self.get_filenames()
        self.current_index = 0
        self.bounding_box_extractor = bounding_box_extractor

    def natural_sort_key(self, s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split(_nsre, s)]

    def get_filenames(self):
        filenames = []

        for filename in os.listdir(self.pathtofiles):  # Utilizați self.pathtofiles direct
            if filename.endswith('.JPEG') or filename.endswith('.png'):
                filenames.append(os.path.join(self.pathtofiles, filename))
        filenames.sort(key=self.natural_sort_key)

        return filenames

    def display_image(self, filename):
        image = Image.open(filename)
        image = image.resize((350, 200))  # Redimensionare la o dimensiune dorită
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def draw_count(self, img, count):
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', 10)
        draw.text((0, 0), str(count), font=font, fill=(255, 255, 0))
        del draw

    def display_vehicles(self, img, tracked_vehicles):
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', 10)
        image_width, image_height = img.size

        cars_between_lines = 0

        # Coordonatele pentru linia orizontală albastră
        y_blue = 250
        blue_line = [(30, y_blue), (300, y_blue)]

        # Desenarea liniei albastre
        draw.line(blue_line, fill=(0, 0, 255), width=2)


        for vehicle in tracked_vehicles:
            # Coordonatele colțurilor dreptunghiului care înconjoară vehiculul
            rect_x1, rect_y1, rect_x2, rect_y2 = int(vehicle[0]), int(vehicle[1]), int(vehicle[2]), int(vehicle[3])
            if y_blue < (rect_y1 + rect_y2) / 2:
                cars_between_lines += 1
            # Folosiți metoda din Bounding_Box_Extractor pentru a obține statusul vehiculului
            vehicle_status = self.bounding_box_extractor.get_status(vehicle[4])

            # Desenarea dreptunghiului
            draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], outline=(0, 0, 255))

            # Coordonatele textului pentru a fi centrat în interiorul dreptunghiului
            text_width, text_height = draw.textsize(str(vehicle[4]), font=font)
            text_x = (rect_x1 + rect_x2 - text_width) / 2
            text_y = (rect_y1 + rect_y2 - text_height) / 2

            # Desenarea textului
            draw.text((text_x, text_y), str(vehicle[4]), font=font, fill=(255, 255, 255))
        draw.text((image_width - 100, 10), f"Cars: {cars_between_lines}", font=font, fill=(255, 255, 255))