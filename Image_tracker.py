from tracker import *

class ImageTracker:
    def __init__(self):
        self.tracker = Tracker()
        self.area_c = set()
        self.static_vehicle_ids = set()
        self.dynamic_vehicle_ids = set()

    def update(self, bbox_list, availability_time_list):
        for bbox_id, availability_time in zip(bbox_list, availability_time_list):
            if availability_time > 0:
                self.dynamic_vehicle_ids.add(bbox_id)
                if bbox_id in self.static_vehicle_ids:
                    self.static_vehicle_ids.remove(bbox_id)
            else:
                self.static_vehicle_ids.add(bbox_id)
                if bbox_id in self.dynamic_vehicle_ids:
                    self.dynamic_vehicle_ids.remove(bbox_id)

        return list(self.static_vehicle_ids), list( self.dynamic_vehicle_ids)  # Convertim seturile în liste pentru a le returna



    def get_count(self):
        return len(self.dynamic_vehicle_ids)