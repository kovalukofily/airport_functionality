from random import randint
from string import ascii_uppercase


class CheckIn(object):
    def __init__(self, flight):
        self.flight = flight
        

    def check_passenger_in(self, passenger, ticket, luggage, passport):
        if not (passenger.name == ticket.name and passenger.surname == ticket.surname):
            print("Registration failed. Names don't match.")
            return False
        if not (self.flight.flight_nr == ticket.flight.flight_nr):
            print("Registration failed. Airports don't match.")
            return False
        print(f"Names and airports are matching. We can proceed checking {passenger.name} {passenger.surname} on a flight {self.flight.flight_nr}.")
        passenger.passport = passport
        if len(passport) != 8:
            return False
        if passport[0] not in list(ascii_uppercase) or passport[1] not in list(ascii_uppercase):
            return False
        nrs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if passport[2] not in nrs or passport[3] not in nrs or passport[4] not in nrs \
            or passport[5] not in nrs or passport[6] not in nrs or passport[7] not in nrs:
            return False
        if luggage.mass_kg > 20:
            print("Customer is charged.")
        luggage.id = randint(1000000, 9999999)
        luggage.flight = self.flight
        print("Luggage is now assigned an ID. Sticker is printed.")
        passenger.boarding_pass_id = randint(10000000, 99999999)
        print("Boarding pass is printed.")
        passenger.status = 1
        return True

