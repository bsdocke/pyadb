DEFAULT_UI_DUMP_FILEPATH = "windowdump.xml"
__author__ = 'Brandon'

import os
import subprocess

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


def swipe(device_identifier, start_x, start_y, end_x, end_y):
    _call_subprocess_with_no_window(
        "{0} -s {1} shell input swipe {2} {3} {4} {5}".format(_ADB_LOCATION, device_identifier, str(start_x),
                                                              str(start_y), str(end_x),
                                                              str(end_y)))


def swipe(start_x, start_y, end_x, end_y):
    _call_subprocess_with_no_window(
        "{0} shell input swipe {1} {2} {3} {4}".format(_ADB_LOCATION, str(start_x), str(start_y), str(end_x),
                                                       str(end_y)))


def tap(device_identifier, tap_x, tap_y):
    _call_subprocess_with_no_window(
        "{0} -s {1} shell input tap {2} {3}".format(_ADB_LOCATION, device_identifier, str(tap_x),
                                                    str(tap_y)))


def tap(tap_x, tap_y):
    _call_subprocess_with_no_window(
        "{0} shell input tap {1} {2}".format(_ADB_LOCATION, str(tap_x), str(tap_y)))

def back():
    _call_subprocess_with_no_window("{0} shell input keyevent 4".format(_ADB_LOCATION))

def screencap():
    _call_subprocess_with_no_window(_ADB_LOCATION + " shell screencap -p /storage/emulated/legacy/screen.png")


def screencap(target_uri):
    screencap()
    _call_subprocess_with_no_window(_ADB_LOCATION + " pull /storage/emulated/legacy/screen.png " + target_uri)

def get_layout_xml():
    dump_layout_xml_to_file(DEFAULT_UI_DUMP_FILEPATH)
    dump_file = open(DEFAULT_UI_DUMP_FILEPATH, 'r')
    dump_contents = dump_file.read()
    dump_file.close()
    os.remove(DEFAULT_UI_DUMP_FILEPATH)
    return dump_contents

def dump_layout_xml_to_file(target_uri):
    _call_subprocess_with_no_window("{0} shell uiautomator dump --verbose".format(_ADB_LOCATION))
    _call_subprocess_with_no_window(
        "{0} pull /storage/emulated/legacy/window_dump.xml {1}".format(_ADB_LOCATION, target_uri))


def _call_subprocess_with_no_window(command_to_call):
    subprocess.call(command_to_call, stdout=_FNULL, stderr=_FNULL, shell=False, startupinfo=_startupinfo)