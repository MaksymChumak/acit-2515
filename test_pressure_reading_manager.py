from managers.pressure_reading_manager import PressureReadingManager
from readings.pressure_reading import PressureReading
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch,mock_open
import datetime
import inspect
import csv
import os

class TestPressureReadingManager(TestCase):
    """ Unit Tests for the PressureReadingManager Class """

    TEST_PRES_READINGS = [
            ["2018-09-23 19:56", "ABC Sensor Pres M100", "1", "50.163", "51.435", "52.103", "GOOD"],
            ["2018-09-23 20:00", "ABC Sensor Pres M100", "2", "100.000", "100.000", "100.000", "HIGH_PRESSURE"],
            ["2018-09-23 20:06", "ABC Sensor Pres M100", "3", "0.000", "0.000", "0.000", "LOW_PRESSURE"] ]

    def logPoint(self):
        """ Display test specific information """

        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print('in %s - %s()' % (currentTest, callingFunction))

    @patch('builtins.open', mock_open(read_data='1'))
    def setUp(self, test_readings=TEST_PRES_READINGS):
        """ Creates fixtures before each test """

        self.logPoint()
        # This mocks the csv reader to return our test readings
        csv.reader = MagicMock(return_value=test_readings)
        self.reading_manager = PressureReadingManager("pres_testresults.csv")

        reading_datetime = datetime.datetime.strptime("2018-09-23 19:56", "%Y-%m-%d %H:%M")
        self.reading = PressureReading(reading_datetime, 1, "ABC Sensor Pres M100", 50.163, 51.435, 52.103, "GOOD")
        self.reading_update = PressureReading(reading_datetime, 1, "ABC Sensor Pres M100", 50.163, 51.435, 52.103, "UPDATED")

    def tearDown(self):
        """ Create a test fixture after each test method is run """

        try: 
            os.remove("pres_testresults.csv")
        except:
            pass
            
        self.logPoint()

    def test_constructor_fail(self):
        """ 010A - Raises ValueError when filepath is empty """

        with self.assertRaises(ValueError):
            self.temp_sensor = PressureReadingManager("")
            self.temp_sensor = PressureReadingManager(None)

    def test_constructor_success(self):
        """ 010B - Creates a PressureReadingManager instance """

        self.assertIsInstance(self.reading_manager, PressureReadingManager, "Must create a pressure reading manager with valid attributes")

    def test_add_reading_list_success(self):
        """ 020A - Adds a PressureReading to a list of readings """

        self.setUp([])
        intial_len = len(self.reading_manager.get_all_readings())
        self.reading_manager.add_reading(self.reading)
        self.assertEqual(len(self.reading_manager.get_all_readings()), intial_len + 1, "Must add reading to the list of readings")

    def test_add_reading_file_success(self):
        """ 020B - Writes a PressureReading to a csv file """

        open("pres_testresults.csv", 'w').close()
        self.setUp([])
        with open("pres_testresults.csv") as f:
            initial_num_rows = sum(1 for line in f)

        self.reading_manager.add_reading(self.reading)

        with open("pres_testresults.csv") as f:
            final_num_rows = sum(1 for line in f)

        self.assertEqual(initial_num_rows + 1, final_num_rows, "Must write reading to the csv file")

    def test_add_reading_seq_num_success(self):
        """ 020C - Creates seq num for new readings """

        self.setUp([])
        self.reading_manager.add_reading(self.reading)
        first_add_seq = self.reading_manager.get_all_readings()[0].get_sequence_num()
        self.reading_manager.add_reading(self.reading)
        second_add_seq = self.reading_manager.get_all_readings()[0].get_sequence_num()
        self.assertEqual(first_add_seq, second_add_seq - 1, "Must create seq num for new readings")

    def test_add_reading_fail(self):
        """ 020D - Returns None if input is invalid """

        self.setUp([])
        self.assertEqual(self.reading_manager.add_reading(None), None, "Must return none for invalid input")

    def test_update_reading_list_success(self):
        """ 030A - Updates PressureReading in a list of readings """

        self.reading_manager.update_reading(self.reading_update)
        self.assertEqual(self.reading_manager.update_reading(self.reading_update), 1, "Must update reading in the list of readings")

    def test_update_reading_invalid_input_fail(self):
        """ 030B - Returns None if the input is invalid """

        self.assertEqual(self.reading_manager.update_reading(None), None, "Must return None if the input is invalid")

    def test_update_reading_not_in_list_fail(self):
        """ 030C - Doesn't update reading if not in the list """

        reading_datetime = datetime.datetime.strptime("2018-09-23 19:56", "%Y-%m-%d %H:%M")
        reading_update_fail = PressureReading(reading_datetime, 0, "ABC Sensor Pres M100", 50.163, 51.435, 52.103, "UPDATED")
        self.assertEqual(self.reading_manager.update_reading(reading_update_fail), 0, "Must return 0 if seq num is not in the list")
        
    def test_delete_reading_list_success(self):
        """ 040A - Deletes a PressureReading from a list of readings """

        intial_len = len(self.reading_manager.get_all_readings())
        self.reading_manager.delete_reading(1)
        self.assertEqual(len(self.reading_manager.get_all_readings()), intial_len - 1, "Must delete reading from the list of readings")

    def test_delete_reading_file_success(self):
        """ 040B - Deletes a PressureReading from a csv file """

        initial_num_rows = len(self.reading_manager.get_all_readings())

        self.reading_manager.delete_reading(1)

        with open("pres_testresults.csv") as f:
            final_num_rows = sum(1 for line in f)

        self.assertEqual(initial_num_rows - 1, final_num_rows, "Must delete reading from the csv file")

    def test_delete_reading_invalid_input_fail(self):
        """ 040C - Raises ValueError when input is invalid """
        
        with self.assertRaises(ValueError):
            self.reading_manager.delete_reading(None)

    def test_delete_reading_not_in_list_fail(self):
        """ 040D - Fails to delete reading if not in the list """
        
        initial_num_rows = len(self.reading_manager.get_all_readings())

        self.reading_manager.delete_reading(0)

        with open("pres_testresults.csv") as f:
            final_num_rows = sum(1 for line in f)

        self.assertEqual(initial_num_rows, final_num_rows, "Must not delete reading from the csv file")

    def test_get_reading_success(self):
        """ 050A - Gets a PressureReading from a list of readings """

        test_reading = self.reading_manager.get_reading(1)
        self.assertEqual(self.reading_manager.get_all_readings()[0], test_reading, "Must get reading from the list of readings")

    def test_get_reading_invalid_input_fail(self):
        """ 050B - Fails to get a PressureReading from a list of readings """

        with self.assertRaises(ValueError):
            self.reading_manager.get_reading(None)

    def test_get_reading_not_in_list_fail(self):
        """ 050C - Fails to get a PressureReading from a list of readings """

        self.assertEqual(self.reading_manager.get_reading(0), None, "Must return None if seq num is not in the list")

    def test_get_all_readings_success(self):
        """ 060A - Gets a PressureReading from a list of readings """

        test_readings = self.reading_manager.get_all_readings()
        self.assertEqual(test_readings, self.reading_manager.get_all_readings(), "Must get reading from the list of readings")

    def test_get_all_readings_empty_success(self):
        """ 060B - Returns empty list if the file is empty  """

        self.setUp([])
        test_readings = self.reading_manager.get_all_readings()
        self.assertEqual(test_readings, [], "Must return empty list if the file is empty")

    
    

   