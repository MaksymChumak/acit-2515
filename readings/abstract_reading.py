import json

class AbstractReading:
    """ Abstract Sensor Reading """

    def __init__(self, timestamp, seq_num, sensor_model, min, avg, max, status):
        """ Initializes the sensor reading """

        self._timestamp = timestamp
        self._sequence_num = seq_num
        self._sensor_model = sensor_model
        self._min = min
        self._avg = avg
        self._max = max
        self._status = status

    def get_timestamp(self):
        """ Getter for timestamp """

        return self._timestamp

    def get_sensor_model(self):
        """ Getter for sensor model """

        return self._sensor_model

    def get_sequence_num(self):
        """ Getter for sequence number """

        return self._sequence_num

    def get_min_value(self):
        """ Getter for the minimum temperature """

        return self._min

    def get_avg_value(self):
        """ Getter for the average temperature """

        return self._avg

    def get_max_value(self):
        """ Getter for the maximum temperature """

        return self._max

    def get_range(self):
        """ Getter for the temperature range """

        return self._max - self._min

    def get_status(self):
        """ Getter for status """

        return self._status

    def set_sequence_num(self, sequence_num):
        """ Setter for sequence number """

        self._sequence_num = sequence_num

    def to_json(self):
        """ Returns json string with reading data """

        reading_manager_data = {
            "timestamp": str(self.get_timestamp()),
            "sequence_num": self.get_sequence_num(), 
            "model": self.get_sensor_model(),
            "min": self.get_min_value(), 
            "avg": self.get_avg_value(),
            "max": self.get_max_value(),
            "status": self.get_status()
        }
        json_string = json.dumps(reading_manager_data, indent=4)
        return json_string

    def is_error(self):
        """ Abstract Method - Is Reading an Error """

        raise NotImplementedError("Must be implemented")

    def get_error_msg(self):
        """ Abstract Method - Get Error Readings """
        
        raise NotImplementedError("Must be implemented")
