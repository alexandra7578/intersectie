from datetime import datetime, timedelta
from tracker import Tracker

class ImageTracker:
    def __init__(self):
        self.tracking_objects = {}
        self.tracking_object_status = {}

    def update(self, bbox_list):
        # Actualizează tracker-ul cu noile bounding box-uri
        self.bounding_box_extractor.update(bbox_list)

        # Obține toate obiectele de urmărire curente
        current_tracks = self.bounding_box_extractor.get_updated_bbox()

        # Actualizează informațiile despre obiectele de urmărire
        for track_id, bbox in current_tracks.items():
            if track_id not in self.tracking_objects:
                self.tracking_objects[track_id] = {'last_appearance_time': datetime.now(), 'status': 'dynamic'}

            # Calculează timpul scurs de la ultima apariție
            elapsed_time = datetime.now() - self.tracking_objects[track_id]['last_appearance_time']

            # Actualizează status-ul în funcție de pragul de timp (30 secunde în exemplul de mai jos)
            if elapsed_time.total_seconds() >= 10:
                self.tracking_objects[track_id]['status'] = 'static'
            else:
                self.tracking_objects[track_id]['status'] = 'dynamic'

            # Actualizează timpul ultimei apariții
            self.tracking_objects[track_id]['last_appearance_time'] = datetime.now()

            # Actualizează statusul înregistrat pentru acest tracking_obj
            self.update_status(track_id, self.tracking_objects[track_id]['status'])

    def update_status(self, track_id, status):
        # Actualizează statusul pentru un anumit obiect de urmărire
        if track_id in self.tracking_object_status:
            self.tracking_object_status[track_id] = status
