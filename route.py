__author__ = 'zahyr'

import os
import config
from flask import Flask, render_template, request, jsonify
from parking_lot_database import ParkingLotDatabase
from encryptor import Encryptor
from plate_recognition import AutomaticPlateRecognition
from rdw_api import RdwApi

app = Flask(__name__)

database = ParkingLotDatabase()
automatic_plate_recognition = AutomaticPlateRecognition()
api = RdwApi(config.API_KEY)
encryptor = Encryptor()
#
# plate = automatic_plate_recognition.get_plate(os.path.join(os.getcwd(), 'static/img/test4.jpg'))
# database.create_car()
# if plate != 'error':
# print(plate)
#     car_info = api.request_information(plate)
#     if car_info != "No data found":
#         encoded = encryptor.encrypt(str(car_info))
#         database.register_parking(plate, encoded.decode("UTF-8").rstrip('{'), 'static/img/test4.jpg', car_info['parkerentoegestaan'])
#     else:
#         print("kek")

@app.route('/', methods=['GET', 'POST'])
def home():
    error = ""
    if request.method == 'POST':
        if request.form['action'] == "IN-GARAGE":
            if request.form['car-action'] == "park":
                plate = automatic_plate_recognition.get_plate(os.path.join(os.getcwd(), request.form['id']))
                print(plate)
                if plate != 'error':
                    car_info = api.request_information(plate)
                    if car_info != "No data found":
                        encoded = encryptor.encrypt(str(car_info))
                        status = "PARKED" if car_info['parkerentoegestaan'] == "Ja" else 'VIOLATION'
                        database.register_parking(plate, encoded.decode("UTF-8").rstrip('{'), request.form['id'],
                                                  status)
                    else:
                        error = "Car not found in government api"
                else:
                    error = "Number plate not recognized"
            else:
                 error = "Car is already parked"
        elif request.form['action'] == "UIT-GARAGE":
            if request.form['car-action'] == "remove":
                plate = request.form['id']
                database.finish_parking(plate)
            else:
                error = "Car not in parking"
    cars = {
        'all': database.get_all_cars(),
        'parked': database.current_cars_parked()
    }
    car_parked = {
        'all': database.get_all_cars_history()
    }

    return render_template('Index.html', cars=cars, error=error, car_parked=car_parked)


@app.route('/car/<id>')
def car(id=None):
    return jsonify(database.get_car_by_plate(id))


if __name__ == "__main__":
    app.run(debug=True, port=666)