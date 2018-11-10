import csv

class AbstractReadingManager:
    """ Abstract Reading Manager """

    def __init__(self, filename):
        """ Initializes the reading manager """
        
        self._filename = filename
        self._readings = []
        self._read_reading_from_file()

    def add_reading(self, reading):
        """ Adds reading to a csv file """

        # Set new reading's seq num to largest sequence number in the readings list + 1
        for r in self._readings:
            if r.get_sequence_num() > reading.get_sequence_num():
                reading.set_sequence_num(r.get_sequence_num())
        reading.set_sequence_num(reading.get_sequence_num() + 1)

        self._readings.append(reading)
        self._write_reading_row(reading)


    def update_reading(self, reading):
        """ Updates reading in a csv file """

        for i, r in enumerate(self._readings):
            if r.get_sequence_num() == reading.get_sequence_num():
                self._readings[i] = reading
        self._write_readings_to_file()


    def delete_reading(self, seq_num):
        """ Deletes reading from a csv file """

        for i, r in enumerate(self._readings):
            if r.get_sequence_num() == seq_num:
                self._readings.pop(i)
        self._write_readings_to_file()

        

    def get_reading(self, seq_num):
        """ Returns reading that mathes sequence number from a scv file """

        for reading in self._readings:
            if reading.get_sequence_num() == seq_num:
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