#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: to_str.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2022, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import sys


def to_str(data):
    if sys.version_info.major > 2:
        if isinstance(data, bytes):
            data = data.decode('utf-8')
    else:
        if isinstance(data, unicode):
            data = data.encode('utf-8')

    return data
