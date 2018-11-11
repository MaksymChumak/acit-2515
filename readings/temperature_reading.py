from readings.abstract_reading import AbstractReading


class TemperatureReading(AbstractReading):
    """ Concrete Implementation of a Temperature Reading """

    # CONSTANTS
    HIGH_TEMP_ERROR = "HIGH_TEMP"
    LOW_TEMP_ERROR = "LOW_TEMP"
    STATUS_OK = "OK"
    DEGREE_SIGN = u'\N{DEGREE SIGN}'

    def is_error(self):
        """ Returns True if there's a there's an error and False if there is no error """

        if self._status != TemperatureReading.STATUS_OK:
            return True

        return False

    def get_error_msg(self):
        """ Returns the error message (or None if not an error) """

        status_display = None
        reading_display_datetime = self._timestamp.strftime('%Y/%m/%d %H:%M')
        reading_seq_num = self._sequence_num

        if self._status == TemperatureReading.HIGH_TEMP_ERROR:
            status_display = "High Temperature (100%cC) at %s, Sequence: %d" % (TemperatureReading.DEGREE_SIGN, reading_display_datetime, reading_seq_num)
        elif self._status == TemperatureReading.LOW_TEMP_ERROR:
            status_display = "Low Temperature (-50%cC) at %s, Sequence: %d" % (TemperatureReading.DEGREE_SIGN, reading_display_datetime, reading_seq_num)

        return status_display
