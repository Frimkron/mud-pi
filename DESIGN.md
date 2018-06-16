# MuddySwamp Design

Note that the time of writing, none of this code exists. This is a design document intended to describe the layout of the project once it does start running. Once the code is underway, this document will evolve. 

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

### Location.py 
  - defines Location class
  - Each location includes
    - a name
    - a list of current players
    - owner (a Character)
    - list of Interactable objects

### Character.py
  - defines Character class — which serves as template for other classes (might be a metaclass)

## Utilities

Utilties found in `./util/`

### Tester.py 
  - needs better name
  - checks all Locations, Characters, and Interactables

s
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