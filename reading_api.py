from flask import Flask
from flask import request
import datetime
import json

from managers.temperature_reading_manager import TemperatureReadingManager
from managers.pressure_reading_manager import PressureReadingManager
from readings.temperature_reading import TemperatureReading
from readings.pressure_reading import PressureReading

temp_readings_file = "data/temperature_readings.csv"
pres_readings_file = "data/pressure_readings.csv"

app = Flask(__name__)

@app.route("/sensor/<string:reading_type>/reading", methods=["POST"])
def add_reading(reading_type):
    """ Assigns a sequence number to the reading and returns the created reading """

    json_reading = request.get_json(silent=True)
    objects = extract_data_from_json(reading_type, json_reading)
    reading_manager = objects[0]
    reading = objects[1]
    if reading:
        reading_manager.add_reading(reading)
        new_json_reading = reading.to_json()
        response = app.response_class(
            response=new_json_reading,
            status=200,
            mimetype="application/json"
        )
    else: 
        response = app.response_class(status=400)

    return response

@app.route("/sensor/<string:reading_type>/reading/<int:seq_num>", methods=["PUT"])
def update_reading(reading_type, seq_num):
    """ Updates a reading based on sequence number """

    json_reading = request.get_json(silent=True)
    objects = extract_data_from_json(reading_type, json_reading, seq_num)
    reading_manager = objects[0]
    reading = objects[1]

    if reading:
        reading_manager.update_reading(reading)
        response = app.response_class(status=200)
    else:
        response = app.response_class(status=400)

    return response

@app.route("/sensor/<string:reading_type>/reading/<int:seq_num>", methods=["DELETE"])
def delete_reading(reading_type, seq_num):
    """ Delete a reading from csv file based on sequence number """

    if reading_type == "temperature":
        reading_manager = TemperatureReadingManager(temp_readings_file)
    elif reading_type == "pressure":
        reading_manager = PressureReadingManager(pres_readings_file)
    else:
        return app.response_class(status=400)

    reading_manager.delete_reading(seq_num)
    response = app.response_class(status=200)
    
    return response

@app.route("/sensor/<string:reading_type>/reading/<int:seq_num>", methods=["GET"])
def get_reading(reading_type, seq_num):
    """ Get a reading from csv file based on sequence number """

    if reading_type == "temperature":
        reading_manager = TemperatureReadingManager(temp_readings_file)
    elif reading_type == "pressure":
        reading_manager = PressureReadingManager(pres_readings_file)
    else:
        return app.response_class(status=400)

    reading = reading_manager.get_reading(seq_num)
    json_reading = reading.to_json()
    response = app.response_class(
        response=json_reading,
        status=200,
        mimetype="application/json"
    )
    return response


@app.route("/sensor/<string:reading_type>/reading/all", methods=["GET"])
def get_all_readings(reading_type):
    """ Get a reading from csv file based on sequence number """

    if reading_type == "temperature":
        reading_manager = TemperatureReadingManager(temp_readings_file)
    elif reading_type == "pressure":
        reading_manager = PressureReadingManager(pres_readings_file)
    else:
        return app.response_class(status=400)
    
    readings = reading_manager.get_all_readings()
    json_readings = []
    for reading in readings:
        json_reading = reading.to_json()
        json_readings.append(json_reading)

    response = app.response_class(
        response=json_readings,
        status=200,
        mimetype="application/json"
    )
    
    return response

def extract_data_from_json(reading_type, json_reading, seq_num=0):
    """ Creates and returns reading and reading manager from json object """

    if reading_type == "temperature" and json_reading:
        reading_manager = TemperatureReadingManager(temp_readings_file)
        reading = TemperatureReading(datetime.datetime.strptime(json_reading["timestamp"], "%Y-%m-%d %H:%M:%S.%f"),
                        seq_num, json_reading["model"], float(json_reading["min"]), float(json_reading["avg"]), 
                        float(json_reading["max"]), json_reading["status"])
    elif reading_type == "pressure" and json_reading:
        reading_manager = PressureReadingManager(pres_readings_file)
        reading = PressureReading(datetime.datetime.strptime(json_reading["timestamp"], "%Y-%m-%d %H:%M"),
                        seq_num, json_reading["model"], float(json_reading["min"]), float(json_reading["avg"]),
                        float(json_reading["max"]), json_reading["status"])
    else:
        reading = None

    return (reading_manager, reading)
    


if __name__ == "__main__":
    app.run()