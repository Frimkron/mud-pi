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
>>> Mr. Magic Beard
Announcement: Welcome to the server, Mr. Magic Beard the Wizard!
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

### Note on implementation:
These help menus will be generated at runtime using docstrings. For a user-level function, **a docstring should be provided**. 

Moreover, the dictionary of user-level functions is generated at runtime. This is done by looking at the attributes of a CharacterClass when it is constructed. All beginning with `cmd_` are considered user-level functions.

Here is an example:

```python
class Wizard(CharacterClass):
  def __str__(self):
      '''overriding the str() function'''
      return self.name + str(self.level)

  def _level_check(self):
      '''internal method to check level'''
      if self.xp > 1000:
          self.level += 1
          self.xp = 0
  
  def add_spell(self, spell):
    '''add a spell, making it available to this wizard'''
    self.spells = spell
  
  def cmd_cast(self, spell, *args):
    '''usage: cast [spellname] [arguments]
    Cast [spellname] with arguments. Arguments very by spell.
    '''
    if spell in self.spells:
        # cast the spell
        spell(args)
```
A few things to note:

 - `__str__` is a special method that hooks into a top level function. You can read about those [here](https://docs.python.org/3/reference/datamodel.html).

 - `_level_check` is an internal method, which signals to other programmers that this method should not be called outside the class. (C++/Java programmers, think `private`).
 - `add_spell` is a normal method, intended to be executed anywhere.
 - `cmd_cast` is a user-level method, which can be executed anywhere, or executed by the user as shown above.

 These implementation notes will be likely be moved to another document.
 
## Components
### MudServer.py (Core Server)
  - Based on the MUD Pi code
  - Only changed as necessary
  - handles events like new players joining
  - sends / receives messages

### MuddySwamp.py 
  - Creates/uses an instance of MudServer
  - imports locations from `./locations/`
    - locations in json format
    - creates an instance of Location class (defined in Location.py)
    - puts new location in dict with name as key
  - imports Characters form `./characters/`
    - Characters use a json format
    - Each json includes a path to a script that defines Character behavior
    - Script must define `class [NAME]` where `[NAME]` is the name of the character
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

### character.py
  - defines Character class — which serves as template for other classes (might be a metaclass)

### fileparser.py
  - responsible for importing in-game locations, items, CharacterClasses

## Utilities

Utilties found in `./util/`

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