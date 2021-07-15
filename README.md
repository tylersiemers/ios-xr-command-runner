# ios-xr-command-runner
Run exec commands via python

As usual always test first in a non-production enviroment. You can run commands that will disrupt traffic. For example a 'reload' command is possible and allowed with this.
Always test the commands on the cli first before running.

## Copy script to box
`Clone or download the xr-command-runner.py`

Place the file where it will be accessible, common place is
`/misc/scratch`, `disk0`

Make the file executable on the box

`run chmod +x /path/to/directory/xr-command-runner.py`

## See help options

`run python xr-command-runner.py -h`

```
usage: xr-command-runner.py [-h] [-t TIMES] [-c COMMANDS [COMMANDS ...]]
                                [-cf COMMAND_FILE] [-p PAUSE] [-f FILE]
                                [-d VERBOSE]
 
Script to run commands via python using the ztpHelper library
 
optional arguments:
  -h, --help            show this help message and exit
  -t TIMES, --times TIMES
                        How many times to run the commands in a loop
  -c COMMANDS [COMMANDS ...], --commands COMMANDS [COMMANDS ...]
                        Commands to run, can be either a single command or an
                        array
  -cf COMMAND_FILE, --command_file COMMAND_FILE
                        File containing line separated commands
  -p PAUSE, --pause PAUSE
                        pause interval between command loops
  -f FILE, --file FILE  local syslog file to save logging onto
  -d VERBOSE, --verbose VERBOSE
                        Enable Debug Mode
```

## Running
### Option 1 - Single Command
`run python xr-command-runner.py --times 1 --commands "show version"`

### Option 2 - Multi Commands
`run python xr-command-runner.py --times 1 --commands "show version","show run"`

### Option 3 - Run from file with show commands
You must create a file on the router first with the show commands
`run vi my_show_commands.txt` or `run nano my_show_commands.txt`

Commands in the file must be line separated
Example
my_show_commands.txt
```
show version
show run
clear counters all;enter
```
`run python xr-command-runner.py --times 1 --command_file "my_show_commands.txt"`

## Handling Prompts
Prompts can be handled by adding semi-colons to end of the show command. You can stack them for multiple prompts
```
"clear counters;enter"
"crypto key generate rsa;yes;2048"
```

`enter` is a special keyword that gets replaced with a \\n in the output. 

## Examples
### Run from file of show commands, looping 3 times over the commands with a 3 second pause between loops and send the output to a log file
```angular2html
run python xr-command-runner.py --times 3 --pause 3 --command_file "my_show_commands.txt" >> example_file.log
 
RP/0/RP0/CPU0:LAB_540#run python xr-command-runner.py --times 3 --pause 3 --command_file "my_show_commands.txt" >> example_file.log
RP/0/RP0/CPU0:LAB_540#more example_file.log
Thu Jul 15 12:04:42.579 CDT
show run
'12:03:02 on Thursday, July the 15th, 2021'
['!! IOS XR Configuration 6.6.3',
 '!! Last configuration change at Thu Jul 15 12:03:11 2021 by ZTP',
 '!',
 'service unsupported-transceiver',
 'hostname LAB_540',
 'clock timezone CST US/Central',
 'banner exec ~*******************************************************************************',
 ..........
```

### Run a single command 10 times, output to terminal
```angular2html
run python xr-command-runner.py --times 10 --commands "show clock"        

RP/0/RP0/CPU0:LAB_540#run python xr-command-runner.py --times 10 --commands "show clock"                                          
Thu Jul 15 12:06:28.375 CDT
show clock
'12:06:28 on Thursday, July the 15th, 2021'
['12:06:40.830 CDT Thu Jul 15 2021']
show clock
'12:06:40 on Thursday, July the 15th, 2021'
['12:06:53.120 CDT Thu Jul 15 2021']
show clock
'12:06:53 on Thursday, July the 15th, 2021'
['12:07:05.439 CDT Thu Jul 15 2021']
show clock
'12:07:05 on Thursday, July the 15th, 2021'
['12:07:57.726 CDT Thu Jul 15 2021']
show clock
'12:07:57 on Thursday, July the 15th, 2021'
['12:08:09.989 CDT Thu Jul 15 2021']
show clock
'12:08:10 on Thursday, July the 15th, 2021'
['12:08:22.222 CDT Thu Jul 15 2021']
show clock
'12:08:22 on Thursday, July the 15th, 2021'
['12:08:34.514 CDT Thu Jul 15 2021']
show clock
'12:08:34 on Thursday, July the 15th, 2021'
['12:08:46.802 CDT Thu Jul 15 2021']
show clock
'12:08:46 on Thursday, July the 15th, 2021'
['12:08:59.061 CDT Thu Jul 15 2021']
show clock
'12:08:59 on Thursday, July the 15th, 2021'
['12:09:11.305 CDT Thu Jul 15 2021']      
```