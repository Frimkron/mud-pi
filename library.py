from location import Location
from character import CharacterClass
from util.distr import RandDist
#from character import Player, CharacterClass
'''library holding dictionaries for in-game objects'''

locations = None
character_classes = None
server = None
random_class = None

def store_lib(input_library):
    '''unpacks a library produced by fileparser.py
    stores it in the module as library.[class_name]
    '''
    # referring to the the global names in the module
    global locations, character_classes, random_class
    if Location in input_library:
        locations = input_library[Location]
    if CharacterClass in input_library:
        character_classes = input_library[CharacterClass]
        # gathering the frequencies for each CharacterClass
        frequencies = [c_class.frequency for c_class in character_classes.values()]
        # creating a dictionary with each frequency
        freq_dict = dict(zip(character_classes, frequencies))
        # creading a Random Distribution for each class
        random_class = RandDist(freq_dict)



def store_server(input_server):
    '''stores [input_server] as library.server'''
    global server
    server = input_server
