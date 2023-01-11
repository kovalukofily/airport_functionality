class Passenger(object):
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.boarding_pass_id = None
        self.status = 0 # 0 = nothing done, 1 = checked in, 2 = security passed, 3 = on flight


