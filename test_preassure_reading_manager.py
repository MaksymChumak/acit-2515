from managers.pressure_reading_manager import PressureReadingManager
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch,mock_open
import datetime
import inspect
import csv

class TestTemperatureReadingManager(TestCase):
    """ Unit Tests for the TemperatureReadingManager Class """

    def logPoint(self):
        """ Display test specific information """

        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print('in %s - %s()' % (currentTest, callingFunction))

    def setUp(self):
        """ Creates fixtures before each test """

        self.logPoint()
        reading_datetime = datetime.datetime.strptime("2018-09-23 19:56:01.345", "%Y-%m-%d %H:%M:%S.%f")
        self.temp_reading = TemperatureReading(reading_datetime, "1", "ABC Sensor Temp M301A", "20.152", "21.367", "22.005", "OK")

    def tearDown(self):
        """ Create a test fixture after each test method is run """
        
        self.logPoint()
