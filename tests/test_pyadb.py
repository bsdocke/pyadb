import unittest
import pyadb
from unittest.mock import MagicMock


class TestPyadb(unittest.TestCase):

    def test_tap(self):
        pyadb.set_adb_location("C:/adb")
        pyadb._call_subprocess_with_no_window = MagicMock()
        pyadb.tap(100,100)
        pyadb._call_subprocess_with_no_window.assert_called_with("C:/adb shell input tap 100 100")

    def test_tap_device(self):
        pyadb.set_adb_location("C:/adb")
        pyadb._call_subprocess_with_no_window = MagicMock()
        pyadb.tap(100, 100, "TESTDEVICE")
        pyadb._call_subprocess_with_no_window.assert_called_with("C:/adb -s TESTDEVICE shell input tap 100 100")

    def test_back(self):
        pyadb.set_adb_location("C:/adb")
        pyadb._call_subprocess_with_no_window = MagicMock()
        pyadb.back()
        pyadb._call_subprocess_with_no_window.assert_called_with("C:/adb shell input keyevent 4")

    def test_back_device(self):
        pyadb.set_adb_location("C:/adb")
        pyadb._call_subprocess_with_no_window = MagicMock()
        pyadb.back("TESTDEVICE")
        pyadb._call_subprocess_with_no_window.assert_called_with("C:/adb -s TESTDEVICE shell input keyevent 4")

    def test_swipe(self):
        pyadb.set_adb_location("C:/adb")
        pyadb._call_subprocess_with_no_window = MagicMock()
        pyadb.swipe(100,200,300,400)
        pyadb._call_subprocess_with_no_window.assert_called_with("C:/adb shell input swipe 100 200 300 400 500")


    def test_swipe_duration(self):
        pyadb.set_adb_location("C:/adb")
        pyadb._call_subprocess_with_no_window = MagicMock()
        pyadb.swipe(100, 200, 300, 400, 700)
        pyadb._call_subprocess_with_no_window.assert_called_with("C:/adb shell input swipe 100 200 300 400 700")


    def test_swipe_duration_device(self):
        pyadb.set_adb_location("C:/adb")
        pyadb._call_subprocess_with_no_window = MagicMock()
        pyadb.swipe(100, 200, 300, 400, 700, "TESTDEVICE")
        pyadb._call_subprocess_with_no_window.assert_called_with("C:/adb -s TESTDEVICE shell input swipe 100 200 300 400 700")