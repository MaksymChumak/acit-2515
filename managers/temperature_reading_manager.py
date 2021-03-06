from managers.abstract_reading_manager import AbstractReadingManager
from readings.temperature_reading import TemperatureReading
import datetime
import csv

class TemperatureReadingManager(AbstractReadingManager):
    """ Temperature Reading Manager """

    TIMESTAMP_INDEX = 0
    SEQ_NUM_INDEX = 1
    SENSOR_MODEL_INDEX = 2
    MIN_INDEX = 3
    AVG_INDEX = 4
    MAX_INDEX = 5
    STATUS_INDEX = 6

    def _load_reading_row(self, row):
        """ Loads list into a TemperatureReading object """
        
        try:
            reading_datetime = datetime.datetime.strptime(row[TemperatureReadingManager.TIMESTAMP_INDEX], "%Y-%m-%d %H:%M:%S.%f")
            temp_reading = TemperatureReading(reading_datetime,
                                int(row[TemperatureReadingManager.SEQ_NUM_INDEX]),
                                row[TemperatureReadingManager.SENSOR_MODEL_INDEX],
                                float(row[TemperatureReadingManager.MIN_INDEX]),
                                float(row[TemperatureReadingManager.AVG_INDEX]),
                                float(row[TemperatureReadingManager.MAX_INDEX]),
                                row[TemperatureReadingManager.STATUS_INDEX])
        except:
            raise ValueError("Invalid data entry")

        return temp_reading
    
    def _reading_to_list(self, reading):
        """ Returns reading object formated as a list of strings """

        try:
            temp_reading = [str(reading.get_timestamp()), str(reading.get_sequence_num()), 
                            reading.get_sensor_model(), str(reading.get_min_value()), 
                            str(reading.get_avg_value()), str(reading.get_max_value()), reading.get_status()]
        except:
            raise ValueError("Invalid data entry")

        return temp_reading


    def _write_reading_row(self, reading):
        """ Writes reading to a csv file """

        if not reading:
            raise ValueError("Invalid data entry")

        temp_reading = self._reading_to_list(reading)
        
        with open(self._filename, "a") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(temp_reading)
