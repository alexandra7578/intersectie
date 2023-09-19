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
    def __init__(self, root, pathtofiles):
        self.root = root
        self.pathtofiles = pathtofiles
        self.image_label = tkinter.Label(root)
        self.image_label.pack()
        self.image_tracker = ImageTracker()
        self.filenames = self.get_filenames()
        self.current_index = 0


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

    def display_vehicles(self, vehicles, img):
        availability_time_list=[]
        dynamic_vechicale_id=[]
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', 10)
        #
        for vehicle in vehicles:
            if not vehicle.is_stationary():
                vehicle.get_availability()
                var=vehicle.get_id()

                #bounding_box.get_bounding_boxes(img)
                x1, y1, x2, y2,id =vehicle.box
                draw.rectangle((x1, y1, x2, y2), outline='red', width=3)
                draw.text((x1, y1), str(var), font=font, fill=(255, 255, 255))
            count = self.image_tracker.get_count()
            self.draw_count(img, count)