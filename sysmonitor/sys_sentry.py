#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: sys_sentry.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2022, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import os
import stat
import psutil
from exe_cmd import ExecCmd

CPU_NUM = os.cpu_count()


def MEM_CAP():
    # ret = ''
    # try:
    #     ret = ExecCmd.exec_with_ret(['cat', '/proc/meminfo'])
    # except Exception:
    #     pass
    #
    # if ret:
    #     ret = re.search(r'memtotal: +([0-9]+) +kb', ret, re.I)
    #     if ret:
    #         ret = ret.group(1)
    #
    # if ret:
    #     return int(ret)
    #
    # return 0

    # code from psutil
    mem = {}
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            fileds = line.split()
            mem[fileds[0][:-1]] = int(fileds[1]) * 1024

    return mem


class LinuxSentry(object):
    @classmethod
    def cpu_sentry(cls):
        cpu_idle = ExecCmd.exec_with_other_pipe('vmstat', "sed -n -e 3p")

        cpu_idle = ExecCmd.exec_with_other_pipe("awk '{print $15}'",
                                                force_shell=True, ret=cpu_idle)

        out, err = cpu_idle.communicate()
        if out and out.isdigit():
            if int(out) < 10:
                cpu_in_work = ExecCmd.exec_with_other_pipe(
                    "awk '{print $1}'", force_shell=True, ret=cpu_idle)

            if cpu_in_work > CPU_NUM:
                return False

        return True

    @classmethod
    def mem_sentry(cls):
        mem = MEM_CAP()
        if not mem:
            return True

        total = mem.get('MemTotal')
        free = mem.get('MemFree')
        buffer = mem.get('Buffers')
        cache = mem.get('Cached')
        in_use_percent = round((total - free - buffer - cache) / total, 2) * 100

        print('mem in use', in_use_percent)
        if in_use_percent >= 90:
            return False

        return True

    @classmethod
    def disk_sentry(cls, dev):
        if not os.path.exists(dev):
            print('path not exist, ignore')
            return True

        if not stat.S_ISBLK(os.stat(dev).st_mode):
            print('not a block device, ignore')
            return True

        if ExecCmd.exec_with_ret(['smartctl', '-H', dev]):
            return True

        print('failed to judge disk status')
        return False

    @classmethod
    def disk_io_sentry(cls):
        pass

    @classmethod
    def network_dev_sentry(cls, network_dev):
        curr_status = psutil.net_if_stats()
        if network_dev not in curr_status:
            return True

        return curr_status.get(network_dev).isup

    @classmethod
    def network_io_sentry(cls, network_dev):
        dev_statistic = ExecCmd.exec_with_other_pipe(
            'ip -s link show {0}'.format(network_dev),
            'sed -n -e 4p')
        if dev_statistic:
            err_pkg_num = ExecCmd.exec_with_other_pipe(
                "awk '{print $3}'", force_shell=True, ret=dev_statistic
                )

        out, err = err_pkg_num.communicate()
        if out and out.isdigit():
            if int(out) > 0:
                return False

        return True


if __name__ == '__main__':
    print(LinuxSentry.cpu_sentry())
    print(LinuxSentry.mem_sentry())
    print(LinuxSentry.disk_sentry('/dev/sda'))
    print(LinuxSentry.network_io_sentry('bridge0'))
