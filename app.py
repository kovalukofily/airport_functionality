import Worker
import CheckIn
import Dispatching
import Flight
import Gate
import GroundWork
import Luggage
import Passenger
import Security
import Ticket
from flask import Flask, render_template, request, jsonify, session
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh_so_secret'

#create the personnel
all_workers = [Worker.Worker(CheckIn, "1", "pass"),
               Worker.Worker(Dispatching, "2", "pass"),
               Worker.Worker(Gate, "3", "pass"),
               Worker.Worker(GroundWork, "4", "pass"),
               Worker.Worker(Security, "5", "pass")]


#Creating the flight
flight_to_jfk = Flight.Flight()

#Creating the processes
check_in = CheckIn.CheckIn(flight_to_jfk)
security = Security.Security()
dispatching = Dispatching.Dispatching()
ground_work = GroundWork.GroundWork()
gate = Gate.Gate(flight_to_jfk)

#Creating the passenger
passenger = Passenger.Passenger('Vladyslav', 'Kovalenko')
ticket = Ticket.Ticket(passenger, flight_to_jfk)
luggage = Luggage.Luggage()
handbags = ["phone", "camera", "clothes", "toothbrush"]


def get_worker_type(login):
    for worker in all_workers:
        if worker.login == login:
            return worker.worker_type


@app.route('/')
def main_page():
    print("Passenger Status", passenger.status)
    try:
        session_worker = session["session_worker"]
    except KeyError:
        session_worker = None
    print("Session Worker", session_worker)
    #info = json.dumps({"display_login": 1 if session_worker is None else 0,
    #"session_worker": str(session_worker) if session_worker is not None else "NONE."})
    #print(info)
    if session_worker is None:
        return render_template("main.html")
    elif get_worker_type(session_worker) == CheckIn:
        return render_template("_checkin.html")
    elif get_worker_type(session_worker) == Dispatching:
        return render_template("_disp.html")
    elif get_worker_type(session_worker) == Gate:
        return render_template("_gate.html")
    elif get_worker_type(session_worker) == GroundWork:
        return render_template("_ground.html")
    elif get_worker_type(session_worker) == Security:
        return render_template("_security.html")


@app.route('/login', methods = ['POST'])
def login():
    print("Passenger Status", passenger.status)
    try:
        session_worker = session["session_worker"]
    except KeyError:
        session_worker = None
    print("Session Worker", session_worker)
    username = request.form['login']
    password = request.form['password']
    for worker in all_workers:
        if worker.login == username and worker.password == password:
            session["session_worker"] = worker.login
            return render_template("logged_in.html")
    return render_template("login_failed.html")


@app.route('/logout')
def logout():
    print("Passenger Status", passenger.status)
    try:
        session_worker = session["session_worker"]
    except KeyError:
        session_worker = None
    print("Session Worker", session_worker)
    session["session_worker"] = None
    return render_template("logged_out.html")


@app.route('/checked_in', methods = ['POST'])
def checked_in():
    print("Passenger Status", passenger.status)
    try:
        session_worker = session["session_worker"]
    except KeyError:
        session_worker = None
    print("Session Worker", session_worker)
    result = check_in.check_passenger_in(passenger, ticket, luggage, request.form["passport"])
    print("Passenger Status", passenger.status)
    if result:
        return render_template("done.html")
    else:
        return render_template("failure.html")


@app.route('/security_done')
def security_done():
    print("Passenger Status", passenger.status)
    try:
        session_worker = session["session_worker"]
    except KeyError:
        session_worker = None
    print("Session Worker", session_worker)
    if passenger.status != 1:
        return render_template("failure.html")
    result = security.check(handbags)
    if result:
        passenger.status = 2
    print("Passenger Status", passenger.status)
    if result:
        return render_template("done.html")
    else:
        return render_template("failure.html")


@app.route('/gate_done')
def gate_done():
    print("Passenger Status", passenger.status)
    try:
        session_worker = session["session_worker"]
    except KeyError:
        session_worker = None
    print("Session Worker", session_worker)
    print("Passenger Status", passenger.status)
    if passenger.status != 2 or not flight_to_jfk.aboard:
        return render_template("failure.html")
    gate.admit(passenger)
    print("Passenger Status", passenger.status)
    return render_template("done.html")


@app.route('/ground_done')
def ground_done():
    print("Passenger Status", passenger.status)
    try:
        session_worker = session["session_worker"]
    except KeyError:
        session_worker = None
    print("Session Worker", session_worker)
    print("Passenger Status", passenger.status)
    if passenger.status not in (1, 2, 3) or not flight_to_jfk.aboard:
        return render_template("failure.html")
    ground_work.send_to_flight(luggage)
    print("Passenger Status", passenger.status)
    return render_template("done.html")


@app.route('/disp_done')
def disp_done():
    print("Passenger Status", passenger.status)
    try:
        session_worker = session["session_worker"]
    except KeyError:
        session_worker = None
    print("Session Worker", session_worker)
    dispatching.arrive(flight_to_jfk)
    return render_template("done.html")


if __name__ == '__main__':
    app.run(port=80)
    # session_worker = None