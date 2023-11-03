=============================================================
Multi-Instance Distributed Process Execution Manager (MIDPEM)
=============================================================

This program allows for configurable and multi-process remote code execution
among multiple devices (identifiable by the ID in "id.txt")

Edit the "main" function in the "bot.py" file to customize MIDPEM remote
execution.  This "main" function should start process(es) to complete some
task, and return a list of ALL processes started during its lifetime.

When the remote controller "start" command is given, main will be run, its
processes will start, and these reported processes will be stored by the MIDPEM
program.  Then, when the "stop" command is given, these reported processes will
be terminated.

To start the manager, edit the bot token and add a bot to controller Discord
server, then run "man.py" on all desired remote controlled devices.

[ NOTE: on larger distributed systems, using the "all devices" command variant
  will often throw a built-in Discord "rate limit" error -- this is unfortunately
  not something that can be avoided, and the recommended solution is to create
  auxiliary helper scripts to iterate through devices and execute individual
  commands with built-in delay ]

=========
Commands:
=========

$start <device_id>
------------------
alias: $st
brief: used to start/restart remote connected bot with given ID

$startall
---------
alias: $sta
brief: used to start/restart all remote connected bots

$stop <device_id>
-----------------
alias: $sp
brief: used to stop remote connected bot with given ID

$stopall [halted]
--------
alias: $spa
brief: used to stop all remote connected bots (add "halted" flag after command
       to only startup devices that are currently not running)

$sendfiles <device_id>
----------------------
alias: $sendfile, $sf
brief: used to send file(s) attached in command message to bot with given ID

$sendfilesall
-------------
alias: $sendfileall, $sfa
brief: used to send file(s) attached in command message to all connected bots

$getfiles <device_id> *[filenames]
----------------------------------
alias: $getfile, $gf
brief: used to fetch file(s) from bot with given ID to send to control server

$getfilesall *[filenames]
-------------------------
alias: $getfileall, $gfa
brief: used to fetch file(s) from all connected bots to send to control server

$status [device_id]
-------------------
alias: $ss
brief: used to get execution status of bot with given ID (or all bots)

$statusall
----------
alias: $ssa
brief: used to get execution status of all connected bots

$shell <device_id> *[command]
-----------------------------
alias: $sl
brief: used to execute shell commands on bot connected device with given ID

$shellall *[command]
--------------------
alias: $sla
brief: used to execute shell commands on all bot connected devices

$shellprocess <device_id> *[command]
-----------------------------
alias: $shellp, $slp
brief: used to execute shell process on bot connected device with given ID
       (unlike with "$shell" program will not halt to wait for a response)
	  
$shellprocessall *[command]
-----------------------------
alias: $shellpall, $shellpa, $slpa
brief: used to execute shell process on all bot connected devices
       (unlike with "$shellall" program will not halt to wait for a response)

$systemoff <device_id>
---------------------
alias: NO ALIAS
brief: used to switch off MIDPEM manager on bot with given ID

$systemoffall
---------------------
alias: NO ALIAS
brief: used to switch off MIDPEM manager on all bot connected devices
