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

print("Setting up configuration and render page...\n")

@app.route('/', methods=['GET', 'POST'])
def home():

    '''
    Defines the homepage to get methods ('GET') or ('POST') passed through the page. and runs the codes below in the homepage.
    '''
    error = ""
    if request.method == 'POST':
        if request.form['action'] == "IN-GARAGE":
            print("IN-GARAGE buttton pressed, loading script\n")
            if request.form['car-action'] == "park":
                print("Car is going to be parked\n")
                plate = automatic_plate_recognition.get_plate(os.path.join(os.getcwd(), request.form['id']))
                print("Getting the license plate of the car to be parked from image, with OpenAlpr: " + plate)
                if plate != 'error':
                    car_info = api.request_information(plate)
                    print("\n Requesting plate: " + plate + " for information from RDW database\n")
                    if car_info != "No data found":
                        print("Encrypting all information found in the database...\n")
                        encoded = encryptor.encrypt(str(car_info))
                        print("Information has been encrypoted and stored in the garage database using Py.Crypto\n")
                        status = "PARKED"\
                            if car_info['parkerentoegestaan'] == "Ja" else 'VIOLATION' and print("Car FLAGGED! Car with license plate: " + plate + " is not allowed to be parked here and has been flagged.")
                        print("The car is parked!")
                        database.register_parking(plate, encoded.decode("UTF-8").rstrip('{'), request.form['id'],
                                                  status)
                    else:
                        error = "Car not found in government api"
                else:
                    error = "Number plate not recognized"
            else:
                 error = "Car is already parked"
        elif request.form['action'] == "UIT-GARAGE":
            print("UIT-GARGAE button pressed loading script for removal \n")
            if request.form['car-action'] == "remove":
                print("Car is getting out of garage...\n")
                plate = request.form['id']
                database.finish_parking(plate)
                print("Car with number place: " + str(plate) + " removed from garage and stored in history database")
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
