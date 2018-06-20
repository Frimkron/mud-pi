from location import Location
#from character import Player, CharacterClass
'''library holding dictionaries for in-game objects'''

#delete this once character module exists
class CharacterClass:
    pass

locations = None
character_classes = None
playernames = None
server = None

def store_lib(input_library):
    '''unpacks a library produced by fileparser.py
    stores it in the module as library.[class_name]
    '''
    # referring to the the global names in the module
    global locations, character_classes
    if Location in input_library:
        locations = input_library[Location]
    if CharacterClass in input_library:
        character_classes = input_library[CharacterClasses]


def store_server(input_server):
    '''stores [input_server] as library.server'''
    global server
    server = input_server
