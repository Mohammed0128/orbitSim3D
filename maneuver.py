class maneuver():
    def __init__(self, name, vessel, mnv_type):
        self.name = name
        self.vessel = vessel
        self.type = mnv_type

    def get_vessel(self):
        return self.vessel

class maneuver_const_accel(maneuver):
    def __init__(self, name, vessel, frame_body, orientation, accel, t_start, duration):
        super().__init__(name, vessel, "const_accel")
        self.frame_body = frame_body
        self.orientation = orientation
        self.orientation_input = orientation
        self.accel = accel
        self.duration = duration
        self.t_start = t_start
        self.done = False

        self.draw_vertices = []

    def set_orientation(self):
        if not type(self.orientation) == list or self.orientation_input[-8:] == "_dynamic":
            self.orientation = self.vessel.get_orientation_rel_to(self.frame_body, self.orientation)

    def perform_maneuver(self, current_time, delta_t):
        
        if (not self.done) and current_time >= self.t_start:
            self.set_orientation()
            
            self.vessel.update_vel([self.orientation[0] * self.accel,
                                    self.orientation[1] * self.accel,
                                    self.orientation[2] * self.accel], delta_t)

            self.draw_vertices.append([self.vessel.get_draw_pos()[0],
                                       self.vessel.get_draw_pos()[1],
                                       self.vessel.get_draw_pos()[2]])

            # if the orientation is set as "dynamic"
            # it needs to be updated every frame
            if self.orientation_input[-8:] == "_dynamic":
                self.orientation = self.orientation_input
            
        if (not self.done) and (current_time > (self.t_start + self.duration)):
            self.done = True

    def is_performing(self, current_time):
        if not self.done and current_time >= self.t_start:
            return True
        else:
            return False

    def get_state(self, current_time):
        if self.done:
            return "Completed"
        elif current_time >= self.t_start:
            return "Performing"
        else:
            return "Pending"

    def get_name(self):
        return self.name

    def get_draw_vertices(self):
        return self.draw_vertices

    def clear_draw_vertices(self):
        self.draw_vertices = []

    def get_params_str(self):
        output = "Vessel: " + self.vessel.get_name() + "\n"
        
        if not type(self.orientation_input) == list:
            if self.orientation_input[-8:] == "_dynamic":
                output += "Orientation: " + self.orientation_input[0:-8] + " (dynamic) rel to " + self.frame_body.get_name()
            else:
                output += "Orientation: " + self.orientation_input[-8:] + " rel to " + self.frame_body.get_name()
        else:
            output += "Orientation: " + str(self.orientation) + " rel to global frame"
            
        output += "\nAcceleration: " + str(self.accel) + " m/s^2\n"
        output += "Start time: " + str(self.t_start) + " s\n"
        output += "Duration: " + str(self.duration) + " s\n"

        return output
    
    def get_duration(self):
        return self.duration

class maneuver_const_thrust(maneuver):
    def __init__(self, name, vessel, frame_body, orientation, thrust, mass_init, mass_flow,
                 t_start, duration):
        
        super().__init__(name, vessel, "const_thrust")
        self.frame_body = frame_body
        self.orientation = orientation
        self.orientation_input = orientation
        self.thrust = thrust
        self.mass_init = mass_init
        self.mass_flow = mass_flow
        self.t_start = t_start
        self.duration = duration
        self.done = False

        self.mass = mass_init

        self.draw_vertices = []

    def set_orientation(self):
        if not type(self.orientation) == list or self.orientation_input[-8:] == "_dynamic":
            self.orientation = self.vessel.get_orientation_rel_to(self.frame_body, self.orientation)

    def perform_maneuver(self, current_time, delta_t):

        if (not self.done) and current_time >= self.t_start:
            self.set_orientation()
            
            if self.mass <= 0:
                self.done = True
                return
            
            accel = self.thrust/self.mass
            self.mass -= self.mass_flow * delta_t
            
            self.vessel.update_vel([self.orientation[0] * accel,
                                    self.orientation[1] * accel,
                                    self.orientation[2] * accel], delta_t)

            self.draw_vertices.append([self.vessel.get_draw_pos()[0],
                                       self.vessel.get_draw_pos()[1],
                                       self.vessel.get_draw_pos()[2]])

            # if the orientation is set as "dynamic"
            # it needs to be updated every frame
            if self.orientation_input[-8:] == "_dynamic":
                self.orientation = self.orientation_input
            
        if (not self.done) and (current_time > (self.t_start + self.duration)):
            self.done = True

    def is_performing(self, current_time):
        if not self.done and current_time >= self.t_start:
            return True
        else:
            return False

    def get_state(self, current_time):
        if self.done:
            return "Completed"
        elif current_time >= self.t_start:
            return "Performing"
        else:
            return "Pending"

    def get_name(self):
        return self.name

    def get_draw_vertices(self):
        return self.draw_vertices

    def clear_draw_vertices(self):
        self.draw_vertices = []

    def get_params_str(self):
        output = "Vessel: " + self.vessel.get_name() + "\n"
        
        if not type(self.orientation_input) == list:
            if self.orientation_input[-8:] == "_dynamic":
                output += "Orientation: " + self.orientation_input[0:-8] + " (dynamic) rel to " + self.frame_body.get_name()
            else:
                output += "Orientation: " + self.orientation_input[-8:] + " rel to " + self.frame_body.get_name()
        else:
            output += "Orientation: " + str(self.orientation) + " rel to global frame"
            
        output += "\nThrust: " + str(self.thrust) + " N\n"
        output += "Initial mass:" + str(self.mass_init) + " kg\n"
        output += "Mass flow: " + str(self.mass_flow) + " kg/s\n"
        output += "Start time: " + str(self.t_start) + " s\n"
        output += "Duration: " + str(self.duration) + " s\n"

        return output

    def get_duration(self):
        return self.duration
