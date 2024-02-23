import pandas as pd
from datetime import datetime, timedelta
from tracker import Tracker
import time

class BoundingBoxExtractor:
    def __init__(self, model, class_list):
        self.model = model
        self.class_list = class_list
        self.previous_time = datetime.now()
        self.static_vehicle_ids = set()
        self.dynamic_vehicle_ids = set()
        self.tracker = Tracker()  # Presupunând că aveți o clasă Tracker pentru urmărire
        self.tracking_objects = {}
        self.bbox_list = []  # Adăugăm aceste variabile la nivel de clasă
        self.availability_time_list = []

    def get_bounding_boxes(self, img):
        results = self.model.predict(img)
        boxes = results[0].boxes.data
        px = pd.DataFrame(boxes).astype("float")
        self.bbox_list = []  # Resetăm listele la fiecare apel
        self.availability_time_list = []

        current_time = datetime.now()
        elapsed_time = current_time - self.previous_time
        self.previous_time = current_time

        for _, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])

            c = self.class_list[d]
            if 'car' in c and y1 > 75:
                self.bbox_list.append([x1, y1, x2, y2, 0])  # 0 în locul pentru ID-ul tracker-ului
                self.availability_time_list.append(elapsed_time.total_seconds())

        # Actualizează tracker-ul cu noile bounding box-uri
        self.tracker.update(self.bbox_list)

        # Obține toate obiectele de urmărire curente
        current_tracks = self.tracker.get_current_tracks()

        # Actualizează informațiile despre obiectele de urmărire
        for track_id, bbox in current_tracks.items():
            if track_id not in self.tracking_objects:
                self.tracking_objects[track_id] = {'last_appearance_time': time.time(), 'status': 'dynamic'}

            # Calculează timpul scurs de la ultima apariție
            elapsed_time = time.time() - self.tracking_objects[track_id]['last_appearance_time']

            # Actualizează status-ul în funcție de pragul de timp (30 secunde în exemplul de mai jos)
            if elapsed_time >= 30:
                self.tracking_objects[track_id]['status'] = 'static'
            else:
                self.tracking_objects[track_id]['status'] = 'dynamic'

            # Actualizează timpul ultimei apariții
            self.tracking_objects[track_id]['last_appearance_time'] = time.time()

        return self.bbox_list, self.availability_time_list

    def update(self):
        current_time = datetime.now()

        for bbox_id, availability_time in zip(self.bbox_list, self.availability_time_list):
            if availability_time >= 30:  # Prag de 30 secunde (300 secunde)
                self.static_vehicle_ids.add(bbox_id)
            else:
                # Actualizează timpul de disponibilitate pentru mașinile care se mișcă
                bbox_id_index = self.dynamic_vehicle_ids.index(bbox_id) if bbox_id in self.dynamic_vehicle_ids else None
                if bbox_id_index is not None:
                    self.dynamic_vehicle_ids.remove(bbox_id)
        print(self.dynamic_vehicle_ids)
        return self.static_vehicle_ids, self.dynamic_vehicle_ids

    def get_status(self, track_id):
        return self.tracking_objects.get(track_id, {}).get('status', 'unknown')
