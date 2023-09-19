import pandas as pd
from datetime import datetime, timedelta
from tracker import *
from ultralytics import YOLO
model = YOLO("yolov8n.pt")
class BoundingBoxExtractor:
    def __init__(self, model, class_list):
        self.model =model
        self.class_list = class_list
        self.previous_time = datetime.now()
        self.static_vehicle_ids = []
        self.dynamic_vehicle_ids = []

    def get_bounding_boxes(self, img):
        results = self.model.predict(img)
        boxes = results[0].boxes.data
        px = pd.DataFrame(boxes).astype("float")
        bbox_list = []

        availability_time_list = []

        current_time = datetime.now()
        elapsed_time = current_time - self.previous_time
        for _, row in px.iterrows():

            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])

            c = self.class_list[d]
            if 'car' in c:
                bbox_list.append([x1, y1, x2, y2, 0])# 0 in the place holder for the trecker id
                availability_time_list.append(elapsed_time.total_seconds())
        # bbox_id=img_tracker.update(bbox_list)
        self.previous_time = current_time
        return bbox_list, availability_time_list

    def update(self, bbox_list, availability_time_list):
        for bbox_id, availability_time in zip(bbox_list, availability_time_list):
            if availability_time >= 300:  # Prag de 5 minute (300 secunde)
                self.static_vehicle_ids.append(bbox_id)
            else:
                self.dynamic_vehicle_ids.append(bbox_id)

        return self.static_vehicle_ids, self.dynamic_vehicle_ids

