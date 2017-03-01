# Project Basecamp
Metasploit modules developed to demonstrate insecure by design PLC's as part of Project Basecamp. See [Dale Peterson's Introduction to Basecamp Video](https://www.youtube.com/watch?v=BKJje3Ram2I&t=9s)

Project Basecamp is a research effort by Digital Bond and a team of volunteer researchers to highlight and demonstrate the fragility and insecurity of most SCADA and DCS field devices, such as PLC's and RTU's.

The goal of Project Basecamp is to make the risk of these fragile and insecure devices so apparent and easy to demonstrate that a decade of inaction will end. SCADA and DCS owner/operators will demand a secure and robust PLC, and this will drive vendors to finally provide a product worthy of being deployed in the critical infrastructure.

The PLC / RTU that are part of this project are:
- [3S CoDeSys](http://github.com/digitalbond/Basecamp#3s-codesys)
- [GE D20](http://github.com/digitalbond/Basecamp#ge-d20-rtu)
- [Koyo / DirectLOGIC](http://github.com/digitalbond/Basecamp#koyo-/-directlogic)
- [Rockwell Automation ControlLogix](http://github.com/digitalbond/Basecamp#rockwell-automation-controllogix)
- [Schneider Electric Modicon](http://github.com/digitalbond/Basecamp#schneider-electric-modicon)

## The Reason: A Firesheep Moment for PLC's

Everyone knows PLC's are vulnerable --- or so we have heard for ten years now since the 9/11 attacks focused attention on DCS and SCADA security. Not only do they lack basic security features, they are also fragile. Warnings abound about the dangers of even running a port scan on a PLC. Yet even though "everyone knows" there has been little or no progress on developing even the option of purchasing a secure and robust PLC.

After this lost decade, Digital Bond decided to stop trying the same failed approach and the result is Project Basecamp. We looked for parallel situations in security where a serious problem was known, not addressed for a long time, and then something triggered a change. The best example we found is Firesheep.

In 2007/2008 there were numerous presentations at security events showing how a twitter, facebook, gmail or other HTTP session could be hijacked because the cookies were not encrypted. It got some buzz at a security events and technical web sites, but no action to address the vulnerability.

In October of 2010 Eric Butler created Firesheep, an easy to use Firefox extension that hijacked an HTTP session. Anyone who could use a browser could hijack Facebook or Twitter sessions in a coffee shop. Shortly after that the vendors took action and made mandatory HTTPS an option and eventually the default.

Project Basecamp is attempting to be a Firesheep Moment for PLC's. The team has, not surprisingly, found many vulnerabilities in the PLC's, but perhaps more importantly have identified "insecure by design" issues that are actually much easier to leverage to affect the availability and integrity of a process.

The key to making this a Firesheep Moment for PLC's is providing tools so any engineer, IT type, security professional or anyone with a bit of computer skill can demonstrate just how fragile and vulnerable these PLC's are. It's beyond, PLC's are vulnerable. Basecamp provides the tools to show an executive just how easy it is to take down the SCADA or DCS.

## The Basecamp Team

Reid Wightman of Digital Bond leads the Basecamp team. He performed the work on two of the devices and coordinated the results with the rest of the research team. The other Project Basecamp team members are:

- Dillon Beresford
- Jacob Kitchel
- Ruben Santamarta
- Anonymous 1
- Anonymous 2

##3S CoDeSys

### Background

3S Software Gmbh produces the CoDeSys ladder logic system.  CoDeSys is used by 261 manufacturers to execute ladder logic on their PLCs, motorized drive controllers, and other industrial controllers.

CoDeSys has several components: a graphical Integrated Development Environment (IDE) for writing ladder logic on a PC and transferring the resultant logic to a PLC, a web server for PCs for retrieving and visualizing data from PLCs, and a ladder logic runtime engine for receiving the ladder logic from a PC and executing it.

### Our Focus

We focused on the ladder logic runtime engine specifically as seen on the WAGO IPC 758-870 model PLC, although all makes and models of CoDeSys PLCs appear to be affected.  The ladder logic runtime is provided by 3S-Software and can be run on many operating systems including Nucleus RTOS, embedded Linux, Windows CE, etc.  The WAGO happens to run embedded Linux on an x86 CPU, and also allows Telnet and FTP access, making it a nice target for evaluation.  The WAGO linux kernel includes a complete filesystem and many programs allowing for a good exercising of CoDeSys’ capabilities.

### Runtime Functionality

The CoDeSys runtime does a lot of things.  Obviously its main purpose is to run ladder logic.  Ladder logic is executed in the form of a wrapped binary, compiled for the operating system and CPU of the PLC.  The ladder logic file contains a header followed by binary executable code.  The CoDeSys ladder logic engine loads the file into memory, and then jumps into that memory and begins executing instructions contained in the file.  This is important when we consider the privileges that CoDeSys often runs with, and its lack of authentication for file transfer.

The CoDeSys runtime has ancillary functions as well.  It offers a TCP listener service, often running on TCP/1200 (although TCP/1201 and TCP/2455 are observed on other controller types).  The TCP listener service allows for file transfer as well as a command-line interface.

Neither the command-line interface nor the file transfer functionality requires authentication.  The CoDeSys runtime engine needs to access /dev devices on embedded Linux and writes to an output bus (K-Bus, which is connected over a PCI interface in the WAGO).  As a consequence, manufacturers often run the ladder logic runtime as ‘root’ (on linux systems), ‘administrator’ (on embedded windows), or run it on an operating system which does not provide deprivileged users.

The result of all of this is that a user with the right know-how can connect to the command-line of CoDeSys and execute commands, as well as transfer files.  Commands include the ability to stop and start the running ladder logic, wipe PLC memory, and list files and directories.  Transferring files include the ability to send and receive.  Sending and receiving files also suffers from directory traversal — we can read and write files outside of the CoDeSys directory on the controller using “../” notation.  On most operating systems this includes the ability to overwrite critical configuration files such as /etc/passwd and /etc/shadow on linux, or the windows registry on Windows CE.

The ladder logic runtime file is transferred in conjunction with a 32-bit checksum.  The 32-bit checksum is computed by adding the bytes of the runtime file together, and treating the result as a 32-bit integer.  The ladder logic runtime transfer is mostly implemented in this release; a missing command is required to make the new ladder logic upload active on the PLC.

### The Tools

We have produced three tools for interacting with PLCs that run CoDeSys.  The first tool is a command-shell utility.  This allows an unauthenticated user the ability to perform privileged operations, sans password.  It is the equivalent of running the “PLC – Browser” function from the CoDeSys desktop software, but does not assert vendor checks normally performed by the CoDeSys software — CoDeSys will normally fail to connect to a PLC and offer this option without properly licensed plugins.

The commands available vary by PLC, so type “?” to get a list of options.

The second tool is a file transfer tool which allows for reading and writing files on controllers with a filesystem.  Again, this tool bypasses the only protections that CoDeSys provides — vendor-specific checks that ensure we’re communicating with the right kind of PLC.

![codesys-shell.py connecting to a Wago controller](https://www.digitalbond.com/wp-content/uploads/2012/10/Codesys-shell-local.png)

These tools come in the form of Python scripts.  The hastily-written code isn’t terribly legible (blame Reid) but works quite well on a wide variety of controllers.  They can easily be ported to be Metasploit modules, and could be made to run the Meterpreter shell on supported operating systems.

### The Source

- [codesys-shell.py](https://github.com/digitalbond/Basecamp/blob/master/codesys-shell.py)

- [codesys-transfer.py](https://github.com/digitalbond/Basecamp/blob/master/codesys-transfer.py)

##GE D20 RTU
### Background
The General Electric D20ME is a widely used in the electric sector, particularly in substations. It is an ancient device with a CPU chip from 1987, actually a similar chip that was in the Macintosh II line, and a PSOS operating system that was end of support in 1999. It even had an old fashioned UV EPROM. All this obsolete technology cost $15,000 for an entry level version with just a couple of cards. The good news is that GE has come out with a new, modern version of the D20 called the D20MX. 

Our blunt advice – don’t deploy any new GE D20s and develop a plan to replace all of your GE D20s with new MX models or some competitive product as soon as practical.

### Metasploit Modules

All of the Metasploit modules are available in Rapid7’s Metasploit feed.

#### d20tftpbd – General Electric D20ME Asynchronous Command Line

This module automates a “feature” in the D20 that allows a user to send via TFTP a MONITOR:command.log file. The D20 will execute all of the commands in that file, and then return the results to the Monitor:response.log file.

This is very unusual and what Reid calls asynchronous command line — and there is no authentication. An attacker could craft a set of attack commands in a file and TFTP it to one or more GE D20’s.

The d20tftpbd module automates the process and the Metasploit users appears to have an interactive command line interface to the GE D20. Try typing the help command to see all the commands that can be run from this asynchronous command line interface.

This is an experimental module available in Metasploit’s testing branch. The module works fine, but it is so unusual that Rapid7 is trying to figure out the best way to include it in the framework.

#### d20pass – General Electric D20ME Credential Recovery

This module retrieves and displays the account usernames and passwords from the GE D20 device configuration.  The credentials can be used to perform any action on the device, including changing ladder logic. The credentials are just part of the plaintext configuration file that is downloaded. An attacker would have complete information on the process and the ability to make any changes.

#### d20_tftp_overflow – General Electric D20ME TFTP Server Buffer Overflow DoS

The D20 has numerous buffer overruns in its TFTP server. This module exploits the TFTP Server transfer-mode overflow and results in a denial of service condition on the D20. If successful you will see “TFTP – DoS complete, the D20 should fault after a timeout.” A reboot of the D20 is required to recover.

The filename also suffers from an overrun but seems unlikely to be exploitable.

### Easy Scripts

[ged20cmd.py](https://github.com/digitalbond/Basecamp/blob/master/ged20cmd.py) – A python script that provides an interactive command-line to the D20’s tftp backdoor command line.  Please read the comments in the header — this requires a new’ish python tftp library to work correctly — the version of the tftp library for python included with most major linux distros (Backtrack, Ubuntu, etc) is too old to work correctly.

This is the same capability provided in the d20tftpbd Metasploit module.

### Buffer Overflow Tools

[ged20tftp.rb](https://github.com/digitalbond/Basecamp/blob/master/ged20tftp.rb) – This module crashes the D20 tftp service.  The operating system catches the exception, but the damage is done — all processes are stopped and the D20’s network stack is disabled.

### Fingerprinting Tools

[ged20telnet-fp.py](https://github.com/digitalbond/Basecamp/blob/master/ged20telnet-fp.py) – This is a generic telnet service fingerprinting tool, which may be used against any controller which supports the telnet protocol.  It actively tries all telnet options against the remote host, to determine what options are supported.  This may crash some controllers, so use it with care.

##Koyo / DirectLOGIC
### Background
The Koyo / DirectLOGIC product line is a much lower cost PLC as compared to the GE, Rockwell Automation and Schneider Quantum products in Project Basecamp. It is less likely to be seen in the critical infrastructure SCADA and DCS, but it is widely used in smaller plants and systems in a variety of industry sectors

The Basecamp team focused on the ECOM Ethernet module as this is the most accessible interface for a cyber attack. The ECOM module is an attractive target for an adversary. In S4 2009 Digital Bond demonstrated how unauthenticated firmware could be uploaded to the device.

In Project Basecamp, the anonymous researcher found ladder logic upload and download is only protected by a seven-digit passcode, that can be brute-forced.  The webserver allows configuration of the Ethernet module only, but lacks any authentication and has cross-site scripting issues as well as denial-of-service issues.  In particular, requesting invalid pages such http://koyodevice/foo.htm will result the in the webserver going offline for several minutes.

### Metasploit Module
[koyobrute.rb](https://github.com/digitalbond/Basecamp/blob/master/koyobrute.rb) – This Metasploit module will bruteforce a Koyo password.  It is likely that this will work against other devices from Automation Direct which support the DirectNet (aka HAP) protocol. 

With the recovered password an attacker can download ladder logic to learn about the project, modify the ladder logic to affect the availability or integrity of the process, and upload rogue ladder logic.

### Fingerprinting Tools
The Koyo is difficult to fingerprint due to its limited services. The web server provides no fingerprintable data (no Server: identifier). The Modbus protocol supports no odd function codes. The device may be located on active search engines such as ERIPP by searching for information contained in its web pages.

##Rockwell Automation ControlLogix
### Background
The Rockwell Automation / Allen-Bradley ControlLogix is a full featured PLC used in a variety of different industry sectors. It is most common in the manufacturing sector, but it is also used in many other industries for ad hoc processes. For example in power plants it is used not in the main DCS but is often seen in balance of plant systems.

The ControlLogix has separate CPU and Ethernet modules.  Architecturally, the system appears similar to the Schneider Modicon Quantum.  The Ethernet module offers a far smaller attack surface than the Schneider device.  Some effort appears to have gone into securing the device from the vendor, but protocol issues were uncovered.

This device was tested by volunteer independent researcher Rubén Santamarta.

### Metasploit Module
[ethernetip-multi.rb](https://github.com/digitalbond/Basecamp/blob/master/ethernetip-multi.rb) – This Metasploit module has four possible payloads. The first two payloads highlight the EtherNet/IP protocol “insecure by design” issue.

- Stop CPU – just like it sounds, this will take the ControlLogix out of service
- Reboot Ethernet Controller – a temporary outage of the ControlLogix Ethernet interface

There are many more request commands in the EtherNet/IP protocol that cause availability and integrity issues with the ControlLogix PLC. None of these commands are authenticated. This problem and attack will be effective on any EtherNet/IP device including other systems manufactured by Rockwell Automation, Schneider, Wago, and others.

The ODVA is responsible for the EtherNet/IP protocol and shows 300 vendors using the protocol. Unbelievably the ODVA has not even begun an effort to add basic security to the protocol. Vendors may need to look at tunnels or wrappers until ODVA starts taking integrity and availability seriously. Not all of the payloads will work for all devices, but approximately 300 vendors will be affected.

The two other payloads are due to protocol stack errors in the ControlLogix. This will also affect any other equipment that uses the same protocol stack.

- Crash the PLC CPU
- Crash the Ethernet Controller

##Schneider Electric Modicon
### Background
The Schneider Electric Modicon Quantum is a versatile PLC used in a wide variety of sectors including manufacturing, water/wastewater, oil and gas, chemical and more. It has a modular architecture so the size and cost can vary a great deal. The very basic Quantum pictured at the left cost $11,000 including the Unity software.

The Modicon Quantum Ethernet card is an embedded system running vxWorks 5.4 on a PowerPC processor (MPC870). The PLCs CPU module sports an x86 processor (the device tested in Basecamp had a 80486). Reid Wightman was the lead Project Basecamp researcher on this PLC, and he also developed the Metasploit Modules.

### Metasploit Modules
The Modicon Metasploit Modules are in the Metasploit Framework.
#### [modicon_command](https://github.com/rapid7/metasploit-framework/blob/master/modules/auxiliary/admin/scada/modicon_command.rb) – Schneider Modicon Remote Start/Stop Command

The Schneider Modicon with Unity series of PLCs use Modbus function code 90 (0x5a) to perform administrative commands without authentication.

This module allows a remote user to change the state of the PLC between STOP and RUN. STOP will stop the CPU and will stop the PLC from monitoring and controlling the process. The CPU can be restarted with the RUN command.

#### [modicon_password_recovery](https://github.com/rapid7/metasploit-framework/blob/master/modules/auxiliary/admin/scada/modicon_password_recovery.rb) – Schneider Modicon Quantum Password Recovery

This Metasploit module retrieves the user-definable login names and passwords to a Schneider Modicon Quantum PLC and stores them in the Metasploit database. It uses a hard coded backdoor account to retrieve the account information via FTP (see ‘Backdoors’ below for a list of possible account names and passwords). Most account information is stored in plaintext.

Three types of credentials are currently retrieved by the modicon_password_recovery module: one is a username and password for the Modicon webserver login, and a second is just a password, which allows control operations to be performed via the web interface (called the ‘Write password’).

The third is a user-definable ftp account, the password of which is protected by the easily-cracked vxWorks loginDefaultEncrypt() hashing function. Recovering this password can be accomplished with the Metasploit framework’s vxworks password cracking tools.  Note that the tool may give a ‘plaintext’ version of the password with non-ASCII characters.  This is fine — these passwords may be used to log in to the device (although they won’t be typeable on a keyboard and will have to be used programmatically).

#### [modicon_stux_transfer](https://github.com/rapid7/metasploit-framework/blob/master/modules/auxiliary/admin/scada/modicon_stux_transfer.rb) – Schneider Modicon Ladder Logic Upload/Download

The Schneider Modicon with Unity series of PLCs use Modbus function code 90 (0x5a) to send and receive ladder logic. The protocol is unauthenticated, and allows a rogue host to retrieve the existing logic and to upload new logic.

Two modes are supported: “SEND” and “RECV,” which behave as one might expect — use ‘set mode ACTIONAME’ to use either mode of operation.

In either mode, FILENAME must be set to a valid path to an existing  file (for SENDing) or a new file (for RECVing), and the directory must already exist. The default, ‘modicon_ladder.apx’ is a blank ladder logic file which can be used for testing. It will overwrite existing ladder logic on the PLC.

This is the same PLC attack methodology as Stuxnet, hence stux in the module name. An attacker would need to gain access to PLC ladder logic, which is possible with the RECV mode in this module. The attacker would then determine how they want to change the process and code the corresponding ladder logic. Then the attacker would upload his rogue ladder logic using the SEND mode in this module.

### Fingerprinting
The Quantum series may be found on search engines such as Shodan and ERIPP using the Server: identifier “Schneider-WEB”.

### Backdoors
The Quantum also contains a large number of backdoor accounts.  For example following accounts may be used to log in to the Ethernet card via telnet and ftp:

ftpuser/password

qbf77101/hexakisoctahedron

When demonstrating the modicon_password_recovery metasploit module, it may be necessary to try several of these accounts.  The exact backdoor account names and passwords vary between the different Ethernet module order numbers.
