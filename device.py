import pyadb


class Device:
    device_id = None

    def __init__(self, device_id):
        self.device_id = device_id

    def kill_application(self,application_name):
        pyadb._call_subprocess_with_no_window(
            "{0} -s {1} shell am force-stop {2}".format(pyadb._get_adb_location(), self.device_id, application_name))

    '''
    Closes the currently opened application on the specified device
    '''

    def kill_current_application(self):
        pyadb._call_subprocess_with_no_window("{0} -s {1} shell am force-stop {2}".format(pyadb._get_adb_location(), self.device_id,
                                                                                    self.get_current_application_package(self
                                                                                        )))

    '''
    Returns a string which is the package name of the current application open on the specified device
    '''
    def get_current_application_package(self):

        dumpsys_output = str(
            pyadb._call_subprocess_with_no_window("{0} -s {1} shell dumpsys window windows".format(pyadb._get_adb_location(),
                                                                                                 self.device_id)))
        return dumpsys_output.split("mCurrentFocus")[-1].split("/")[0].split(" ")[-1]


    '''
    Simulates a tap on a given device at coordinates
    '''
    def tap(self, tap_x, tap_y):
            pyadb._call_subprocess_with_no_window(
                "{0} -s {1} shell input tap {2} {3}".format(pyadb._get_adb_location(), self.device_id, str(tap_x),
                                                            str(tap_y)))

    '''
    Simulates a finger swipe on the specified device, from one point to another over a given duration in milliseconds
    '''
    def swipe(self,start_x, start_y, end_x, end_y, duration=500):
            pyadb._call_subprocess_with_no_window(
                "{0} -s {1} shell input swipe {2} {3} {4} {5} {6}".format(pyadb._get_adb_location(), self.device_id,
                                                                          str(start_x),
                                                                          str(start_y), str(end_x),
                                                                          str(end_y), duration))

    '''
    Simulates pressing of the back button on a device
    '''

    # TODO move this function to be with the other input simulation functions
    def back(device_id=None):
        _call_subprocess_with_no_window(_get_input_key_event_string(4, device_id))

    '''
    Simulates the pressing of the Home button on a device
    '''

    def home(device_id=None):
        _call_subprocess_with_no_window(_get_input_key_event_string(3, device_id))
