import math
class TrackObj:
    def __init__(self):
        self.box = None
        self.first_occurrence_time = None
        self.center_point = None

    def update_box(self, new_box):
        self.box = new_box

class Tracker:

    def __init__(self):
        self.count=0
        self.center_points_prev_frame = []
        self.tracking_objects ={} #lista de trackobj
        self.track_id=0
    def get_tracked_obj(self):
        return self.tracking_objects

    def update(self, boxes):
        self.count+=1
        center_points_cur_frame=[]

        #collect all centraer points of the carent box detection
        for box in boxes:

            (x1, y1, x2, y2, id) = box

            cx = int((x1 + x2 ) / 2)
            cy = int((y1 + y2) / 2)

            center_points_cur_frame.append((cx, cy))
            # print("FRAME N: ", self.count, " ", x, y, w, h)
        # Only at the beginning we compare previous and current frame

        if self.count <= 2:
            for pt in center_points_cur_frame:
                for pt2 in self.center_points_prev_frame:
                    distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                    # for pt
                    if distance < 50:
                        self.tracking_objects[self.track_id] = pt
                        self.track_id += 1
            print("Tracking objects")
            print(self.tracking_objects)
        else:

            tracking_objects_copy = self.tracking_objects.copy()
            print(tracking_objects_copy)
            center_points_cur_frame_copy = center_points_cur_frame.copy()
            print(len(tracking_objects_copy))
            for object_id, pt2 in tracking_objects_copy.items():
                object_exists = False
                pt_closest=(1000,1000)
                distance_smalest=1000
                for pt in center_points_cur_frame_copy:
                    distance_tracked_2_curent = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                    # un for pt cea mai mica distanta
                    # Update IDs position
                    if distance_tracked_2_curent<distance_smalest:
                        distance_smalest=distance_tracked_2_curent
                        pt_closest=pt
                print(distance_smalest)
                if distance_smalest < 50:
                    self.tracking_objects[object_id] = pt_closest
                    object_exists = True
                    if pt_closest in center_points_cur_frame:
                        center_points_cur_frame.remove(pt_closest)

                # Remove IDs lost
                if not object_exists:
                    self.tracking_objects.pop(object_id)

            # Add new IDs found
            for pt in center_points_cur_frame:
                self.tracking_objects[self.track_id] = pt
                self.track_id += 1



        # print("Tracking obj")
        # print(self.tracking_objects)
        #
        # print("CUR FRAME")
        # print(self.center_points_cur_frame)
        #
        # print("PREV FARME")
        # print(self.center_points_prev_frame)

        self.center_points_prev_frame = center_points_cur_frame.copy()