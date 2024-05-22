import tkinter as tk
from PIL import Image, ImageTk
import os
import threading
from ultralytics import YOLO
import re

# Asigurați-vă că toate importurile sunt corecte și că modulele sunt disponibile
from Image_display import ImageDisplay
from Boundin_Boxes import BoundingBoxExtractor
from TrafficController import TrafficLightController
import tkinter
from sort import *
from Semafor import Semafor
import cv2
# pentru a face filmuletele imagini
# vidcap = cv2.VideoCapture('Est.mp4')
# def getFrame(sec):
#     vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
#     hasFrames,image = vidcap.read()
#     if hasFrames:
#         cv2.imwrite("est_00"+str(count)+".JPEG", image)     # save frame as JPG file
#     return hasFrames
# sec = 0
# frameRate = 0.5 #//it will capture image in each 0.5 second
# count=1
# # success = getFrame(s  ec)
# while success:
#     count = count + 1
#     sec = sec + frameRate
#     sec = round(sec, 2)
#     success = getFrame(sec)
_nsre = re.compile('([0-9]+)')
model = YOLO("yolov8n.pt")
my_file=open("model.txt", "r")
data=my_file.read()
class_list=data.split("\n")
# Setarea căii proiectului
project_path = os.path.abspath(os.path.dirname(__file__))

controller = TrafficLightController(ns_green_duration=10, ew_green_duration=10)
root = tk.Tk()
root.title("Traffic Light Simulation")
root.geometry("400x400")

semafor_nord = Semafor(root, x=950, y=50, initial_color='green')
semafor_sud = Semafor(root, x=900, y=540, initial_color='green')
semafor_est = Semafor(root, x=1200, y=100, initial_color='red')
semafor_vest = Semafor(root, x=100, y=100, initial_color='red')

# Gruparea semafoarelor Nord-Sud și Est-Vest
ns_semafoare = [semafor_nord, semafor_sud]
ew_semafoare = [semafor_est, semafor_vest]
def update_traffic_lights():
    if controller.current_state == 'NSG' or controller.current_state == 'NSY':
        ns_color = 'green' if controller.current_state == 'NSG' else 'yellow'
        ew_color = 'red'
    elif controller.current_state == 'EWG' or controller.current_state == 'EWY':
        ew_color = 'green' if controller.current_state == 'EWG' else 'yellow'
        ns_color = 'red'

    for light in ns_semafoare:
        light.set_color(ns_color)
    for light in ew_semafoare:
        light.set_color(ew_color)
    root.after(1000, update_traffic_lights)

def process_direction(root):
    last_update_time = time.time()
    update_frequency_time = 30  # secunde

    mot_tracker = Sort()
    image_label_nord = tkinter.Label(root)
    image_label_nord.place(x=500, y=25)
    image_label_sud = tkinter.Label(root)
    image_label_sud.place(x=500, y=400)
    image_label_est = tkinter.Label(root)
    image_label_est.place(x=15, y=270)
    image_label_vest = tkinter.Label(root)
    image_label_vest.place(x=1000, y=270)

    bounding_box_extractor_nord = BoundingBoxExtractor(model, class_list)
    image_display_nord = ImageDisplay(root, os.path.join(project_path, "Poze_Nord"), bounding_box_extractor_nord)
    filenames_nord = image_display_nord.get_filenames()

    bounding_box_extractor_sud = BoundingBoxExtractor(model, class_list)
    image_display_sud = ImageDisplay(root, os.path.join(project_path, "Poze_Sud"), bounding_box_extractor_sud)
    filenames_sud = image_display_sud.get_filenames()

    bounding_box_extractor_est = BoundingBoxExtractor(model, class_list)
    image_display_est = ImageDisplay(root, os.path.join(project_path, "Poze_Est"), bounding_box_extractor_est)
    filenames_est = image_display_est.get_filenames()

    bounding_box_extractor_vest = BoundingBoxExtractor(model, class_list)
    image_display_vest = ImageDisplay(root, os.path.join(project_path, "Poze_Vest"), bounding_box_extractor_vest)
    filenames_vest = image_display_vest.get_filenames()
    for i in range(len(filenames_vest)):
        img_nord = Image.open(filenames_nord[i])
        img_sud = Image.open(filenames_sud[i])
        img_est = Image.open(filenames_est[i])
        img_vest = Image.open(filenames_vest[i])
        img_nord = img_nord.resize((400, 350))
        img_sud = img_sud.resize((400, 350))
        img_est = img_est.resize((400, 350))
        img_vest = img_vest.resize((400, 350))
        print("Frame number: {}".format(i))


        # Obțineți detecțiile pentru imaginea curentă
        track_bbs_ids_nord = bounding_box_extractor_nord.get_bounding_boxes(img_nord)
        track_bbs_ids_sud = bounding_box_extractor_sud.get_bounding_boxes(img_sud)
        track_bbs_ids_est = bounding_box_extractor_est.get_bounding_boxes(img_est)
        track_bbs_ids_vest = bounding_box_extractor_vest.get_bounding_boxes(img_vest)
        print("detections: {}".format(len(track_bbs_ids_nord)))
        print("detections: {}".format(len(track_bbs_ids_est)))
        print("detections: {}".format(len(track_bbs_ids_vest)))
        print("detections: {}".format(len(track_bbs_ids_sud)))


        current_time = time.time()
        if current_time - last_update_time > update_frequency_time:
            ns_traffic = len(track_bbs_ids_nord)+len(track_bbs_ids_sud)  # Adună detecțiile pentru nord-sud
            ew_traffic = len(track_bbs_ids_est)+len(filenames_vest)  # Adună detecțiile pentru est-vest

            ns_green_time = 15 + 3 * (ns_traffic % 10)
            ew_green_time = 15 + 3 * (ew_traffic % 10)

            ns_green_time = min(ns_green_time, 60)  # Limita maxima de 60 secunde
            ew_green_time = min(ew_green_time, 60)  # Limita maxima de 60 secunde

            controller.set_green_duration(ns_duration=ns_green_time, ew_duration=ew_green_time)
            last_update_time = current_time

        controller.update_state()  # rularea semaforului
        update_traffic_lights()
        #Actualizați eticheta imaginii pentru a afișa imaginea curentă
        image_display_nord.display_vehicles(img_nord, track_bbs_ids_nord)
        image_display_nord.draw_count(img_nord, 0)
        img_tk_nord = ImageTk.PhotoImage(img_nord)
        image_label_nord.configure(image=img_tk_nord)
        image_label_nord.image = img_tk_nord


        image_display_sud.display_vehicles(img_sud, track_bbs_ids_sud)
        image_display_sud.draw_count(img_sud, 0)
        img_tk_sud = ImageTk.PhotoImage(img_sud)
        image_label_sud.configure(image=img_tk_sud)
        image_label_sud.image = img_tk_sud


        image_display_est.display_vehicles(img_est, track_bbs_ids_est)
        image_display_est.draw_count(img_est, 0)
        img_tk_est = ImageTk.PhotoImage(img_est)
        image_label_est.configure(image=img_tk_est)
        image_label_est.image = img_tk_est

        image_display_vest.display_vehicles(img_vest, track_bbs_ids_vest)
        image_display_vest.draw_count(img_vest, 0)
        img_tk_vest = ImageTk.PhotoImage(img_vest)
        image_label_vest.configure(image=img_tk_vest)
        image_label_vest.image = img_tk_vest


        root.update()  # Actualizați fereastra Tkinter
        root.after(500)


def main():
    process_direction(root)
    root.mainloop()

if __name__ == "__main__":
    main()


