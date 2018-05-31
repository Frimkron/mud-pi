# MuddySwamp

Multi-user dungeons, or "MUDs" are text-based role-playing games, that naturally evolved from the text-based rpg and adventure games of the 1970s. This project aims to introduce a new generation—one that never experienced a world without broadband internet—to this classic game genre. While this code can be adapted for any setting, we intend to render our university in beautiful ASCII. 

## Requirements
  - For **connecting** to an existing server, a simple telnet client is required.
  - For **hosting** a server, Python 3 must be installed on the system (along with an appropriate internet connection.) For Python installation, visit <https://www.python.org>

## Getting Started

### Hosting

Download this repository, or one of the releases. In a terminal, navigate to the repository and run

    python simplemud.py

More details will be added here as the project evolves.

If you are hosting a server for other people to connect, you will need to port foward your router (by default, the port used is **1234**). This is done so that traffic on port **1234** will be directed to the machine hosting the server.

### Connecting

Simply connect with a telnet client of your choosing. By default, the server uses port **1234**. 

#### On MacOS, Linux, and other *nix Systems:

Navigate to the terminal, and type

    telnet <ip address> 1234
		
#### On MacOS High Sierra and higher

Navigate to the terminal, and type

    nc <ip address> 1234

#### On Windows:

A telnet client is not provided by default on Windows. One option is to follow [this guide](http://technet.microsoft.com/en-us/library/cc771275%28v=ws.10%29.aspx)
to install the Windows telnet client.

Alternatively, you can install [PuTTY](https://putty.org/), a **free and open source** telnet and ssh client. 

## Contributing

Please read **[CONTRIBUTING.md](CONTRIBUTING.md)** for how to work on the project.

## License

This project is licensed under the **MIT** License - see the [LICENSE.md](LICENSE.md) file for details.
