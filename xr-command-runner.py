# !/usr/bin/env python

# ------------------------------------------------------------------
# Nsight XR command runner - Run single or multiple commands on XR routers 64-bit
#
#
# Input:
#
# Time: How many times to run the commands. It will loop over the command array X times
# Commands: Exec commands, either single command or comma separated in string format
# ex. "show ver" <-- single
# "show ver","clear counters all;enter" <--multiple with prompts
# command_file: a file with line separated show commands, if flag is used it will override -c
# -----Note: if the show command contains an " you must switch it to '.
# Pause: XX seconds to pause between command loops
# File: Full file path to save logging
#
#
# Author: Ty Siemers tyler.siemers@nsight.com
# Credit for original script:
# Qi Miao, Liu  qiliu@cisco.com l2.py
# akshshar@cisco.com https://github.com/cisco-ie/iosxr-ztp-python/blob/master/lib/ztp_helper.py
#
# Jul 15 2021, Ty Siemers
# Copyright (c) 2021 by Nsight Teleservices
# All rights reserved.
# -------------------------

import sys
import datetime
import argparse
import time
import json
sys.path.append("/pkg/bin/")
from ztp_helper import ZtpHelpers
from pprint import pprint


class CommandRunner(ZtpHelpers):

    @staticmethod
    def command_objects(cmds):
        if ';' in cmds:
            cmd_parser = cmds.split(';')
            command = cmd_parser[0]
            cmd_parser.pop(0)
            prompts = []
            for p in cmd_parser:
                if p == 'enter':
                    prompts.append(p.replace('enter', '\\n'))
                else:
                    prompts.append(p)
            if len(prompts) > 1:
                prompts = "\\n ".join(prompts).rstrip()
            else:
                prompts = prompts[0] + "\\n"
        else:
            command = cmds
            prompts = ""

        cmd = '{"exec_cmd": "%s", "prompt_response": "%s"}' % (command, prompts)
        command_obj = json.loads(cmd)

        return command_obj

    # Send commands into function to loop over them X times pausing X secs between
    def run_cmds(self, cmds, pause=0, loop_total=0):
        prompt = ""
        for i in range(1, loop_total):
            if pause > 0 and i > 1:
                print("Pausing for %d seconds between command runs" % pause)
                time.sleep(pause)
            if len(cmds) > 1:
                for cmd in cmds:
                    cmd = self.command_objects(cmd)
                    print(cmd)
                    now = datetime.datetime.now()
                    pprint(now.strftime('%H:%M:%S on %A, %B the %dth, %Y'))
                    self.syslogger.info(now.strftime('%H:%M:%S on %A, %B the %dth, %Y'))
                    cmd = self.xrcmd(cmd)
                    pprint(cmd['output'])
                    self.syslogger.info(cmd)
                    i += 1
            else:
                cmd = self.command_objects(cmds)
                print(cmd)
                now = datetime.datetime.now()
                pprint(now.strftime('%H:%M:%S on %A, %B the %dth, %Y'))
                self.syslogger.info(now.strftime('%H:%M:%S on %A, %B the %dth, %Y'))
                cmd = self.xrcmd(cmd)
                pprint(cmd['output'])
                self.syslogger.info(cmd)
                i += 1


if __name__ == "__main__":

    # Command line arg switches passed in
    parser = argparse.ArgumentParser(
        description="Script to run commands via python using the ztpHelper library")

    parser.add_argument("-t", "--times", action="store",
                        help="How many times to run the commands in a loop ",
                        default=1)

    parser.add_argument("-c", "--commands", nargs='+',
                        help="Commands to run, can be either a single command or an array",
                        default="")

    parser.add_argument("-cf", "--command_file", action='store',
                        help="File containing line separated commands",
                        default="")

    parser.add_argument("-p", "--pause", action="store",
                        help="pause interval between command loops",
                        default=0)

    parser.add_argument("-f", "--file", action="store",
                        help="local syslog file to save logging onto",
                        default=False)

    parser.add_argument("-d", "--verbose", action="store",
                        help="Enable Debug Mode",
                        default=False)

    args = parser.parse_args()

    # Create an Object of the child class, syslog parameters are optional.
    # If nothing is specified, then logging will happen to local log rotated file.
    cmds = []

    if args.command_file:
        filename = args.command_file
        with open(filename) as f:
            content = f.read().splitlines()
        for line in content:
            cmds.append(line)
    else:
        cmds_full = args.commands[0]
        cmds = cmds_full.split(',')

    log_file = args.file
    times = int(args.times) + 1
    pause = int(args.pause)

    # Create object from NsightCommandRunner class
    cmd_runner = CommandRunner(syslog_file=log_file)
    print(cmds)
    # Run commands using argparse options
    # TODO: Investiagte why running commands via ztpHelper.xrcmd is delayed by 9-10seconds
    # TODO: Add debugging
    cmd_runner.run_cmds(cmds, pause, times)
