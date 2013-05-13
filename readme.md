MUD Pi
======

A simple text-based Multi-User Dungeon (MUD) game, which could be run on a 
Raspberry Pi or other low-end server.


Requirements
------------

You will need to install Python (2.7+ or 3.3+)


Running the Server
------------------

### On Windows

Double click on "simplemud.py" - the file will be opened with the Python 
interpreter

### On Mac

** TODO **

### On Linux

From the terminal, change to the directory containing the script and run 

	sudo python simplemud.py
	
The script must be run as root in order to have permission to listen on port 23.


Connecting to the Server
------------------------

If the server is running behind a NAT such as a home router, you will need to 
set up port 23 to be forwarded to the machine running the server. See your 
router's instructions for how to set this up.

You will need to know the _external_ IP address of the machine running the 
server. This can be discovered by visiting <http://www.whatsmyip.org> from
that machine.

To connect to the server, open your operating system's terminal or command
prompt and start the telnet client by running:

	telnet <ip address>
	
where `<ip address>` is the external IP address of the server, as described 
above.


