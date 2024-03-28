from Image_display import *
from Image_display import *
from Analyze import *
from Boundin_Boxes import*
import tkinter
from PIL import Image, ImageTk
import os.path
import threading
from sort import Sort
import numpy as np


project_path = os.path.abspath(os.path.dirname(__file__))

# vidcap = cv2.VideoCapture('VideoPod.mp4')
# def getFrame(sec):
#     vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
#     hasFrames,image = vidcap.read()
#     if hasFrames:
#         cv2.imwrite("pod_00"+str(count)+".JPEG", image)     # save frame as JPG file
#     return hasFrames
# sec = 0
# frameRate = 0.5 #//it will capture image in each 0.5 second
# count=1
# success = getFrame(sec)
# while success:
#     count = count + 1
#     sec = sec + frameRate
#     sec = round(sec, 2)
#     success = getFrame(sec)
# root.geometry("1000x1000")

# image_label_nord=tkinter.Label(root)
# image_label_nord.place(x=350, y=25)
# image_label_nord=tkinter.Label(root)
# image_label_nord.place(x=350, y=25)
# image_label_sud=tkinter.Label(root)
# image_label_sud.place(x=350, y=520)
# image_label_est=tkinter.Label(root)
# image_label_est.place(x=15, y=270)
# image_label_vest=tkinter.Label(root)
# image_label_vest.place(x=600, y=270)
# o functie care parseaza folderele cate elem au
# daca sunt egale le iau una cate una cu un i
# analyze si draw

#o functie init si main unde sa apelez init
#in while i <nr_de_img_
#de optimizat c


def process_direction(root):
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

        # Actualizați eticheta imaginii pentru a afișa imaginea curentă
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
    root = tkinter.Tk()

    # Definirea funcțiilor pentru procesarea fiecărei direcții
    process_direction(root)

    # Start the Tkinter main loop
    root.mainloop()


# Apelați funcția main
if __name__ == "__main__":
    main()