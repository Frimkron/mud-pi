import location
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
        # creating the proper name
        if "name" not in dict:
            self.name = camel_to_space(cls)
        self.unique_commands = []
        self.commands = {}
        # creating a dictionary of commands
        # all functions starting with cmd_ are commands
        for func in dir(self):
            if func.startswith("cmd_"):
                self.commands[func[4::]] =  getattr(self, func)
        # building the unique_commands
        character_bases = [base for base in bases if hasattr(base, "commands")]
        for command in self.commands:
            # if the command does not appear in any of the base classes
            if not any(command in base.commands for base in character_bases):
                self.unique_commands.append(command)
        # building the help menu
        self.help_menu = self.build_help_menu(bases)
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


class Character(metaclass=CharacterClass):
    starting_location = location.Location("NullLocation", "Default Location")
    name = "Default Character"
    names = {}

    def __init__(self, controller):
        self.name = None
        self.controller = controller
        self.location = None
        self.set_destination(self.starting_location)

    def message(self, msg):
        '''send a message to the controller of this character'''
        self.controller.write_msg(msg)

    def die(self):
        '''method executed when a player dies'''
        pass
        #print(repr(self) + " died")

    def set_name(self, new_name):
        '''changes a characters's name, with all appropriate error checking'''
        if new_name in Character.names:
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
    
    def detach(self, hard_detach=True):
        '''removes a character from its controller
        if hard_detach is True, the player enter its
        death process, defined by die
        '''
        try:
            self.controller.receiver = None
        except AttributeError:
            return
        self.controller = None
        if hard_detach:
            self._die()
    
    def attach(self, controller):
        self.detach(True)
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
        self.location.remove_char(self, silent=True)
    
    def cmd_talk(self):
        print("talking")
    
    def cmd_meme(self):
        print("memeing")
    
    '''
    def _get_help_menu(self, cls=None):
        if cls is None:
            cls = type(self)
        output = ""
        output += "[%s Commands]\n" % type(self)
        output += "\t".join(self.unique_commands)
        try:
            output += self._get_help_menu(super(cls))
        except AttributeError as ex:
            print(ex)
        except Exception:
            pass
        return output
    '''

    def cmd_help(self):
        '''Prints a help menu.'''
        print(self.__class__.help_menu)
    
    def sup(self):
        print(super())
        

class DarkWizard(Character):
    def cmd_enchant(self):
        print("boom")
    
    def sup(self):
        print(super())

rob = Character("meme", None)
rab = DarkWizard("meme2", None)
rab.cmd_help()
print("done")
