import random
import time
import csv


class Simulation:
    def __init__(self, velocity: float, start_1:int, start_2: int,end_1: int,end_2: int, position=0, time_step=0.1):
        # assert isinstance(start_1, int), f"{start_1} should be an int"
        # assert isinstance(end_1, int), f"{end_1} should be an int"
        # assert isinstance(start_2, int), f"{start_2} should be int"
        # assert isinstance(end_2, int), f"{end_2} should be int"

        self.velocity = velocity
        self.position = position
        self.start_1 = start_1
        self.end_1 = end_1
        self.start_2 = start_2
        self.end_2 = end_2
        self.magnet_zones = [(self.start_1,self.end_1), (self.start_2,self.end_2)]
        self.state_on = False
        self.stopped = False
        self.running = True
        self.time_step = time_step
        self.times = []
        self.positions = []
        self.atom_continuesText = ""
        self.atom_stopsText = ""
        # for reset function
        self.initial_velocity = velocity
        self.initial_position = position
        self.initial_time = time_step
    def start(self):
        for t in range(100):
            global curr_time
            if self.stopped:
                break
            curr_time = t*self.time_step
            self.position += self.velocity * self.time_step
            if any(start <= self.position <= end for (start, end) in self.magnet_zones):
                self.state_on = True
                self.atom_continuesText = f"Magnetic field detected at {self.position:.2f} m  and time {curr_time:.1f}s - stopping! State is off?: {self.state_on}"

                # print(f"Magnetic field detected at {self.position:.2f} m  and time {curr_time:.1f}s - stopping! State is off?: {self.state_on}")
                self.velocity = 0
                self.stopped = True

            self.times.append(curr_time)
            self.positions.append(self.position)
            self.atom_stopsText = f"Time: {curr_time:.1f}s, Position: {self.position:.2f} m and state is off?: {self.state_on}"
            # print(f"Time: {curr_time:.1f}s, Position: {self.position:.2f} m and state is off?: {self.state_on}")

    def reset(self):
        self.velocity = self.initial_velocity
        self.position = self.initial_position
        self.state_on = False
        self.stopped = False
        self.times.clear()
        self.positions.clear()
    def magnetzone_active(self):
        return self.state_on
    def get_variables(self):
        return self.position, self.velocity, curr_time, self.state_on
    # WIP: create CSV file 
    # def create_csv(self, name):
    #     csv_file = name + ".csv"
    #     with open(csv_file, 'w', newline='') as csvdata:
    #         writer = csv.writer(csvdata)
    #         writer.writerow(["Time", "Position"])
    #         for t, p in zip(self.times, self.positions):
    #             writer.writerow([t,p])
    #     print(f"{csv_file} has been created!")


