#!/usr/bin/env python
# -*- coding: utf-8 -*-

from assisipy import casu

import sys

if __name__ == '__main__':
    
    rtc = sys.argv[1]

    mycasu = casu.Casu(rtc_file_name=rtc)
    
    mycasu.stop()
