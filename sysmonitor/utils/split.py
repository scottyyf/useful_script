#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: split.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2022, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""


def split(data, extra_split_str=''):
    if not extra_split_str:
        return data.split()

    ret = []
    left, right, cnt = 0, 0, 0
    for i in range(len(data)):
        if data[i] in extra_split_str:
            cnt += 1

            if cnt == 2:
                ret.append(data[left:right+1])

                if i <= len(data) - 1:
                    left = right = i+1

                cnt = 0

        elif cnt == 0 and data[i] == ' ':
            if left == right == 0:
                left = right = i + 1
                continue

            ret.append(data[left:right])
            left = right = i+1
            continue

        elif cnt == 0 and right == len(data)-1:
            if left != right:
                ret.append(data[left:right+1])
                continue

        right += 1

    return ret


if __name__ == '__main__':
    print(split("vmstat", "'"))