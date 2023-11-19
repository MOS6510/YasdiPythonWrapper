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


# Constants

# Some return codes used by some yasdi functions
YE_OK                     = 0  # ok
YE_NO_ERROR               = 0  # ok, no error
YE_UNKNOWN_HANDLE         = -1 # function called with invalid handle (device or channel)
YE_NOT_ALL_DEVS_FOUND     = -1 # device detection failed, not all devices found...
YE_SHUTDOWN               = -2 # YASDI is in shutdwon mode. Function can't be called
YE_TIMEOUT                = -3 # A timeout while getting or setting channel value has occured
YE_NO_RANGE               = -3 # "GetChannelValRange": Channel has no value range
YE_VALUE_NOT_VALID        = -4 # channel value is not valid
YE_NO_ACCESS_RIGHTS       = -5 # Insufficient rights to access channel value.
YE_CHAN_TYPE_MISMATCH     = -6 # operation is not possible on that channel
YE_INVAL_ARGUMENT         = -7 # function was called with an invalid argument or pointer
YE_NOT_SUPPORTED          = -8 # function not supported anymore...
YE_DEV_DETECT_IN_PROGRESS = -9 # Device detection is already in progress
YE_TOO_MANY_REQUESTS      = -20 # Sync functions: Too many requests by user API...

# marker for an invalid handle (channel or device)
INVALID_HANDLE = 0


# Implementation

class Yasdi:

    """Wrapper for the lower part of YASDI"""

    def __init__(self):
        self.yasdi = cdll.LoadLibrary(find_library("yasdi"))
        #self.yasdiInitialize()
    
    def yasdiInitialize(self, initfile="." + os.pathsep + "yasdi.ini"):
        driverCount = c_int(0)
        self.yasdi.yasdiInitialize(initfile, byref(driverCount))

    def yasdiGetDrivers(self):
        """Returns list of driver handles of yasdi interfaces (configured serial ports)"""
        driverHandleArray = (ctypes.c_uint * 32)()
        usedHandlesInArray = self.yasdi.yasdiGetDriver(driverHandleArray, len(driverHandleArray))
        return driverHandleArray[0:usedHandlesInArray]

    def yasdiGetDriverName(self, driverID):
        """Returns the name of the driver name"""
        driverNameBufferString = (c_char * 32)()
        if self.yasdi.yasdiGetDriverName(driverID, driverNameBufferString, len(driverNameBufferString)) > 0:
            return string_at(driverNameBufferString).decode("ascii")
        else:
            return ""

    def yasdiSetDriverOnline(self, driverHandle):
        """Activates a driver. Set it online."""
        if self.yasdi.yasdiSetDriverOnline(driverHandle) > 0:
            return True
        else:
            return False

    def yasdiSetDriverOffline(self, driverHandle):
        """Deactivates a driver. Set it offline"""
        if YE_OK == self.yasdi.yasdiSetDriverOffline(driverHandle):
            return True
        else:
            return False