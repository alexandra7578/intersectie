from Boundin_Boxes import *
from tracker import *

class Analyzer:
    def __init__(self, bounding_box_extractor, img_tracker):
        self.bounding_box_extractor = bounding_box_extractor
        self.img_tracker=img_tracker

    def analyze_frame(self, img):
        bbox_list, availability_time_list = self.bounding_box_extractor.get_bounding_boxes(img)
        # print(bbox_list)
        # vechicule noi
        self.img_tracker.update(bbox_list)
    def get_vehicles(self):
        return self.img_tracker.get_tracked_obj()
        print(self.img_tracker.get_tracked_obj())