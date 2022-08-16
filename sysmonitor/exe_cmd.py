#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: exe_cmd.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2022, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
from subprocess import Popen, PIPE, TimeoutExpired, STDOUT
from utils.to_str import to_str
from utils.split import split


class ExecCmd(object):
    @classmethod
    def exec_with_ret(cls, cmd):
        if isinstance(cmd, list):
            pass
        elif isinstance(cmd, str):
            cmd = split(cmd)

        try:
            proc = Popen(cmd, stderr=STDOUT, stdout=PIPE)
            outs, errs = proc.communicate(timeout=6)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()

        ret = proc.returncode

        if ret != 0:
            print(outs)
            return ''

        return to_str(outs)


    @classmethod
    def exec_with_other_pipe(cls, *args, force_shell=False, ret=None, **kwargs):
        ret = '' if not ret else ret

        for cmd in args:
            if force_shell:
                if not ret:
                    ret = Popen(cmd, stdout=PIPE, shell=True)
                else:
                    ret = Popen(cmd, stdin=ret.stdout, stdout=PIPE, shell=True)

                continue

            if isinstance(cmd, str):
                cmd = split(cmd, "'")

            if not ret:
                ret = Popen(cmd, stdout=PIPE)
            else:
                ret = Popen(cmd, stdin=ret.stdout, stdout=PIPE)

        return ret


if __name__ == '__main__':
    ret = ExecCmd.exec_with_other_pipe('vmstat', 'sed -n -e 3p')
    ret = Popen("awk '{print $15}'", stdin=ret.stdout, stdout=PIPE, shell=True)
    print(ret.communicate(), 'er0000')
