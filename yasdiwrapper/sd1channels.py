
#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""A simple SMA YASDI Library Python 3.x Wrapper
"""

__author__ = "Heiko Prüssing"
__license__ = "MIT License"
__version__ = "0.0.1"
__maintainer__ = "Heiko Prüssing"


# Some channel names identifications. This list is incomplete.

CHANNEl_NAME_PAC = "Pac" # Current AC Power
CHANNEl_NAME_ETAG = "E-Tag" # Energy today produced
CHANNEl_NAME_ETOTAL = "E-Total" # Energy total produced
CHANNEL_NAME_STATUS = "Status" # The "status" of an inverter. On a sunny boy control the value can be one of:  0: Stop 1: Warten 2: Betrieb, 3: Stoerung, 4: Fehler, 5: Erfassung, 6: Transparent
