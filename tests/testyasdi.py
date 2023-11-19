#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Unittests. A simple SMA YASDI Library Python 3.x Wrapper. 
"""

import unittest
from yasdiwrapper.yasdi import *
from yasdiwrapper.yasdimaster import *
from yasdiwrapper.sd1channels import *

# Search for YASDI libraries also in the current directory first
os.environ["DYLD_LIBRARY_PATH"] = os.getcwd() # for macOS
os.environ["LD_LIBRARY_PATH"] = os.getcwd() # for Linux/Unix

class YasdiTests(unittest.TestCase):

    yasdiMaster = YasdiMaster()
    yasdi = Yasdi()

    def setUp(self):
        """"""

    def tearDown(self):
        """"""

    def testInit(self):
        self.assertIsNotNone(self.yasdiMaster)
        self.assertIsNotNone(self.yasdi)

    def testYasdiGetDrivers(self):
        self.assertGreater(len(self.yasdi.yasdiGetDrivers()), 0)

    def testYasdiSetDriverOnline(self):
        # Given
        driverHandleList = self.yasdi.yasdiGetDrivers()
        self.assertGreater(len(driverHandleList),0)
        firstDriverHandle = driverHandleList[0]

        # Then
        self.assertEqual(True, self.yasdi.yasdiSetDriverOnline(firstDriverHandle))

    def testYasdiSetDriverOffline(self):
        # Given
        driverHandleList = self.yasdi.yasdiGetDrivers()
        self.assertGreater(len(driverHandleList),0)
        firstDriverHandle = driverHandleList[0]
        self.assertEqual(True, self.yasdi.yasdiSetDriverOnline(firstDriverHandle))

        # Then
        self.assertEqual(True, self.yasdi.yasdiSetDriverOffline(firstDriverHandle))

    def testYasdiGteDriverName(self):
        # Given
        driverHandleList = self.yasdi.yasdiGetDrivers()
        self.assertGreater(len(driverHandleList),0)
        firstDriverHandle = driverHandleList[0]

        # Then
        self.assertGreater(len(self.yasdi.yasdiGetDriverName(firstDriverHandle)), 0)

# ---------------------------------------------- YASDI Master ---------------------------------------------------
# Test of all YASDI master methods here. Most depends on a successfully device detection which takes a long time.

    def testYasdiMaster(self):
        # Given:
        driverHandleList = self.yasdi.yasdiGetDrivers()
        self.assertGreater(len(driverHandleList),0)
        firstDriverHandle = driverHandleList[0]
        self.assertEqual(True, self.yasdi.yasdiSetDriverOnline(firstDriverHandle))

        # Then:
        self.assertTrue(self.yasdiMaster.DoMasterCmdEx(cmd=CMD_DEVICE_DETECTION, param1=1))

        deviceHandles = self.yasdiMaster.GetDeviceHandles()
        self.assertGreater(len(deviceHandles),0)

        firstDeviceHandle = deviceHandles[0]
        spotChannelList = self.yasdiMaster.GetChannelHandlesEx(firstDeviceHandle, SPOTCHANNELS)
        self.assertGreater(len(spotChannelList), 0)

        paramChannelList = self.yasdiMaster.GetChannelHandlesEx(firstDeviceHandle, PARAMCHANNELS)
        self.assertGreater(len(paramChannelList), 0)

        allChannelList = self.yasdiMaster.GetChannelHandlesEx(firstDeviceHandle, ALLCHANNELS)
        self.assertGreater(len(allChannelList), 0)
        
        deviceName = self.yasdiMaster.GetDeviceName(firstDeviceHandle)
        self.assertNotEqual(0, len(deviceName))

        deviceSerialNumber = self.yasdiMaster.GetDeviceSN(firstDeviceHandle)
        self.assertNotEqual(0, deviceSerialNumber)

        deviceType = self.yasdiMaster.GetDeviceType(firstDeviceHandle)
        self.assertNotEqual(0, deviceType)

        channelHandlePac = self.yasdiMaster.FindChannelName(firstDeviceHandle, CHANNEl_NAME_PAC)
        self.assertNotEqual(channelHandlePac, INVALID_HANDLE)

        channelName = self.yasdiMaster.GetChannelName(channelHandlePac)     
        self.assertNotEqual(0, len(channelName))

        channelUnit = self.yasdiMaster.GetChannelUnit(channelHandlePac)     
        self.assertNotEqual(0, channelUnit)

        channelHandleStatus = self.yasdiMaster.FindChannelName(firstDeviceHandle, CHANNEL_NAME_STATUS)
        self.assertNotEqual(channelHandleStatus, INVALID_HANDLE)

        countOfStatusTextCount = self.yasdiMaster.GetChannelStatTextCnt(channelHandleStatus)
        self.assertNotEqual(0, countOfStatusTextCount)

        for textIndex in range(countOfStatusTextCount):
            text = self.yasdiMaster.GetChannelStatText(channelHandleStatus, textIndex)
            print(f"{textIndex}: {text}")
            self.assertNotEqual(0, len(text))
        
        channelValue = self.yasdiMaster.GetChannelValue(channelHandlePac, firstDeviceHandle, 1)     
        self.assertNotEqual(math.nan, channelValue)

        channelValueTimeStamp = self.yasdiMaster.GetChannelValueTimeStamp(channelHandlePac, firstDeviceHandle)     
        self.assertGreater(channelValueTimeStamp, 0)

        # On a SBC only, not inverter.
        channelH = self.yasdiMaster.FindChannelName(firstDeviceHandle, "SK_Toleranz")
        if channelH != INVALID_HANDLE:
            rangeParameterValue = self.yasdiMaster.GetChannelValRange(channelH)
            self.assertNotEqual(rangeParameterValue[0], None)
            self.assertNotEqual(rangeParameterValue[1], None)
            print(f"Range of channel '{self.yasdiMaster.GetChannelName(channelH)}' = {rangeParameterValue}")

if __name__ == '__main__':
    unittest.main()
