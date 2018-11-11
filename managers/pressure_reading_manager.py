from managers.abstract_reading_manager import AbstractReadingManager
from readings.pressure_reading import PressureReading
import datetime
import csv

class PressureReadingManager(AbstractReadingManager):
    """ Pressure Reading Manager """

    TIMESTAMP_INDEX = 0
    SENSOR_NAME_INDEX = 1
    SEQ_NUM_INDEX = 2
    MIN_INDEX = 3
    AVG_INDEX = 4
    MAX_INDEX = 5
    STATUS_INDEX = 6


    def _load_reading_row(self, row):
        """ Loads list into a PressureReading object """

        try:
            reading_datetime = datetime.datetime.strptime(row[PressureReadingManager.TIMESTAMP_INDEX], "%Y-%m-%d %H:%M:%S")
            pres_reading =  PressureReading(reading_datetime,
                                int(row[PressureReadingManager.SEQ_NUM_INDEX]),
                                row[PressureReadingManager.SENSOR_NAME_INDEX],
                                float(row[PressureReadingManager.MIN_INDEX]),
                                float(row[PressureReadingManager.AVG_INDEX]),
                                float(row[PressureReadingManager.MAX_INDEX]),
                                row[PressureReadingManager.STATUS_INDEX])
        except:
            raise ValueError("Invalid data entry")

        return pres_reading

    def _reading_to_list(self, reading):
        """ Returns reading object formated as list of strings """

        try:
            pres_reading = [str(reading.get_timestamp()), reading.get_sensor_model(), 
                            str(reading.get_sequence_num()), str(reading.get_min_value()), 
                            str(reading.get_avg_value()), str(reading.get_max_value()), reading.get_status()]
        except:
            raise ValueError("Invalid data entry")

        return pres_reading

    def _write_reading_row(self, reading):
        """ Writes reading to a csv file """

        if not reading:
            raise ValueError("Invalid data entry")

        pres_reading = self._reading_to_list(reading)
        
        with open(self._filename, "a") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(pres_reading)
            