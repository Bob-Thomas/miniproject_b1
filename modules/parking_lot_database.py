__author__ = 'Robbie'
import os
import sqlite3
import time
from encryptor import Encryptor


class ParkingLotDatabase(object):
    conn = sqlite3.connect(os.path.join(os.getcwd(), 'modules\parking_lot.db'), check_same_thread=False)
    c = conn.cursor()
    encryptor = Encryptor()

    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(os.getcwd(), 'modules\parking_lot.db'), check_same_thread=False)
        self.c = self.conn.cursor()
        self.encryptor = Encryptor()

    def create_tables(self):
        """
        Create the table(s) if not exists in the database.
        :return: NONE
        """
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS car_parked(id INTEGER PRIMARY KEY AUTOINCREMENT, licence_plate TEXT, register_time INT, status TEXT, end_time INT)")
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS car(id INTEGER PRIMARY KEY AUTOINCREMENT, licence_plate TEXT, info TEXT, image_path TEXT)")

        self.conn.commit()

    def create_car(self):
        """
        Execute an INSERT query to the database. the new row will contain a primary key and a image path. Rest of the attributes will be updated with values later.
        :return: NONE
        """
        count = 1
        while count <= 4:
            image_path = "static/img/test" + str(count) + ".jpg"
            self.c.execute("INSERT INTO car(image_path) VALUES(?)", (str(image_path), ))
            self.conn.commit()
            count = int(count) + 1

    def register_parking(self, licence_plate, info, image_path, status):
        """
        Update all general constant information in to the car table. The parking information will be stored in the car_parked table.
        :param licence_plate : TEXT
        :param info : TEXT (json formatted from import io)
        :param image_path : TEXT (path to image file)
        :param status : TEXT 'parked' OR 'violation'
        :return: NONE
        """
        # update the car table
        # self.c.execute("UPDATE car SET licence_plate='" + str(licence_plate) + "', info='" + str(
        # info) + "' WHERE image_path = '" + str(image_path) + "' ")

        self.c.execute("UPDATE car SET licence_plate=?, info=? WHERE image_path=?",
                       (str(licence_plate), str(info), str(image_path),))
        # insert into the car_parking table
        self.c.execute(
            "INSERT INTO car_parked(licence_plate, register_time, status) VALUES(?, ?, ?)",
            (str(licence_plate), str(time.time()), str(status), ))
        self.conn.commit()

    def current_cars_parked(self):

        result = []
        """
        SELECT * cars in the parking_lot where end_time IS NULL
        :return: list with cars parked in the parking lot
        """
        cars_parked_query = self.c.execute("SELECT * FROM car_parked WHERE end_time IS NULL")
        cars_parked = cars_parked_query.fetchall()
        return self.create_array_dict(cars_parked, True)

    def get_all_cars(self):
        query = self.c.execute("SELECT * FROM car")
        data = query.fetchall()

        return self.create_array_dict(data)

    def get_all_cars_history(self):
        query = self.c.execute("SELECT * FROM car_parked")
        data1 = query.fetchall()

        return self.create_array_dict(data1, True)

    def finish_parking(self, license_plate):
        self.c.execute("UPDATE car_parked SET end_time=? WHERE licence_plate=? AND end_time IS NULL", (str(time.time()), str(license_plate), ))
        self.conn.commit()

    def get_car_by_plate(self, license_plate):
        car = self.c.execute("SELECT * FROM car_parked WHERE licence_plate=?", (license_plate, )).fetchone()
        return self.create_parked_car_dict(car)

    def create_array_dict(self, cars, parked=False):
        result = []
        for car in cars:
            if parked:
                result.append(self.create_parked_car_dict(car))
            else:
                result.append(self.create_car_dict(car))
        return result

    def create_parked_car_dict(self, car):
        car_dict = {
            'id': car[0],
            'license_plate': car[1],
            'register_time': car[2],
            'status': car[3]
        }
        licence_plate = car[1]
        cars_general_query = self.c.execute("SELECT * FROM car WHERE licence_plate=?", (str(licence_plate), ))
        cars_general = cars_general_query.fetchall()
        for car_general in cars_general:
            car_dict['info'] = self.encryptor.decrypt(car_general[2])
            car_dict['image_path'] = car_general[3]
        return car_dict

    def create_car_dict(self, car):
        parked = self.c.execute("SELECT * from car_parked WHERE licence_plate=? AND end_time IS NULL", (car[1], )).fetchone()
        car_dict = {
            'id': car[0],
            'license_plate': car[1],
            'info': car[2],
            'image_path': car[3],
            'parked': True if parked else False
        }
        return car_dict