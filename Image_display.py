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

        for vehicle in tracked_vehicles:
            radius = 5

            # Folosiți metoda din Bounding_Box_Extractor pentru a obține statusul vehiculului
            vehicle_status = self.bounding_box_extractor.get_status(vehicle[4])
            #if vehicle_status is not None:
            #    # Desenează în funcție de status
            #    if vehicle_status == 'moving':
            draw.ellipse((vehicle[0], vehicle[1], vehicle[2], vehicle[3]),outline=(0, 0, 255), fill=(0, 0, 255))
            draw.text((vehicle[2], vehicle[3]), str(vehicle[4]), font=font, fill=(255, 255, 255))
            #    else:
            #        if vehicle_status == 'stationary':
            #            # Desenează cu altă culoare pentru vehiculele statice (de exemplu, roșu)
            #            draw.rectangle((x_upper_left, y_upper_left, x_bottom_right, y_bottom_right),
            #                       outline=(255, 0, 0), fill=(255, 0, 0))
            #            draw.text((x, y), str(vehicle_id), font=font, fill=(255, 255, 255))