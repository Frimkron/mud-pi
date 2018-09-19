# MuddySwamp Design

Note that the time of writing, only a portion of this code exists. This is a design document intended to describe the layout of the project once it does start running. Once the code is underway, this document will evolve. 

## Top-Down Description

When the player logs in, they will receive a message akin to this:
```
Welcome to MuddySwamp!
You are a(n): Wizard

What is your name?
>>>
```
At this point, the player will now enter a valid name.
```
>>> Bill
Announcement: Welcome to the server, Bill the Wizard!
```
That announcement will be sent to all players.

Now, the player is free to explore. At any time, they can view available abilities like so:
```
>>> help

Type "help [command]" for specific information.
Commands available:
[STANDARD COMMANDS]
help  say  tell  walk  report
[WIZARD COMMANDS]
cast  enchant  brew

>>> help report

usage: report [player name] [optional reason]
Report [player name] for violating server rules. 
Reports will be sent to the server logs for later review.
False reports may result in a response, as per the policy of the server admins.

>>> help cast

usage: cast [spellname] [arguments]
Cast [spellname] with arguments. Arguments very by spell. 
```

Coming soon: what does one do once they are in the game?
 
## Components
### mudserver.py (Core Server)
  - Based on the MUD Pi code
  - Only changed as necessary
  - handles events like new players joining
  - sends / receives messages

### fileparser.py
  - defines the Parser class
    - a Parser contains several lists
    - provides a framework for resolving dependencies
  - defines the derived parsers: LocationParser, CharacterParser, etc.
    - responsible for parsing respective files
  - contains `import_files` which returns a *library* ready to be unpacked
  - Locations follow a .json format (see ./locations/template)
  - CharacterClasses follow a .json format (see ./chars/template)

### library.py
  - makes in-game objects globally available
  - key fields:
    - `locations`: dictionary of locations, indexed by location name
    - `character_classes`: dictionary of character_classes, indexed by proper name
    - `random_class`: a random distribution, use `random_class.get()` to produce a random CharacterClass with appropriate weighting
    - `server`:  stored instance of a MudServer
  - key functions:
    - `store_lib(input_library)`: provide a library, which will be unpacked into all the appropriate variables
    - `store_server(input_server)`: provide an instance of MUD server, which will be stored as `server`

### MuddySwamp.py 
  - Creates/uses an instance of MudServer
  - imports locations from `./locations/`
  - imports Characters form `./characters/`
  - begin core loop
    - while the queue is not empty, handle events (new players, incoming messages, etc.) on the queue
    - if queue is empty, sleep

### location.py 
  - defines Location class
  - Each location includes
    - a name
    - a list of current players
    - owner (a Character)
    - list of Interactable objects
  - defines Exit class
    - a simple class representing an exit to some location
    - handles nicknames, names, etc.

### control.py
- defines Controller abstract class
  - the concept of a "Controller" is used to interface with different types of Controllers
  - Player, Nonplayer, etc. work as controllers
  - easily multithreaded
  - Key methods:
    - `assume_control(receiver)` take control of receiver
    - `read_cmd()` read a command from the input stream (used by receivers)
    - `write_msg(msg)` write feedback from the receiver back to the controller
    - `has_msg()` returns true if there is feedback available for the controller to read
    - `has_cmd()` returns true if there are commands available for the receiver to read
- defines the Player class
  - Players are Controllers that can be accessed by id
  - using Player.player_ids[id] allows server to grab any particular player
  - Players are used to interface with players connected
- future: Nonplayer
  - reads from file or script


### character.py
  - defines CharacterClass, the metaclass that in-game character classes
    - "Wizard" would be a CharacterClass
    - "Bill the Wizard" is a Wizard
  - defines Character, the base class for player-controlled characters
    - establishes default commands

## Utilities

Utilties found in `./util/`

### distr.py
  - defines the RandDist class
  - RandDist creates a weighted random distribution

### Tester.py [coming soon]
  - needs better name
  - checks all Locations, Characters, and Interactables


## Timeline (Work in Progress)

### Phase 1 (Really Really Minimal Viable Product)
  - "GatorChat"
  - ~~profanity filter~~ turns out this is a bad idea
    - if interested, read up on the "clbuttic mistake"
    - we have opted for a reporting system instead
  - player names
  - only one chat room

### Phase 2 (Really Minimal Viable Product)
  - introduce Locations, Location parsing
  - introudce Location-based parsing
  - introduce interactables?

### Phase 3 (True Minimal Viable Product)
  - introduce classes, command palettes vary by class
  - introduce goals
  - classes at this point should form core "Rock-Paper-Scissors" like nucleus for other classes to hook into

### Phase N
  - add additional locations, classes, and interactables