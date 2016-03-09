__author__ = 'Brandon Dockery'

import os
import subprocess
import codecs

_DEFAULT_UI_DUMP_FILEPATH = "windowdump.xml"
_DEVICE_STORAGE_DIRECTORY = "/storage/emulated/legacy/"

_ADB_LOCATION = None
_FNULL = open(os.devnull, 'w')
_startupinfo = subprocess.STARTUPINFO()
_startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

if 'adb.exe' in os.environ.get('PATH'):
    _ADB_LOCATION = 'adb.exe'
elif os.environ.get('ANDROID_SDK_HOME'):
    _ADB_LOCATION = os.environ.get('ANDROID_SDK_HOME') + "/platform-tools/adb.exe"


def set_adb_location(adb_location):
    global _ADB_LOCATION
    _ADB_LOCATION = adb_location


def set_device_storage_directory(folder_name):
    global _DEVICE_STORAGE_DIRECTORY
    _DEVICE_STORAGE_DIRECTORY = folder_name


def swipe(start_x, start_y, end_x, end_y, device_identifier=None):
    if(device_identifier == None):
         _call_subprocess_with_no_window(
            "{0} shell input swipe {1} {2} {3} {4}".format(_ADB_LOCATION, str(start_x),
                                                                  str(start_y), str(end_x),
                                                                  str(end_y)))
    else:
        _call_subprocess_with_no_window(
            "{0} -s {1} shell input swipe {2} {3} {4} {5}".format(_ADB_LOCATION, device_identifier, str(start_x),
                                                                  str(start_y), str(end_x),
                                                                  str(end_y)))


def tap(tap_x, tap_y, device_identifier=None):
    if(device_identifier == None):
        _call_subprocess_with_no_window(
            "{0} shell input tap {1} {2}".format(_ADB_LOCATION, str(tap_x),
                                                       str(tap_y)))
    else:
        _call_subprocess_with_no_window(
            "{0} -s {1} shell input tap {2} {3}".format(_ADB_LOCATION, device_identifier, str(tap_x),
                                                       str(tap_y)))

def back():
    _call_subprocess_with_no_window(_get_input_key_event_string(4))

def home():
    _call_subprocess_with_no_window(_get_input_key_event_string(3))

def _get_input_key_event_string(keycode):
    return "{0} shell input keyevent {1}".format(_ADB_LOCATION, str(keycode))

def screencap(target_uri=None, device_identifier=None):
    if target_uri == None and device_identifier != None:
         _call_subprocess_with_no_window("{0} -s {1} shell screencap -p {2}screen.png".format(_ADB_LOCATION, device_identifier, _DEVICE_STORAGE_DIRECTORY))
    elif target_uri == None and device_identifier == None:
         _call_subprocess_with_no_window("{0} shell screencap -p {1}screen.png".format(_ADB_LOCATION, _DEVICE_STORAGE_DIRECTORY))
    elif target_uri != None and device_identifier == None:
        screencap(None,None)
        _call_subprocess_with_no_window(
            "{0} pull {1}screen.png {2}".format(_ADB_LOCATION, _DEVICE_STORAGE_DIRECTORY, target_uri))
    else:
        screencap(None,device_identifier)
        _call_subprocess_with_no_window(
            "{0} -s {1} pull {2}screen.png {3}".format(_ADB_LOCATION, device_identifier, _DEVICE_STORAGE_DIRECTORY, target_uri))


def get_layout_xml(device_identifier=None):
    if(device_identifier == None):
        dump_layout_xml_to_file(_DEFAULT_UI_DUMP_FILEPATH)
        dump_file = open(_DEFAULT_UI_DUMP_FILEPATH, 'r')
        dump_contents = dump_file.read().decode("utf-8")
        dump_file.close()
        os.remove(_DEFAULT_UI_DUMP_FILEPATH)
        return dump_contents
    else:
        dump_layout_xml_to_file(_DEFAULT_UI_DUMP_FILEPATH, device_identifier)
        #dump_file = open(_DEFAULT_UI_DUMP_FILEPATH, 'r')
        dump_file = codecs.open(_DEFAULT_UI_DUMP_FILEPATH, 'r', 'utf-8')#dump_file.read().decode("utf-8")
        dump_contents = dump_file.read()
        dump_file.close()
        os.remove(_DEFAULT_UI_DUMP_FILEPATH)
        return dump_contents

def dump_layout_xml_to_file(target_uri,device_identifier=None):
    if(device_identifier == None):
        _call_subprocess_with_no_window("{0} shell uiautomator dump --verbose".format(_ADB_LOCATION))
        _call_subprocess_with_no_window(
            "{0} pull {1}window_dump.xml {2}".format(_ADB_LOCATION, _DEVICE_STORAGE_DIRECTORY, target_uri))
    else:
        _call_subprocess_with_no_window("{0} -s {1} shell uiautomator dump --verbose".format(_ADB_LOCATION, device_identifier))
        print("Layout XML dumped in device")
        _call_subprocess_with_no_window(
        "{0} -s {1} pull {2}window_dump.xml {3}".format(_ADB_LOCATION, device_identifier, _DEVICE_STORAGE_DIRECTORY, target_uri))
        print("Layout XML pulled from device")


def get_current_activity():
    dumpsys_output = str(_call_subprocess_with_no_window("{0} shell dumpsys activity".format(_ADB_LOCATION)))

    for line in dumpsys_output.split("\\r\\r\\n"):
        stripped_line = line.rstrip().lstrip()

        if "Run #" in stripped_line:
            return stripped_line.split("/")[1].split(" ")[0].split(".")[-1]

def _call_subprocess_with_no_window(command_to_call):
    try:
        return subprocess.check_output(command_to_call, stderr=_FNULL, shell=False, startupinfo=_startupinfo)
    except subprocess.CalledProcessError:
        #subprocess.check_output("{0} kill-server".format(_ADB_LOCATION), stderr=_FNULL, shell=False, startupinfo=_startupinfo)
        print("Lost connection to the device. Please reconnect and run adb tcpip 5555, disconnect, then run adb connect <IP ADDRESS>")
