import csv

class AbstractReadingManager:
    """ Abstract Reading Manager """

    FILENAME = "File Name"
    SEQ_NUM = "Sequence Number"

    def __init__(self, filename):
        """ Initializes the reading manager """

        AbstractReadingManager._validate_string_input(AbstractReadingManager.FILENAME, filename)
        self._filename = filename
        self._readings = []
        self._read_reading_from_file()

    def add_reading(self, reading):
        """ Adds reading to a csv file """
        
        if not reading:
            return None

        # Set new reading's seq num to largest sequence number in the readings list + 1
        for r in self._readings:
            if r.get_sequence_num() > reading.get_sequence_num():
                reading.set_sequence_num(r.get_sequence_num())
        reading.set_sequence_num(reading.get_sequence_num() + 1)

        self._readings.append(reading)
        self._write_reading_row(reading)

    def update_reading(self, reading):
        """ Updates reading in a csv file """

        if not self._readings or reading.__class__ != self._readings[0].__class__:
            return None

        count = 0
        for i, r in enumerate(self._readings):
            if r.get_sequence_num() == reading.get_sequence_num():
                self._readings[i] = reading
                count += 1
        self._write_readings_to_file()
        return count

    def delete_reading(self, seq_num):
        """ Deletes reading from a csv file """

        AbstractReadingManager._validate_int(AbstractReadingManager.SEQ_NUM, seq_num)
        count = 0
        for i, r in enumerate(self._readings):
            if r.get_sequence_num() == seq_num:
                self._readings.pop(i)
                count += 1
        self._write_readings_to_file()
        return count

    def get_reading(self, seq_num):
        """ Returns reading that mathes sequence number from a scv file """

        AbstractReadingManager._validate_int(AbstractReadingManager.SEQ_NUM, seq_num)
        reading = None
        for r in self._readings:
            if r.get_sequence_num() == seq_num:
                reading = r
        return reading
        
    def get_all_readings(self):
        """ Returns a list of all readings """

        return self._readings

    def _read_reading_from_file(self):
        """ Reads reading from a csv file """

        with open(self._filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                reading = self._load_reading_row(row)
                self._readings.append(reading)

        self._readings.sort(key=lambda reading: reading.get_sequence_num())

    def _write_readings_to_file(self):
        """ Writes readings to a csv file """
        
        readings = []
        for reading in self._readings:
            lreading = self._reading_to_list(reading)
            readings.append(lreading)
            
        with open(self._filename, mode="w", newline="") as f:
            reading_writer = csv.writer(f, delimiter=",")
            reading_writer.writerows(readings)

    def _load_reading_row(self, row):
        """ Abstract Method - Gets reading from a csv file """

        raise NotImplementedError("Must be implemented")

    def _write_reading_row(self, reading):
        """ Abstract Method - Writes reading to a csv file """

        raise NotImplementedError("Must be implemented")

    def _reading_to_list(self, reading):
        """ Abstract Method - Returns reading object formated as list """

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