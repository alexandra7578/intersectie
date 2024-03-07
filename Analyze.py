from Boundin_Boxes import *
from tracker import *

class Analyzer:
    def __init__(self, bounding_box_extractor, img_tracker):
        self.bounding_box_extractor = bounding_box_extractor
        self.tracked_boxes = None
        #self.img_tracker=img_tracker

    def analyze_frame(self, img):
        self.tracked_boxes = self.bounding_box_extractor.get_bounding_boxes(img)

    def get_vehicles(self):
        return self.tracked_boxes