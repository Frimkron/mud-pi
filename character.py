import location
import control
from time import time
'''Module defining the CharacterClass metaclass, and Character base class'''

def camel_to_space(name):
    '''adds spaces before capital letters
    ex: CamelCaseClass => Camel Case Class'''
    output = ""
    for letter in name:
        if letter.upper() == letter:
            output += " "
        output += letter
    return output.strip()


class CharacterClass(type):
    '''The metaclass for all Character class
    key features:
        name: how the class appears to the players
        commands: a dictionary of all user commands
        unique_commands: a list of commands not found in base classes
        help_menu: a preformatted help menu, printed when 'help' is called
    '''
    def __init__(self, cls, bases, dict):
        # creating the proper name, if one is not provided
        if "name" not in dict:
            self.name = camel_to_space(cls)
        # adding a frequency field, if not already provided
        if "frequency" not in dict:
            self.frequency = 1
        # creating a dictionary of commands
        # all functions starting with cmd_ are commands
        self.commands = {}
        for func in dir(self):
            if func.startswith("cmd_"):
                self.commands[func[4::]] =  getattr(self, func)
        # building the unique_commands
        # a unique command is not found in any of the base classes
        self.unique_commands = []
        character_bases = [base for base in bases if hasattr(base, "commands")]
        for command in self.commands:
            # if the command does not appear in any of the base classes
            if not any(command in base.commands for base in character_bases):
                self.unique_commands.append(command)
        # building the help menu
        self.help_menu = self._build_help_menu(bases)
        # calling the super init
        super().__init__(cls, bases, dict)
    
    def _build_help_menu(self, bases):
        '''building a help menu, with the commands from each base on coming
        before the commands unique to this class'''
        output = ""
        for base in bases:
            if isinstance(base, CharacterClass):
                output += base.help_menu
        output += "[%s Commands]\n" % self
        output += "\t".join(self.unique_commands) + "\n"
        return output

    def __str__(self):
        return self.name


def cooldown(delay):
    def delayed_cooldown(func):
        setattr(func, "last_used", 0)
        def cooled_down_func(*args, **kwargs):
            print(func.last_used + delay)
            print(time())
            diff = func.last_used + delay - time()
            if diff < 0:
                func.last_used = time()
                return func(*args, **kwargs)
            else:
                raise Exception("Cooldown expires in : %i" % diff)
        return cooled_down_func
    return delayed_cooldown


class Character(metaclass=CharacterClass):
    '''Base class for all other characters'''

    starting_location = location.Location("NullLocation", "Default Location")
    name = "Default Character"
    names = {}

    def __init__(self):
        super().__init__()
        self.name = None
        self.location = None
        self.set_location(self.starting_location, True)

    def message(self, msg):
        '''send a message to the controller of this character'''
        self.name = None
        self.location = None
        self.set_location(self.starting_location, True)

    def message(self, msg):
        '''send a message to the controller of this character'''
        if self.controller is not None:
            self.controller.write_msg(msg)
    
    def detach(self, hard_detach=False):
        '''removes a character from its controller
        if hard_detach is True, the player enter its
        death process, defined by die
        '''
        # calling method from control.Receiver
        super().detach()
        if hard_detach:
            self.die()

    def update(self):
        while self.controller.has_cmd():
            line = self.controller.read_cmd()
            if line.strip() == "":
                continue
            if self.name is None:
                try:
                    self.player_set_name(line.strip())
                except Exception as ex:
                    self.message(str(ex))
                finally:
                    return
            try:
                self.parse_command(line)
            except Exception as ex:
                self.message(str(ex))

    def _set_name(self, new_name):
        '''changes a characters's name, with all appropriate error checking'''
        if new_name in Character.names:
            raise PlayerException("Name already taken.")
        if self.name is not None:
            del(self.names[self.name])
        self.name = new_name
        self.names[self.name] = self
    
    def player_set_name(self, new_name):
        '''intended for first time players set their name'''
        if not new_name.isalnum():
            raise PlayerException("Names must be alphanumeric.")
        self._set_name(new_name)
        #TODO: replace this when appropriate
        from library import server
        server.send_message_to_all("Welcome, %s, to the server!" % self)
        self.cmd_look("")
        
    def set_location(self, new_location, silent=False, reported_exit=None):
        '''sets location, updating the previous and new locations as appropriate
        if reported_exit is supplied, then other players in the location 
        will be notified of which location he is going to
        '''
        # break recursive loop
        if self.location == new_location:
            return
        try:
            self.location.remove_char(self, silent, reported_exit)
        except AttributeError:
            # location was none
            pass
        self.location = new_location
        self.location.add_char(self)

    def parse_command(self, line):
        '''parses a command, raises AttributeError if command cannot be found'''
        command = line.split(" ")[0]
        args = line[len(command)::].strip()
        if command not in self.commands:
            raise AttributeError("Command \'%s\' not recognized." % command)
        method = self.commands[command]
        method(self, args)
    
    def _remove_references(self):
        '''method executed when a character is being removed
        this takes care of any undesired references, and allows
        the player to die'''
        try:
            self.location.remove_char(self)
            self.location = None
        except AttributeError:
            # location is none
            pass
        
        # delete character from the name dictionary
        try:
            del self.names[self.name]
        except KeyError:
            pass

    def die(self):
        '''method executed when a player dies'''
        self._remove_references()
        
    def __str__(self):
        if self.name is None:
            return "A nameless %s" % self.__class__.name
        return "%s the %s" % (self.name, self.__class__.name) 

    def __del__(self):
        self.die()
    
    def cmd_help(self, args):
        '''Show relevant help information for a particular command.
        usage: help [command]
        If no command is supplied, a list of all commands is shown.
        '''
        if len(args) == 0:
            self.message(self.__class__.help_menu)
            return
        command = args.split(" ")[0]
        if command in self.commands:
            self.message(self.commands[command].__doc__)
        else:
            raise AttributeError("Command \'%s\' not recognized." % command)

    def cmd_look(self, args):
        '''Provide information about the current location.
        usage: look
        '''
        self.message(self.location.__str__(True))
        exit_list = self.location.exit_list()
        exit_msg = "\nExits Available:\n"
        if len(exit_list) == 0:
            exit_msg += "None"
        else:
            exit_msg += " ,".join(map(str, exit_list))
        self.message(exit_msg)

    def cmd_say(self, args):
        '''Say a message aloud, sent to all players in your current locaton.
        usage: say [msg]
        '''
        self.location.message_chars("%s : %s" % (self, args))
    
    def cmd_walk(self, args):
        '''Walk to an accessible location.
        usage: walk [exit name]
        '''
        exit_name = args.split(" ")[0]
        exit = self.location.get_exit(exit_name)
        self.set_location(exit.get_destination(), False, exit)
