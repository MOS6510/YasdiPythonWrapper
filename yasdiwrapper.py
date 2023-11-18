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
import time
import ctypes
import math


# constants

YASDI_RESULT_OK = 0

SPOTCHANNELS = 0
PARAMCHANNELS = 1
TESTCHANNELS = 2
ALLCHANNELS = 3


# implementation

class YasdiMaster:

    def __init__(self, ini_file="." + os.sep + "yasdi.ini"):    
        """Init yasdi master. Call with path to yasdi.ini file for configuration if needed.
        """
        self.yasdiMaster = ctypes.cdll.LoadLibrary(find_library("yasdimaster"))
        self.yasdiMasterInitialize(ini_file)

    def yasdiMasterInitialize(self, iniFile):
        """This method must be called first."""
        availableDriverCount = c_uint()
        if YASDI_RESULT_OK == self.yasdiMaster.yasdiMasterInitialize(iniFile.encode("ascii"), byref(availableDriverCount)):
            return availableDriverCount.value
        else:
            return 0

    def yasdiMasterShutdown(self):
        """Beendet die yasdiMaster Lib, diese Methode gibt alle Resourcen wieder frei."""
        self.yasdiMaster.yasdiMasterShutdown()

    def yasdiReset(self):
        """Setzt die yasdiMaster Lib wiedr in den Ursprungszustend... wie nach yasdiMasterInitialize"""
        self.yasdiMaster.yasdiReset()

    def GetDeviceHandles(self):
        """Get list of all available (found) SMA devices"""
        deviceHandleList = (c_uint * 32)()
        devCount = self.yasdiMaster.GetDeviceHandles(byref(deviceHandleList), len(deviceHandleList))
        return deviceHandleList[0:devCount]

    def GetDeviceName(self,handle):
        """Gibt zu dem GeraeteHandle den Geraetenamen als String zurueck
                Parameter:
                handle = Geraetehandle"""
        deviceNameBuffer = (c_char * 32)()
        self.yasdiMaster.GetDeviceName(handle,byref(deviceNameBuffer),len(deviceNameBuffer))
        return string_at(deviceNameBuffer).decode("ascii")

    def GetDeviceSN(self,handle):
        """Delivers the serial number (SN) of a device"""
        serialNumber = c_int32()
        self.yasdiMaster.GetDeviceSN(handle,byref(serialNumber))
        return int(serialNumber.value)

    def GetDeviceType(self,handle):
        """Returns the device type e.g. 'SunBC-38'
        """
        stringBuffer = (c_char * 16)()
        if YASDI_RESULT_OK == self.yasdiMaster.GetDeviceType(handle,byref(stringBuffer),len(stringBuffer)):
            return string_at(stringBuffer).decode("ascii")
        else:
            return "???"
    
    def GetChannelHandles(self, deviceHandle, channelType=SPOTCHANNELS):
        """Get list of channel handles of an group type
                parameter_channel = 0 -> Spotwerte| 1 -> Parameterwerte"""
        
        wChanType = c_ushort()
        bChanIndex = c_byte(0)
        channelHandleListBuffer = (c_uint * 100)()
        
        if channelType == PARAMCHANNELS:
            wChanType = c_ushort(0x040f)
        elif channelType == SPOTCHANNELS:
            wChanType = c_ushort(0x090f)
        else:
            wChanType = c_ushort(0x0000)

        # /* define channel type for the next function "GetChannelHandlesEx" */
        # typedef enum { SPOTCHANNELS=0, PARAMCHANNELS, TESTCHANNELS, ALLCHANNELS } TChanType;
        count = self.yasdiMaster.GetChannelHandlesEx(deviceHandle,
                                            byref(channelHandleListBuffer),
                                            len(channelHandleListBuffer),
                                            wChanType)
        return channelHandleListBuffer[0:count]

    def FindChannelName(self, deviceHandle, channelName):
        """Lookup for a channel name. Returns the handle of the channel if available"""
        return self.yasdiMaster.FindChannelName(deviceHandle, channelName.encode('ascii'))

    def GetChannelName(self,handle):
        """Returns the channel name of an channel handle"""
        """
        result = self.yasdiMaster.GetChannelName(handle,self.ChannelName,len(self.ChannelName))
        if result == math.nan:
            return result
        else:
            return self.ChannelName.replace("\x00","").rstrip().lstrip()
        """

    def GetChannelValue(self, channel_handle, device_handle, max_val_age=0):
        """Returns a channel values as a tuple of timestamp and a (double) channel value"""
        doubleValue = c_double()
        result = self.yasdiMaster.GetChannelValue( channel_handle,
                                                   device_handle,
                                                   byref(doubleValue),
                                                   None, 
                                                   0,
                                                   max_val_age)
        if result == YASDI_RESULT_OK:
            return doubleValue.value
        else:
            return math.nan

    def GetChannelValueTimeStamp(self,channelHandle, deviceHandle):
        """Current Timestamp of the channel value"""
        timestamp = self.yasdiMaster.GetChannelValueTimeStamp(channelHandle, deviceHandle)
        return timestamp

    def GetChannelUnit(self, channelHandle):
        """Delivers the unit of the data channel"""
        bufferString = (c_char * 16)()
        if YASDI_RESULT_OK == self.yasdiMaster.GetChannelUnit(channelHandle, byref(bufferString), len(bufferString)):
            return string_at(bufferString).decode("ascii")
        else:
            return "???"

    def GetMasterStateIndex(self):
        """Delivers the state of the state machine used internally:
                1 = Initial
                2 = Device detection
                3 = Resolving SD1 network address 
                4 = Request channel list
                5 = Processing master commands
                6 = Reading channel data
                7 = Writing channel data"""
        result = self.yasdiMaster.GetMasterStateIndex()
        return result

    def SetChannelValue(self,channel_handle,device_handle,value):
        result = self.yasdiMaster.SetChannelValue(channel_handle,device_handle,value)
        return result

    def GetChannelStatTextCnt(self,handle):
        """Delivers number of status texts for this channel (if this is a status text)"""
        result = self.yasdiMaster.GetChannelStatTextCnt(handle)
        return result

    def GetChannelStatText(self,handle,index,):
        """Delivers the status text of an data channel. First index starts at "0"
        """
        stringBuffer = (c_char * 16)()
        result = self.yasdiMaster.GetChannelStatText(handle,index,byref(stringBuffer),len(stringBuffer))
        if YASDI_RESULT_OK == result:
            return string_at(stringBuffer).decode("ascii")
        else:
            return "???"

    def GetChannelMask(self, channelHandle):
        """Delivers the mask of an channel: Type + Index as tuple"""
        
        channelType = c_uint8()
        channelIndex = c_uint16()
        result = self.yasdiMaster.GetChannelMask(channelHandle, byref(channelType), byref(channelIndex))
        return (channelType,channelIndex)

    def DoMasterCmdEx(self,cmd="detection",param1=None,param2=None):
        """Sendet Kommandos an den YASDI-Master. In YASDI 1.3 gibt es nur das Cmd "detection"
                Parameter:
                cmd = "detection" , das einzige Cmd ist voreingestellt und sucht nach Geraeten
                param1 = if device detection count of device to be searched
                param2 = None k.a.
                Ergebnis:
                0 = OK
                -1 = es wurden nicht alle Geraete gefunden"""
        return self.yasdiMaster.yasdiDoMasterCmdEx(cmd.encode('ascii'),param1,param2)

    def GetChannelValRange(self,handle):
        """Gibt den Bereich des Kanals zurueck. z.B. Kanal 82 (DA_Messintervall von 0 - 240)
                Parameter:
                handle = Kanalhandle
                Ergebnis:
                Python Tupel(min,max) bei OK
                -1: Kanalhandle ist ungueltig
                -2: Zeiger fuer Ergebnis ungueltig (sollte durch den yasdiwrapper nicht vorkommen)
                -3: wenn es keinen extra Wertebereich gibt
                """
        """
        result = self.yasdiMaster.GetChannelValRange(handle,self.prange_min,self.prange_max)
        if not result:
            return (self.range_min.value,self.range_max.value)
        else:
            return result"""

class Yasdi:

    """Wrapper for the lower part of YASDI"""

    def __init__(self):
        """Konstruktor"""
        self.yasdi = cdll.LoadLibrary(find_library("yasdi"))

    def yasdiGetDrivers(self):
        """Returns list of driver handles of yasdi interfaces (configured serial ports)"""
        driverHandleArray = (ctypes.c_uint * 32)()
        usedHandlesInArray = self.yasdi.yasdiGetDriver(driverHandleArray, len(driverHandleArray))
        return driverHandleArray[0:usedHandlesInArray]

    def yasdiGetDriverName(self,driverID):
        """Returns the name of the driver name"""
        driverNameBufferString = (c_char * 32)()
        if YASDI_RESULT_OK == self.yasdi.yasdiGetDriverName(driverID, driverNameBufferString, len(driverNameBufferString)):
            return string_at(driverNameBufferString).decode("ascii")
        else:
            return ""

    def yasdiSetDriverOnline(self,driverHandle):
        """Activates a driver. Set it online."""
        if YASDI_RESULT_OK == self.yasdi.yasdiSetDriverOnline(driverHandle):
            return True
        else:
            return False

    def yasdiSetDriverOffline(self, driverHandle):
        """Deactivates a driver. Set it offline"""
        if YASDI_RESULT_OK == self.yasdi.yasdiSetDriverOffline(driverHandle):
            return True
        else:
            return False

if __name__ == "__main__":

    # Let search for yasdi libraries in current directory too
    os.environ["DYLD_LIBRARY_PATH"] = os.getcwd() # for macOS
    os.environ["LD_LIBRARY_PATH"] = os.getcwd() # for Linux/Unix

    yasdiMasterLibrary = YasdiMaster(ini_file="./yasdi.ini")
    yasdiLibrary = Yasdi()

    try:
        driverHandleList = yasdiLibrary.yasdiGetDrivers()
        if len(driverHandleList) == 0:
            raise Exception("Error: No configured interfaces available! Please check your YASDI configuration try again...")

        # Switch all interfaces (drivers) online
        for driverHandle in driverHandleList:
             print(f"Set driver '{yasdiLibrary.yasdiGetDriverName(driverHandle)}' online. Success = {yasdiLibrary.yasdiSetDriverOnline(driverHandle)}" )

        # Search for SMA devices (inverters, etc...)
        print("Start searching SMA devices...")
        result = yasdiMasterLibrary.DoMasterCmdEx(cmd="detection", param1=1) # Search for at leased one device
        if result != YASDI_RESULT_OK:
            print(f"Error searching devices: {result}")

        # Get the list of found SMA devices
        devicesList = yasdiMasterLibrary.GetDeviceHandles()
        for deviceHandle in devicesList:
            print(f"Found device: {yasdiMasterLibrary.GetDeviceName(deviceHandle)}")

        if len(devicesList) == 0:
            raise Exception("ERROR: No SMA inverter found! Check your hardware or configuration and try again...")
        
        # Request some live values:

        # List of all data channels I'd like to request
        # "Pac" => "Current Power AC", 
        # "E-Tag" => "Energy from today", 
        # "E-Total" => "Energy total"
        channelsToRequest = ["Pac", "E-Tag", "E-Total"] 

        # The age of the channel value should not older than 1 second
        AGE_OF_VALUE_SECONDS = 1

        while True:
            for deviceHandle in devicesList:
                for channelName in channelsToRequest:
                    channelListOfSpots = yasdiMasterLibrary.GetChannelHandles(deviceHandle,SPOTCHANNELS)
                    channelHandle = yasdiMasterLibrary.FindChannelName(deviceHandle, channelName)
                    if channelHandle < 0:
                        print(f"Error: Channel {channelName} not found on device {yasdiMasterLibrary.GetDeviceName(deviceHandle)} ...")
                    else:
                        channelValue = yasdiMasterLibrary.GetChannelValue(channelHandle, deviceHandle, AGE_OF_VALUE_SECONDS)
                        timestamp = yasdiMasterLibrary.GetChannelValueTimeStamp(channelHandle, deviceHandle)
                        channelUnit = yasdiMasterLibrary.GetChannelUnit(channelHandle)
                        print(f"{channelName};{channelUnit};{timestamp};{channelValue}")
            time.sleep(2)

    #except Exception as e:
    #    print(f"=> Exception: {e}")

    finally:
        yasdiMasterLibrary.yasdiMasterShutdown()
