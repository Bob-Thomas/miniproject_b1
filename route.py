__author__ = 'zahyr'

import os
import config
from flask import Flask, render_template, request, jsonify
from parking_lot_database import ParkingLotDatabase
from encryptor import Encryptor
from plate_recognition import AutomaticPlateRecognition
from rdw_api import RdwApi


'''
imported module Flask is assigned a variable app for easier use.
'''
app = Flask(__name__)

'''
imported module ParkingLotDatabase() is assigned a variable for easier use and cleanliness.
'''
database = ParkingLotDatabase()
'''
imported module AutomaticPlateRecognition() is assigned a variable for easier.
'''
automatic_plate_recognition = AutomaticPlateRecognition()
'''
imported module AutomaticPlateRecognition()) is assigned a variable for easier use.
'''
api = RdwApi(config.API_KEY)
'''
imported module and function RdwApi(config.API_KEY) is assigned a variable for easier use.
'''
encryptor = Encryptor()
'''
imported module and function Encryptor() is assigned a variable for easier use.
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    '''
    Defines the homepage to get methods ('GET') or ('POST') passed through the page. and runs the codes below in the homepage.
    '''
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
    '''
    Dictionaries created with the database variables for easier calling methods throughout the code, these lead back to the imported database files
    '''

    return render_template('Index.html', cars=cars, error=error, car_parked=car_parked)
'''
    renders the homepage with variable passed as cars, error and car_parked
'''

@app.route('/car/<id>')
def car(id=None):
    return jsonify(database.get_car_by_plate(id))

'''
Gets the JSON fine from RWD database and renders the file in browser.
'''

if __name__ == "__main__":
    app.run(debug=True, port=666)


'''
Runs the whole application on debugging mode and on port 666 for testing and feedback
'''
