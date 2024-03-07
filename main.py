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

def configure(root):
    image_label_vest = tkinter.Label(root)
    image_label_vest.place(x=600, y=270)
    bounding_box_extractor = BoundingBoxExtractor(model, class_list)
    image_display_pod = ImageDisplay(root, os.path.join(project_path, "Poze_Pod"), bounding_box_extractor)
    filenames_pod = image_display_pod.get_filenames()

    img_tracker = Tracker()
    analyzer_nord = Analyzer(bounding_box_extractor=bounding_box_extractor, img_tracker=img_tracker)

    return image_label_vest, bounding_box_extractor, image_display_pod, filenames_pod, img_tracker, analyzer_nord





def process_direction(direction, image_display, analyzer, bounding_box_extractor,filenames, image_label, root):
    mot_tracker = Sort()
    for i in range(len(filenames)):
        img = Image.open(filenames[i])
        print("Frame number: {}".format(i))

        # Obțineți detecțiile pentru imaginea curentă
        track_bbs_ids = bounding_box_extractor.get_bounding_boxes(img)
        print("detections: {}".format(len(track_bbs_ids)))

        # Actualizați eticheta imaginii pentru a afișa imaginea curentă
        image_display.display_vehicles(img, track_bbs_ids)
        image_display.draw_count(img, 0)
        img_tk = ImageTk.PhotoImage(img)
        image_label.configure(image=img_tk)
        image_label.image = img_tk
        root.update()  # Actualizați fereastra Tkinter
        root.after(1000)

    # for i in range(len(filenames)):
    #     img = Image.open(filenames[i])
    #     print("Frame number: {}".format(i))
    #
    #     analyzer.analyze_frame(img)
    #     tracked_vehicles = analyzer.get_vehicles()
    #
    #     image_display.display_vehicles(img, tracked_vehicles)
    #     image_display.draw_count(img, 0)
    #
    #     img_tk = ImageTk.PhotoImage(img)
    #     image_label.configure(image=img_tk)
    #     image_label.image = img_tk
    #     root.update()  # Update the Tkinter window
    #     root.after(1000)


# def main():
#     root=tkinter.Tk()
#     image_label_vest = tkinter.Label(root)
#     image_label_vest.place(x=600, y=270)
#     bounding_box_extractor = BoundingBoxExtractor(model, class_list)
#     # Initialize ImageDisplay instances for different directions
#     # image_display_nord = ImageDisplay(root, "D:\Work\intersectie\Poze_Nord")
#     # image_display_sud = ImageDisplay(root, "D:\Work\intersectie\Poze_Sud")
#     # image_display_est = ImageDisplay(root, "D:\Work\intersectie\Poze_Est")
#     # image_display_vest = ImageDisplay(root, "D:\Work\intersectie\Poze_Vest")
#     image_display_pod = ImageDisplay(root, "D:\Work\intersectie\Poze_Pod", bounding_box_extractor)
#     filenames_pod = image_display_pod.get_filenames()
#     # Initialize BoundingBoxExtractor and Analyzer instances
#
#     img_tracker = Tracker()
#     analyzer_nord = Analyzer(bounding_box_extractor=bounding_box_extractor, img_tracker=img_tracker)
#     # analyzer_sud = Analyzer(bounding_box_extractor=bounding_box_extractor, img_tracker=img_tracker)
#     # analyzer_est = Analyzer(bounding_box_extractor=bounding_box_extractor, img_tracker=img_tracker)
#     # analyzer_vest = Analyzer(bounding_box_extractor=bounding_box_extractor, img_tracker=img_tracker)
#     #analyzer_pod = Analyzer(bounding_box_extractor=bounding_box_extractor, img_tracker=img_tracker)
#
#     # Call process_direction for each direction
#     # process_direction("nord", image_display_nord, analyzer_nord)
#     # process_direction("sud", image_display_sud, analyzer_sud, image_label_sud, 0)
#     # process_direction("est", image_display_est, analyzer_est, image_label_est, 0)
#     # process_direction("vest", image_display_vest, analyzer_vest, image_label_vest, 0)
#     process_direction("nord", image_display_pod, analyzer_nord, filenames_pod, image_label_vest, root)
#     root.mainloop()
def main():
    root = tkinter.Tk()
    bounding_box_extractor = BoundingBoxExtractor(model, class_list)
    # Call the configure function to set up components
    image_label_vest, bounding_box_extractor, image_display_pod, filenames_pod, img_tracker, analyzer_nord = configure(
        root)


    process_direction("nord", image_display_pod, analyzer_nord,bounding_box_extractor, filenames_pod, image_label_vest, root)

    # Start the Tkinter main loop
    root.mainloop()

# Call the main function
if __name__ == "__main__":
    main()
