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

@app.route("/sensor/<string:sensor_type>/reading", methods=["POST"])
def add_reading(sensor_type):
    """ Assigns a sequence number to the reading and returns the created reading """

    if sensor_type == "temperature":
        reading_manager = TemperatureReadingManager(temp_readings_file)
    elif sensor_type == "pressure":
        reading_manager = PressureReadingManager(pres_readings_file)
    else:
        return app.response_class(status=400)    

    json_reading = request.get_json(silent=True)
    reading = create_reading(sensor_type, json_reading)
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

@app.route("/sensor/<string:sensor_type>/reading/<int:seq_num>", methods=["PUT"])
def update_reading(sensor_type, seq_num):
    """ Updates a reading based on sequence number """

    if sensor_type == "temperature":
        reading_manager = TemperatureReadingManager(temp_readings_file)
    elif sensor_type == "pressure":
        reading_manager = PressureReadingManager(pres_readings_file)
    else:
        return app.response_class(status=400)

    json_reading = request.get_json(silent=True)
    reading = create_reading(sensor_type, json_reading, seq_num)

    if reading:
        if reading_manager.update_reading(reading):
            response = app.response_class(status=200)
        else:
            response = app.response_class(status=404, response="Reading is not found")  
    else:
        response = app.response_class(status=400)

    return response

@app.route("/sensor/<string:sensor_type>/reading/<int:seq_num>", methods=["DELETE"])
def delete_reading(sensor_type, seq_num):
    """ Delete a reading from csv file based on sequence number """

    if sensor_type == "temperature":
        reading_manager = TemperatureReadingManager(temp_readings_file)
    elif sensor_type == "pressure":
        reading_manager = PressureReadingManager(pres_readings_file)
    else:
        return app.response_class(status=400)

    if reading_manager.delete_reading(seq_num):
        response = app.response_class(status=200)
    else:
        response = app.response_class(status=404, response="Reading is not found")
    
    return response

@app.route("/sensor/<string:sensor_type>/reading/<int:seq_num>", methods=["GET"])
def get_reading(sensor_type, seq_num):
    """ Get a reading from csv file based on sequence number """

    if sensor_type == "temperature":
        reading_manager = TemperatureReadingManager(temp_readings_file)
    elif sensor_type == "pressure":
        reading_manager = PressureReadingManager(pres_readings_file)
    else:
        return app.response_class(status=400)

    reading = reading_manager.get_reading(seq_num)
    if reading:
        json_reading = reading.to_json()
        return app.response_class(
            response=json_reading,
            status=200,
            mimetype="application/json"
        )
    else:
        return app.response_class(status=404, response="Reading is not found")

@app.route("/sensor/<string:sensor_type>/reading/all", methods=["GET"])
def get_all_readings(sensor_type):
    """ Get a reading from csv file based on sequence number """

    if sensor_type == "temperature":
        reading_manager = TemperatureReadingManager(temp_readings_file)
    elif sensor_type == "pressure":
        reading_manager = PressureReadingManager(pres_readings_file)
    else:
        return app.response_class(status=400)
    
    readings = reading_manager.get_all_readings()
    dict_readings = []
    for reading in readings:
        # Convert reading object to a dictionary with values converted to a string
        reading_dict = dict((attr.replace("_", ""), str(v)) for attr, v in reading.__dict__.items())
        dict_readings.append(reading_dict)

    json_readings = json.dumps(dict_readings)

    response = app.response_class(
        response=json_readings,
        status=200,
        mimetype="application/json"
    )
    
    return response

def create_reading(sensor_type, json_reading, seq_num=0):
    """ Creates and returns tuple containing reading and reading manager """

    if sensor_type == "temperature":    
        try:
            reading = TemperatureReading(datetime.datetime.strptime(json_reading["timestamp"], "%Y-%m-%d %H:%M:%S.%f"),
                            seq_num, json_reading["model"], float(json_reading["min"]), float(json_reading["avg"]), 
                            float(json_reading["max"]), json_reading["status"])
        except:
            return None

    if sensor_type == "pressure":
        try:
            reading = PressureReading(datetime.datetime.strptime(json_reading["timestamp"], "%Y-%m-%d %H:%M"),
                        seq_num, json_reading["model"], float(json_reading["min"]), float(json_reading["avg"]),
                        float(json_reading["max"]), json_reading["status"])
        except:
            return None
        
    return reading
    


if __name__ == "__main__":
    app.run()