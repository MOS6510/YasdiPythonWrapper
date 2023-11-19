#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""A simple SMA YASDI Library Python 3.x Wrapper
"""

__author__ = "Heiko Prüssing"
__license__ = "MIT License"
__version__ = "0.0.1"
__maintainer__ = "Heiko Prüssing"


# imports

from ctypes import *
from ctypes.util import find_library
import os
import ctypes
import math
from yasdiwrapper.yasdi import *


# Constants

SPOTCHANNELS = 0
PARAMCHANNELS = 1
TESTCHANNELS = 2
ALLCHANNELS = 3

CMD_DEVICE_DETECTION = "detection"

# implementation

class YasdiMaster:

    def __init__(self, ini_file="." + os.sep + "yasdi.ini"):    
        """Constructor. Overwrite path to configuration ini file if needed
        """
        self.yasdiMaster = ctypes.cdll.LoadLibrary(find_library("yasdimaster"))
        self.yasdiMasterInitialize(ini_file)

    def yasdiMasterInitialize(self, iniFile):
        """This method must be called first. Initialize yasdi master."""
        availableDriverCount = c_uint()
        if YE_OK == self.yasdiMaster.yasdiMasterInitialize(iniFile.encode("ascii"), byref(availableDriverCount)):
            return availableDriverCount.value
        else:
            return 0

    def yasdiMasterShutdown(self):
        """Cleanup yasdi master. Last called method."""
        self.yasdiMaster.yasdiMasterShutdown()

    def yasdiReset(self):
        """Reset yasdi. The same as restart the complete process."""
        self.yasdiMaster.yasdiReset()

    def GetDeviceHandles(self) -> [c_int]:
        """Get list of all available (found) SMA devices. Device detection has to be done befor."""
        deviceHandleList = (c_uint * 50)() # 50 inverter device should be enough for now. 
        devCount = self.yasdiMaster.GetDeviceHandles(byref(deviceHandleList), len(deviceHandleList))
        return deviceHandleList[0:devCount]

    def GetDeviceName(self, deviceHandle) -> str:
        """Delivers the device name of a SMA device"""
        deviceNameBuffer = (c_char * 32)()
        if YE_OK == self.yasdiMaster.GetDeviceName(deviceHandle, byref(deviceNameBuffer), len(deviceNameBuffer)):
            return string_at(deviceNameBuffer).decode("ascii")
        else:
            return "???"

    def GetDeviceSN(self, deviceHandle) -> c_uint32:
        """Delivers the serial number (SN) of a device. It's 32 bit value"""
        serialNumber = c_uint32()
        if YE_OK == self.yasdiMaster.GetDeviceSN(deviceHandle, byref(serialNumber)):
            return serialNumber.value
        else:
            return math.nan

    def GetDeviceType(self, deviceHandle) -> str:
        """Returns the device type e.g. 'SunBC-38'. Every type identifies the same group of channels the device supports.
        """
        stringBuffer = (c_char * 16)()
        if YE_OK == self.yasdiMaster.GetDeviceType(deviceHandle,byref(stringBuffer),len(stringBuffer)):
            return string_at(stringBuffer).decode("ascii")
        else:
            return "???"
    
    def GetChannelHandlesEx(self, deviceHandle, channelType=SPOTCHANNELS) -> [c_int]:
        """Returns list of all channels (handles) of a device for a given channel group. Group type can be:
        - SPOTCHANNELS for live data values
        - PARAMCHANNELS for channels that are writable (parameter)
        - TESTCHANNELS internal readonly data channels 
        - ALLCHANNELS all channels
        """
        channelHandleListBuffer = (c_uint * 255)() # return the first 255 channels
        count = self.yasdiMaster.GetChannelHandlesEx(deviceHandle,
                                                    byref(channelHandleListBuffer),
                                                    len(channelHandleListBuffer),
                                                    channelType)
        return channelHandleListBuffer[0:count]

    def FindChannelName(self, deviceHandle, channelName) -> c_int:
        """Lookup for a channel name. Returns the handle of the channel if available"""
        return self.yasdiMaster.FindChannelName(deviceHandle, channelName.encode('ascii'))

    def GetChannelName(self, deviceHandle) -> str:
        """Returns the channel name of an channel handle"""
        stringBuffer = (c_char * 16)()
        if YE_OK == self.yasdiMaster.GetChannelName(deviceHandle, byref(stringBuffer), len(stringBuffer)):
            return string_at(stringBuffer).decode("ascii")
        else:
            return "???"

    def GetChannelValue(self, channel_handle, device_handle, max_val_age=1) -> float:
        """Returns a channel values as a tuple of timestamp and a (double) channel value"""
        doubleValue = c_double()
        if YE_OK == self.yasdiMaster.GetChannelValue(channel_handle,
                                                  device_handle,
                                                  byref(doubleValue),
                                                  None, 
                                                  0,
                                                  max_val_age):
            return float(doubleValue.value)
        else:
            return math.nan

    def GetChannelValueTimeStamp(self,channelHandle, deviceHandle) -> int:
        """Current Timestamp of the channel value"""
        timestamp = self.yasdiMaster.GetChannelValueTimeStamp(channelHandle, deviceHandle)
        if timestamp != 0:
            return int(timestamp)
        else:
            return None

    def GetChannelUnit(self, channelHandle) -> str:
        """Delivers the unit of the data channel"""
        bufferString = (c_char * 16)()
        if YE_OK == self.yasdiMaster.GetChannelUnit(channelHandle, byref(bufferString), len(bufferString)):
            return string_at(bufferString).decode("ascii")
        else:
            return "???"

    def SetChannelValue(self, channel_handle, device_handle, value: float) -> bool:
        result = self.yasdiMaster.SetChannelValue(channel_handle, device_handle, value)
        if YE_OK:
            return True
        else:
            return False

    def GetChannelStatTextCnt(self, channelHandle) -> int:
        """Delivers number of status texts for this channel (if this is a status text)"""
        return self.yasdiMaster.GetChannelStatTextCnt(channelHandle)

    def GetChannelStatText(self, channelHandle, textIndex: int):
        """Delivers the status text of an data channel. First index starts at "0". Call GetChannelStatTextCnt for maximal count.
        """
        stringBuffer = (c_char * 16)()
        result = self.yasdiMaster.GetChannelStatText(channelHandle, textIndex, byref(stringBuffer), len(stringBuffer))
        if YE_OK == result:
            return string_at(stringBuffer).decode("ascii")
        else:
            return "???"

    def GetChannelMask(self, channelHandle) -> (int,int):
        """Delivers the mask of an channel: Type + Index as tuple"""
        channelType = c_uint8()
        channelIndex = c_uint16()
        result = self.yasdiMaster.GetChannelMask(channelHandle, byref(channelType), byref(channelIndex))
        return (channelType,channelIndex)

    def DoMasterCmdEx(self,cmd="detection",param1=None,param2=None) -> bool:
        """Sends a master command to yasdi. Supported is only "detection" by now.
                Parameter:
                cmd = "detection" , das einzige Cmd ist voreingestellt und sucht nach Geraeten
                param1 = if device detection count of device to be searched
        """
        if YE_OK == self.yasdiMaster.yasdiDoMasterCmdEx(cmd.encode('ascii'),param1,param2):
            return True
        else:
            return False

    def GetChannelValRange(self,handle) -> (int, int):
        """Delivers the value range of a parameter channel (e.g. 0 - 240 for channel 'DA_Messintervall')
        """
        result = self.yasdiMaster.GetChannelValRange(handle,self.prange_min,self.prange_max)
        if YE_OK == result:
            return (self.range_min.value,self.range_max.value)
        else:
            return (None,None)