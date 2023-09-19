from datetime import datetime
class Vehicle:
    def __init__(self, box, id, start_time):
        self.box = box
        self.id = id
        self.start_time = start_time
        self.availability = self.calculate_availability()
        self.stationary=False

    def update(self, current_time, box):
        self.availability = self.calculate_availability(current_time)
        self.box=box
        if self.availability>300:
            self.stationary=True
        else:
            self.stationary=False

    def get_availability(self):
        return self.availability

    def get_id(self):
        return self.id

    def calculate_availability(self, current_time=None):
        if current_time is None:
            current_time = datetime.now()  # timpul curent în secunde
        return (current_time - self.start_time).total_seconds()

    def is_stationary(self):
        return  self.stationary
