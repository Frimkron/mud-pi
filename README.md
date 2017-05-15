MUD Pi
======

A simple text-based Multi-User Dungeon (MUD) game, which could be run on a 
Raspberry Pi or other low-end server.


Requirements
------------

You will need to install _Python_ (2.7+ or 3.3+) where you wish to run the 
server. Installers for Windows and Mac can be found at 
<http://www.python.org/download/>. There are also tarballs for Linux, although 
the best way to install on Linux would be via the package manager.

To allow players to connect remotely, the server will also need to be connected
to the internet. 

To connect to the server you will need a telnet client. On Mac, Linux, and 
versions of Windows prior to Windows Vista, the telnet client is usually 
installed by default. For Windows Vista, 7, 8 or later, you may need to follow
[this guide](http://technet.microsoft.com/en-us/library/cc771275%28v=ws.10%29.aspx)
to install it.


Running the Server
------------------

### On Windows

Double click on `simplemud.py` - the file will be opened with the Python 
interpreter. To stop the server, simply close the terminal window.


### On Mac OSX and Linux (including Raspberry Pi)

From the terminal, change to the directory containing the script and run 

	python simplemud.py
	
Note, if you are connected to the machine via SSH, you will find that the 
script stops running when you quit the SSH session. A simple way to leave the 
script running is to use a tool called `screen`. Connect via SSH as usual then
run `screen`. You will enter what looks like a normal shell prompt, but now you
can start the python script running and hit `ctl+a` followed by `d` to leave
_screen_ running in the background. The next time you connect, you can 
re-attach to your screen session using `screen -r`. Alternatively you could
[create a daemon script](http://jimmyg.org/blog/2010/python-daemon-init-script.html)
to run the script in the background every time the server starts.


Connecting to the Server
------------------------

If the server is running behind a NAT such as a home router, you will need to 
set up port **1234** to be forwarded to the machine running the server. See your
router's instructions for how to set this up. There are a large number of 
setup guides for different models of router here: 
<http://portforward.com/english/routers/port_forwarding/>

You will need to know the _external_ IP address of the machine running the 
server. This can be discovered by visiting <http://www.whatsmyip.org> from
that machine.

To connect to the server, open your operating system's terminal or command
prompt and start the telnet client by running:

	telnet <ip address> 1234
	
where `<ip address>` is the external IP address of the server, as described 
above. 1234 is the port number that the server listens on.

If you are using Windows Vista, 7, 8 or later and get the message:

	'telnet' is not recognized as an internal or external command, operable
	program or batch file.
	
then follow 
[this guide](http://technet.microsoft.com/en-us/library/cc771275%28v=ws.10%29.aspx)
to install the Windows telnet client.

If all goes well, you should be presented with the message 

	What is your name?

To quit the telnet client, press `ctl + ]` to go to the prompt, and then 
type `quit`.


What is Telnet?
---------------

Telnet is simple text-based network communication protocol that was invented in
1969 and has since been superseded by other, more secure protocols. It does 
remain popular for a few specialised uses however, MUD games being one of these
uses. A long (and boring) history of the telnet protocol can be found here:
<http://www.cs.utexas.edu/users/chris/think/ARPANET/Telnet/Telnet.shtml>


What is a MUD?
--------------

MUD is short for Multi-User Dungeon. A MUD is a text-based online role-playing
game. MUDs were popular in the early 80s and were the precursor to the 
graphical Massively-Multiplayer Online Role-Playing Games we have today, like 
World of Warcraft. <http://www.mudconnect.com> is a great site for learning 
more about MUDs.


Extending the Game
------------------

MUD Pi is a free and open source project (that's _free_ as in _freedom_). This 
means that the source code is included and you are free to read it, copy it, 
extend it and use it as a starting point for your own MUD game or any other 
project. See `licence.md` for more info.

MUD Pi was written in the Python programming language. If you have never used
Python before, or are new to programming in general, why not try an online
tutorial, such as <http://www.learnpython.org/>.

There are 2 source files in the project. `mudserver.py` is a module containing
the `MudServer` class - a basic server script which handles player connections 
and sending and receiving messages. `simplemud.py` is an example game using 
`MudServer`, with player chat and rooms to move between. 

The best place to start tweaking the game would be to have a look at 
`simplemud.py`. Why not try adding more rooms to the game world? You'll find
more ideas for things to try in the source code itself.

Of course if you're feeling more adventurous you could take a look at the 
slightly more advanced networking code in `mudserver.py`.


Author
------

MUD Pi was written by Mark Frimston

For feedback, please email <mfrimston@gmail.com> or add a comment on the 
project's [Github page](http://github.com/frimkron/mud-pi)
