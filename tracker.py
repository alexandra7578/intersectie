import math
from datetime import datetime, timedelta

class TrackObj:
    def __init__(self, center_point):
        self.box = None
        self.first_occurrence_time = datetime.now()
        self.center_point = center_point
        self.status = 'unknown'
        self.stationary_time = timedelta(seconds=0)  # timpul de staționare

    def update_stationary_time(self):
        if self.status == 'stationary':
            self.stationary_time += timedelta(seconds=1)
        else:
            self.stationary_time = timedelta(seconds=0)

class Tracker:

    def __init__(self):
        self.count = 0
        self.center_points_prev_frame = []
        self.tracking_objects = {}  # dicționar cu identificatori unici
        self.track_id = 0

    def get_tracked_obj(self):
        return self.tracking_objects

    def update(self, boxes):
        self.count += 1
        center_points_cur_frame = []

        # Colectează toate punctele centrale ale detecțiilor curente
        for box in boxes:
            (x1, y1, x2, y2, id) = box
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            center_point = (cx, cy)
            center_points_cur_frame.append(center_point)

        # Doar la început comparăm frame-ul anterior cu frame-ul curent
        if self.count <= 2:
            for pt in center_points_cur_frame:
                for pt2 in self.center_points_prev_frame:
                    distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                    if distance < 50:
                        # Crează un obiect TrackObj și adaugă-l în dicționarul de urmărire
                        self.tracking_objects[self.track_id] = TrackObj(pt)
                        self.track_id += 1
                        break
            print("Tracking objects")
            print(self.tracking_objects)
        else:
            tracking_objects_copy = self.tracking_objects.copy()

            for object_id, track_obj in tracking_objects_copy.items():
                object_exists = False
                pt_closest = (1000, 1000)
                distance_smallest = 1000

                for pt in center_points_cur_frame:
                    distance_tracked_2_current = math.hypot(track_obj.center_point[0] - pt[0],
                                                            track_obj.center_point[1] - pt[1])

                    if distance_tracked_2_current < distance_smallest:
                        distance_smallest = distance_tracked_2_current
                        pt_closest = pt

                if distance_smallest < 200:
                    # De actualizat statusul; dacă distance_smallest < 10, masina e parcata
                    if distance_smallest < 10:
                        track_obj.status = 'parked'
                    else:
                        track_obj.status = 'moving'
                        track_obj.update_stationary_time()

                        if (
                                track_obj.status == 'stationary'
                                and track_obj.stationary_time > timedelta(seconds=30)
                        ):
                            print(f"Car {object_id} has been stationary for more than 30 seconds.")

                    # Actualizează punctul central al obiectului de urmărire
                    self.tracking_objects[object_id].center_point = pt_closest
                    object_exists = True

                    if pt_closest in center_points_cur_frame:
                        center_points_cur_frame.remove(pt_closest)
                else:
                    current_time = datetime.now()
                    time_since_first_occurrence = current_time - track_obj.first_occurrence_time
                    if time_since_first_occurrence.total_seconds() > 30:
                        track_obj.status = 'stationary'
                    else:
                        track_obj.status = 'moving'

                # Elimină obiectele pierdute
                if not object_exists:
                    print("Tracked object missing cur frame")
                    self.tracking_objects.pop(object_id)

            # Adaugă noile identificatori găsite
            for pt in center_points_cur_frame:
                self.tracking_objects[self.track_id] = TrackObj(pt)
                self.track_id += 1

        self.center_points_prev_frame = center_points_cur_frame.copy()

    def get_current_tracks(self):
        return self.tracking_objects

