class Ticket(object):
    def __init__(self, passenger, flight):
        self.flight = flight
        self.name = passenger.name
        self.surname = passenger.surname
        passenger.ticket = self
    """description of class"""


