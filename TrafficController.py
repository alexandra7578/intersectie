import time
import threading

class TrafficLightController:
    def __init__(self, ns_green_duration=10, ew_green_duration=10):
        self.ns_green_duration = ns_green_duration
        self.ew_green_duration = ew_green_duration
        self.current_state = 'NSG'  # Start with North-South Green
        self.state_start_time = time.time()
        self.yellow_duration=1 # sec

    def set_green_duration(self, ns_duration=None, ew_duration=None):
        if ns_duration is not None:
            self.ns_green_duration = ns_duration
        if ew_duration is not None:
            self.ew_green_duration = ew_duration

    def update_state(self):
        print(f"Current State Before Update: {self.current_state}")
        elapsed_time = time.time() - self.state_start_time
        if self.current_state == 'NSG' and elapsed_time >= self.ns_green_duration:
            self.current_state = 'NSY'
            print("Switching to NSY")
        elif self.current_state == 'NSY' and elapsed_time >= self.yellow_duration:
            self.current_state = 'EWG'
            print("Switching to EWG")
            self.state_start_time = time.time()
        elif self.current_state == 'EWG' and elapsed_time >= self.ew_green_duration:
            self.current_state = 'EWY'
            self.state_start_time = time.time()
        elif self.current_state == 'EWY' and elapsed_time >= self.yellow_duration:  # Assuming 3 seconds for yellow light
            self.current_state = 'NSG'
            self.state_start_time = time.time()