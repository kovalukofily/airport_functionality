class Gate(object):
    """description of class"""

    def __init__(self, flight):
        self.flight_nr = flight.flight_nr

    def check_validity(self, passenger, ticket):
        if passenger.boarding_pass_id is not None and ticket.flight.flight_nr == self.flight_nr:
            return True
        return False

    def admit(self, passenger):
        x = self.check_validity(passenger, passenger.ticket)
        passenger.status = 3
        print("The passenger was admitted to the flight.")
        return x
