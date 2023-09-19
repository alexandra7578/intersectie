from Image_display import *
from Image_display import *
from Analyze import *
from Boundin_Boxes import*
import threading
root = tkinter.Tk()
root.geometry("1000x1000")

image_label_nord=tkinter.Label(root)
image_label_nord.place(x=350, y=25)
image_label_sud=tkinter.Label(root)
image_label_sud.place(x=350, y=520)
image_label_est=tkinter.Label(root)
image_label_est.place(x=15, y=270)
image_label_vest=tkinter.Label(root)
image_label_vest.place(x=600, y=270)
# o functie care parseaza folderele cate elem au
# daca sunt egale le iau una cate una cu un i
# analyze si draw
def process_direction(direction, image_display, analyzer, image_label, i=0):
    filenames = image_display.get_filenames()
    i = (i + 1) % len(filenames)

    img = Image.open(filenames[i])
    img = img.resize((350, 200))

    analyzer.analyze_frame(img)
    vehicles = analyzer.get_vechicle()

    image_display.display_vehicles(vehicles, img)
    image_display.draw_count(img, 0)

    img_tk = ImageTk.PhotoImage(img)
    image_label.configure(image=img_tk)
    image_label.image = img_tk

    # Schedule the next iteration after a delay
    root.after(1000, process_direction, direction, image_display, analyzer, image_label, i)
# Initialize ImageDisplay instances for different directions
image_display_nord = ImageDisplay(root, "D:\Work\intersectie\Poze_Nord")
# image_display_sud = ImageDisplay(root, "D:\Work\intersectie\Poze_Sud")
# image_display_est = ImageDisplay(root, "D:\Work\intersectie\Poze_Est")
# image_display_vest = ImageDisplay(root, "D:\Work\intersectie\Poze_Vest")

# Initialize BoundingBoxExtractor and Analyzer instances
bounding_box_extractor = BoundingBoxExtractor(model, class_list)
img_tracker_nord = Tracker()
img_tracker_sud=Tracker()
img_tracker_vest=Tracker()
img_tracker_est=Tracker()
analyzer_nord = Analyzer(bounding_box_extractor=bounding_box_extractor, img_tracker=img_tracker_nord)
analyzer_sud = Analyzer(bounding_box_extractor=bounding_box_extractor, img_tracker=img_tracker_sud)
analyzer_est = Analyzer(bounding_box_extractor=bounding_box_extractor, img_tracker=img_tracker_est)
analyzer_vest = Analyzer(bounding_box_extractor=bounding_box_extractor, img_tracker=img_tracker_vest)

# Call process_direction for each direction
process_direction("nord", image_display_nord, analyzer_nord, image_label_nord, 0)
# # process_direction("sud", image_display_sud, analyzer_sud, image_label_sud, 0)
# # process_direction("est", image_display_est, analyzer_est, image_label_est, 0)
# process_direction("vest", image_display_vest, analyzer_vest, image_label_vest, 0)

root.mainloop()
