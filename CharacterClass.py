import location
from abc import ABCMeta, abstractmethod
import queue
# TODO: make abstract?
class Controller(metaclass=ABCMeta):
    '''Abstract base class for implementing a Controller
    a Controller acts as two streams
    a stream of instructions (controlled by .read())
    '''
    def __init__(self):
        self.character = None
        self.input_stream = None

    def assume_control(self, character):
        character.detach()
        character.attach(self)
    
    @abstractmethod
    def poke(self):
        pass
    
    @abstractmethod
    def read(self):
        pass
    
    @abstractmethod
    def has_input(self):
        pass


        

class Player(Controller):
    '''Player class acts as a stream of incoming data
    '''
    player_ids = {}
    def __init__(self, id):
        if id in self.player_ids:
            raise Exception("ID already taken: %s" % id)
        self.id = id
        self.player_ids[id] = self
        self._command_queue = queue
        super().__init__()
    
    def poke(self):
        try:
            self.character.update()
        except AttributeError:
            pass

    def read(self):
        return self._command_queue.get()

    def has_input(self):
        return not self._command_queue.empty()

    def __del__(self):
        print(self.character)
        try:
            self.character.die()
            self.character.detach()
        except AttributeError:
            # self.character is most likely None
            pass
        print(repr(self) + " disconnected")
    
    @classmethod
    def receive_message(id, message):
        Player.player_ids[id]._command_queue.put(message)
            

class Nonplayer:
    '''Nonplayer acts as a stream of incoming data
    '''
    pass

class CharacterClass:
    #metaclass
    #dip through and construct two things:
    # a Class.commands dict
    # a help menu


class Character:

    starting_location = location.Location("Null", "Default Location")
    names = {}

    def __init__(self, name, controller):
        self.name = name
        self.controller = controller
        self.set_destination(starting_location)

    def die(self):
        '''method executed when a player is deleted'''
        print(repr(self) + " died")

    def set_name(self, new_name):
        '''changes a characters's name, with all appropriate error checking'''
        if new_name in self.names:
            raise "Name already taken"
        if self.name is not None:
            del(self.names[self.name])
        self.name = newname
        player_names[self.name] = self

    #TODO: fix
    def parse_command(self, line):
        command = line.split(" ")[0]
        if command not in self.commands:
            raise AttributeError("Command not recognized.")
        method = self.commands[command]
        self.method(line)
    
    def detach(self):
        try:
            self.controller.character = None
        except AttributeError:
            return
        self.controller = None
    
    def attach(self, controller):
        self.detach()
        self.controller = controller 
        self.controller.character = self
    
    def set_destination(self, new_location):
        try:
            self.location.remove_char(self)
        except AttributeError:
            # location was none
            pass
        self.location = new_location
        self.location.add_char(self)

    def update(self):
        while self.controller.has_input():
            self.parse_command(self.controller.read())
    
    def __del__(self):
        #TODO: make a hard delete option, that removes the character altogether?
        self.die()
        self.location.remove_character(silent=True)

class Location:
    
    def __init__(self):
        self.chars = []
    
    def add_char(char):
        self.chars.append(char)

p = Player(10)
while var != "meme":
    var = input()
    print(var)
x = 5 + 3
print(x)
