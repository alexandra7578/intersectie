import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from tracker import Tracker
import time
from sort import *

class BoundingBoxExtractor:
    def __init__(self, model, class_list):
        self.model = model
        self.class_list = class_list
        self.tracking_objects = {}
        self.tracker = Sort(max_age=3, min_hits=1, iou_threshold=0.01)

    def get_bounding_boxes(self, img):
        results = self.model.predict(img)
        boxes = results[0].boxes.data
        px = pd.DataFrame(boxes).astype("float")

        detections = []
        for _, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])

            c = self.class_list[d]
            if 'car' in c and y1 > 75:
                detections.append([x1, y1, x2, y2, 1]) #1 represent the score

        # Actualizăm tracker-ul SORT cu detecțiile
        track_bbs_ids = self.update_tracker(np.array(detections))

        return track_bbs_ids

    def update_tracker(self, detections):
        return self.tracker.update(detections)

    def get_status(self, track_id):
        return self.tracking_objects.get(track_id, {}).get('status', 'unknown')


