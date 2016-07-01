import os
import random
import subprocess
import traceback

__author__ = 'Brandon Dockery'

_DEFAULT_UI_DUMP_FILE_PATH = "windowdump.xml"
_DEVICE_STORAGE_DIRECTORY = "/storage/emulated/legacy/"

_ADB_LOCATION = None
_FNULL = open(os.devnull, 'w')
_startupinfo = subprocess.STARTUPINFO()
_startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

if 'adb.exe' in os.environ.get('PATH'):
    _ADB_LOCATION = 'adb.exe'
elif os.environ.get('ANDROID_SDK_HOME'):
    _ADB_LOCATION = os.environ.get('ANDROID_SDK_HOME') + "/platform-tools/adb.exe"


def _get_adb_location():
    if _ADB_LOCATION is not None:
        return _ADB_LOCATION
    else:
        print(
            "Location of adb.exe not set. Please set environment variable ANDROID_SDK_HOME, " +
            "add adb.exe to PATH, or define adb location by pyadb.set_adb_location")


def set_adb_location(adb_location):
    global _ADB_LOCATION
    _ADB_LOCATION = adb_location


def set_device_storage_directory(folder_name):
    global _DEVICE_STORAGE_DIRECTORY
    _DEVICE_STORAGE_DIRECTORY = folder_name


def swipe(start_x, start_y, end_x, end_y, duration=500, device_identifier=None):
    if device_identifier is None:
        _call_subprocess_with_no_window(
            "{0} shell input swipe {1} {2} {3} {4} {5}".format(_get_adb_location(), str(start_x),
                                                               str(start_y), str(end_x),
                                                               str(end_y), duration))
    else:
        _call_subprocess_with_no_window(
            "{0} -s {1} shell input swipe {2} {3} {4} {5} {6}".format(_get_adb_location(), device_identifier,
                                                                      str(start_x),
                                                                      str(start_y), str(end_x),
                                                                      str(end_y), duration))


def tap(tap_x, tap_y, device_identifier=None):
    if device_identifier is None:
        _call_subprocess_with_no_window(
            "{0} shell input tap {1} {2}".format(_get_adb_location(), str(tap_x),
                                                 str(tap_y)))
    else:
        _call_subprocess_with_no_window(
            "{0} -s {1} shell input tap {2} {3}".format(_get_adb_location(), device_identifier, str(tap_x),
                                                        str(tap_y)))


def get_coordinates_of_element_from_text(layout_string, target):
    index_of_close_btn = layout_string.index(target)

    while layout_string[index_of_close_btn] != '[':
        index_of_close_btn += 1

    index_of_close_btn += 1
    start_pos = ""
    while layout_string[index_of_close_btn] != ']':
        start_pos = start_pos + layout_string[index_of_close_btn]
        index_of_close_btn += 1

    index_of_close_btn += 2

    end_pos = ""
    while layout_string[index_of_close_btn] != ']':
        end_pos += layout_string[index_of_close_btn]
        index_of_close_btn += 1

    pos_upper_left = start_pos.split(",")
    pos_lower_right = end_pos.split(",")

    click_x = int(random.randint(int(pos_upper_left[0]), int(pos_lower_right[0])))
    click_y = int(random.randint(int(pos_upper_left[1]), int(pos_lower_right[1])))

    return [click_x, click_y]


def back(device_id=None):
    _call_subprocess_with_no_window(_get_input_key_event_string(4, device_id))


def home(device_id=None):
    _call_subprocess_with_no_window(_get_input_key_event_string(3, device_id))


def _get_input_key_event_string(keycode, device_id=None):
    if device_id is None:
        return "{0} shell input keyevent {1}".format(_get_adb_location(), str(keycode))
    else:
        return "{0} -s {1} shell input keyevent {2}".format(_get_adb_location(), device_id, str(keycode))


def screencap(target_uri=None, device_identifier=None):
    if target_uri is None and device_identifier is not None:
        _call_subprocess_with_no_window(
            "{0} -s {1} shell screencap -p {2}screen.png".format(_get_adb_location(), device_identifier,
                                                                 _DEVICE_STORAGE_DIRECTORY))
    elif target_uri is None and device_identifier is None:
        _call_subprocess_with_no_window(
            "{0} shell screencap -p {1}screen.png".format(_get_adb_location(), _DEVICE_STORAGE_DIRECTORY))
    elif target_uri is not None and device_identifier is None:
        screencap(None, None)
        _call_subprocess_with_no_window(
            "{0} pull {1}screen.png {2}".format(_get_adb_location(), _DEVICE_STORAGE_DIRECTORY, target_uri))
    else:
        screencap(None, device_identifier)
        _call_subprocess_with_no_window(
            "{0} -s {1} pull {2}screen.png {3}".format(_get_adb_location(), device_identifier,
                                                       _DEVICE_STORAGE_DIRECTORY,
                                                       target_uri))


def get_layout_xml(device_identifier=None):
    _dump_layout_xml_on_device(device_identifier)
    return _get_layout_xml_string(device_identifier)


def _dump_layout_xml_on_device(device_identifier=None):
    if device_identifier is None:
        _call_subprocess_with_no_window("{0} shell uiautomator dump --verbose".format(_get_adb_location()))
    else:
        _call_subprocess_with_no_window(
            "{0} -s {1} shell uiautomator dump --verbose".format(_get_adb_location(), device_identifier))


def dump_layout_xml_to_file(target_uri, device_identifier=None):
    _dump_layout_xml_on_device(device_identifier)
    if device_identifier is None:
        _call_subprocess_with_no_window(
            "{0} pull {1}window_dump.xml {2}".format(_get_adb_location(), _DEVICE_STORAGE_DIRECTORY, target_uri))
    else:
        _call_subprocess_with_no_window(
            "{0} -s {1} pull {2}window_dump.xml {3}".format(_get_adb_location(), device_identifier,
                                                            _DEVICE_STORAGE_DIRECTORY,
                                                            target_uri))


def get_current_activity(device_id=None):
    return _get_current_activity_string(device_id).split(".")[-1]


def get_fully_qualified_current_activity(device_id=None):
    return _get_current_activity_string(device_id)


def _get_layout_xml_string(device_id=None):
    if device_id is None:
        dumped_layout_xml = str(_call_subprocess_with_no_window(
            "{0} shell cat {1}window_dump.xml".format(_get_adb_location(), _DEVICE_STORAGE_DIRECTORY)))
    else:
        dumped_layout_xml = str(_call_subprocess_with_no_window(
            "{0} -s {1} shell cat {2}window_dump.xml".format(_get_adb_location(), device_id,
                                                             _DEVICE_STORAGE_DIRECTORY)))
    return dumped_layout_xml


def _get_current_activity_string(device_id=None):
    if device_id is None:
        dumped_sys_output = str(
            _call_subprocess_with_no_window("{0} shell dumpsys activity".format(_get_adb_location())))
    else:
        dumped_sys_output = str(
            _call_subprocess_with_no_window("{0} -s {1} shell dumpsys activity".format(_get_adb_location(), device_id)))
    dumped_sys_output = dumped_sys_output.split("Running activities")[-1]
    for line in dumped_sys_output.split("\\r\\r\\n"):
        stripped_line = line.rstrip().lstrip()

        if "Run #" in stripped_line:
            return stripped_line.split("/")[1].split(" ")[0]


def kill_current_application(device_id=None):
    _call_subprocess_with_no_window("{0} -s {1} shell am force-stop {2}".format(_get_adb_location(), device_id,
                                                                                get_current_application_package(
                                                                                    device_id)))


def kill_application(application_name, device_id=None):
    _call_subprocess_with_no_window(
        "{0} -s {1} shell am force-stop {2}".format(_get_adb_location(), device_id, application_name))


def launch_application(application_name, device_id=None):
    if device_id is None:
        _call_subprocess_with_no_window("{0} shell monkey -p {1} 1".format(_get_adb_location(), application_name))
    else:
        _call_subprocess_with_no_window(
            "{0} -s {1} shell monkey -p {2} 1".format(_get_adb_location(), device_id, application_name))


def get_current_application_package(device_id=None):
    if device_id is None:
        dumpsys_output = str(
            _call_subprocess_with_no_window("{0} shell dumpsys window windows".format(_get_adb_location())))
    else:
        dumpsys_output = str(
            _call_subprocess_with_no_window("{0} -s {1} shell dumpsys window windows".format(_get_adb_location(),
                                                                                             device_id)))
    return dumpsys_output.split("mCurrentFocus")[-1].split("/")[0].split(" ")[-1]


def get_connected_devices():
    dumpsys_output = str(_call_subprocess_with_no_window("{0} devices".format(_get_adb_location())))
    dumplines = filter(lambda x: "device" in x, dumpsys_output.split("\\r\\n")[1:])
    return list(map(lambda x: x.split("\\t")[0].rstrip().lstrip(), dumplines))



def _call_subprocess_with_no_window(command_to_call):
    try:
        return subprocess.check_output(command_to_call, stderr=_FNULL, shell=False, startupinfo=_startupinfo)
    except subprocess.CalledProcessError:
        traceback.print_exc()
