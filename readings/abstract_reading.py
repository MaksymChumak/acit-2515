import json

class AbstractReading:
    """ Abstract Sensor Reading """

    SENSOR_TIMESTAMP = "Timestamp"
    SENSOR_MODEL = "Sensor Model"
    READING_SEQ_NUM = "Sequence Number"
    READING_MIN = "Min"
    READING_AVG = "Average"
    READING_MAX = "Max"
    READING_STATUS = "Status"

    def __init__(self, timestamp, seq_num, sensor_model, min, avg, max, status):
        """ Initializes the sensor reading """

        if timestamp is not None:
            self._timestamp = timestamp
        else:
            raise ValueError("Date must be defined")
        
        AbstractReading._validate_int(AbstractReading.READING_SEQ_NUM, seq_num)
        self._sequence_num = seq_num
        AbstractReading._validate_string_input(AbstractReading.SENSOR_MODEL, sensor_model)
        self._sensor_model = sensor_model
        AbstractReading._validate_float(AbstractReading.READING_MIN, min)
        self._min = min
        AbstractReading._validate_float(AbstractReading.READING_AVG, avg)
        self._avg = avg
        AbstractReading._validate_float(AbstractReading.READING_AVG, max)
        self._max = max
        AbstractReading._validate_string_input(AbstractReading.READING_STATUS, status)
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
        """ Returns json object with reading data """

        reading_manager_data = {
            "timestamp": str(self.get_timestamp()),
            "sequence_num": str(self.get_sequence_num()), 
            "model": self.get_sensor_model(),
            "min": str(self.get_min_value()), 
            "avg": str(self.get_avg_value()),
            "max": str(self.get_max_value()),
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

    @staticmethod
    def _validate_string_input(display_name, input_value):
        """ Private helper to validate input values as not None or an empty string """

        if input_value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if input_value == "":
            raise ValueError(display_name + " cannot be empty.")

    @staticmethod
    def _validate_int(display_name, input_value):
        """ Private method to validate the input value is an integer type """

        if type(input_value) != int:
            raise ValueError(display_name, " must be an integer type")

    @staticmethod
    def _validate_float(display_name, input_value):
        """ Private method to validate the input value is a float type """

        if type(input_value) != float:
            raise ValueError(display_name, " must be a float type")
