# TODO: consider adding a "CharacterClass" property
# that restricts who can use an exit
class Exit:
    '''Class representing an Exit
    Exits link a set of names with a particular location
    Contains: 
        a list of strings [exit names]
        destination [the location this points to]
    There are also several variables involved with filtering:
        _whitelist - players and classes allowed through
        _blacklist - players and classes forbidden
        closed - set True to close this exit to EVERYONE
        restricted - True to apply restrictions; False if unrestricted
        assume_include -what happens to players neither in whitelist|blacklist
            If True: players not in lists are allowed in
            If False: players not in lists are forbidden
    The list can be accessed by treating the this as an iterable
    For instance:
        "exit_name" in myExit [returns true if "exit_name" is in exit]
        for exit_name in myExit:
            [iterates over all the possible exit names]
    For accessibility manipulation:
        exit << thing [true if exit is accessible to thing]
        exit += thing [include thing in exit]
        exit -= thing [exclude thing in exit]
    '''
    def __init__(self, destination, primary_name, *other_names, **kwargs):
        '''Constructor for Exit
        Takes as input:
            location [location it points to]
            at least one name is required [primary name]
            additional names are optional
            optional keyword arguments (whitelist, blacklist, assume_include)
        '''
        self._destination = destination
        self._names = [primary_name] + list(other_names)
        self._whitelist = []
        self._blacklist = []
        if 'whitelist' in kwargs:
            self._whitelist.extend(kwargs['whitelist'])
        if 'blacklist' in kwargs:
            self._blacklist.extend(kwargs['blacklist'])
        print(self._blacklist)
        self.closed = False
        self.restricted = True
        self.assume_include = True
        if 'assume_include' in kwargs:
            self.assume_include = kwargs['assume_include']
        else:    
            if len(self._whitelist) > 0:
                # if whitelist and blacklist are provided
                # then there is an ambiguity that must be resolved
                if len(self._blacklist) > 0:
                    ex = ("When both whitelist and blacklist keyword args "
                         "are provided, boolean keyword \'assume_include\' "
                         "must be supplied")
                    raise Exception(ex)
                else:
                    self.assume_include = False
    
    def get_destination(self):
        return self._destination
    
    def __eq__(self, other):
        '''Overriding ==
        Returns True if:
            other is an Exit that points to the same location
            other is a string that is in the list
        '''
        try:
            return self._destination == other._destination
        except AttributeError:
            return other in self._names

    def is_accessible(self, other):
        '''Overriding << pe
        Returns True if this Exit is accessible to 
        player or class [other]
        '''
        if self.closed:
            return False
        if not self.restricted:
            return True
        # checking if other is an instance of type
        # for instance, a character is an instance of a CharacterClass
        # if we pass in a character, this block will be executed
        # if we pass in a CharacterClass, this block will be skipped
        if not isinstance(other, type):
            if other in self._blacklist:
                return False
            if other in self._whitelist:
                return True 
            other = type(other)
        if self.assume_include:
            return other not in self._blacklist
        else:
            return other in self._whitelist
        
    def include(self, other):
        '''
        include [other], allowing them to access this exit
        that is, remove from internal blacklist, add to the whitelist
        this will make [other] be included
        '''
        if other in self._blacklist:
            self._blacklist.remove(other)
        if not other in self._whitelist:
            self._whitelist.append(other)

    def exclude(self, other):
        '''
        exclude [other] from accessing this exit
        that is, remove from internal whitelist, and add to the blacklist
        '''
        if other in self._whitelist:
            self._whitelist.remove(other)
        if other not in self._blacklist:
            self._blacklist.append(other)

    def __lshift__(self, other):
        '''overriding <<
        returns true if this exit is accessible to [other]
        '''
        return self.is_accessible(other)
    
    def __iadd__(self, other):
        '''overriding +=
        this will make [other] be included
        '''
        self.include(other)
        return self
    
    def __isub__(self, other):
        '''overriding -=
        this will make [other] be excluded
        '''
        self.exclude(other)
        return self

    def __eq__(self, other):
        '''overriding ==
        if a name is provided, returns true this exit contains the name
        if a Location is provided, returns true if it is the destination
        else, returns true if the exit equals this exit
        '''
        if isinstance(other, str):
            return other in self
        elif isinstance(other, Location):
            return self._destination == other
        else:
            return self is other

    def __contains__(self, other):
        '''Overriding in operator
        Returns True if other is in list of names
        '''
        return other in self._names

    def __iter__(self):
        for name in self._names:
            yield name
    
    def __str__(self):
        '''overriding str() function'''
        return "%s: %s" % (self._names[0], self._destination.name)


class Location:
    '''Class representing an in-game Location
    Maintains a list of players
    Contains a list of exits to other locations
    Has a name and description
    '''

    #TODO change "player" to "character"
    def __init__(self, name, description):
        self._character_list = []
        self._exit_list = []
        self.name = name
        self.description = description
        # this will come into play later
        self.owner = None

    def add_char(self, char):
        self._character_list.append(char)
        char.set_location(self)
    
    def remove_char(self, char, silent=False, exit=None):
        self._character_list.remove(char)
        if not silent:
            if exit is not None:
                self.message_chars("%s left via %s" )
            else:
                self.message_chars("%s left." % char)
    
    def get_character_list(self):
        return list(self._character_list)
    
    def message_chars(self, msg):
        '''send message to all characters currently in location'''
        for char in self._character_list:
            char.message(msg)
    
    def add_exit(self, exit_to_add):
        '''adds an exit, while performing a check for any ambigious names'''
        for exit_name in exit_to_add:
            assert exit_name not in self._exit_list, \
            "\nLocation:\t%s\nExit:\t\t%s" % (self.name, exit_to_add)
        self._exit_list.append(exit_to_add)

    def exit_list(self):
        '''returns a copy of private exit list'''
        return list(self._exit_list)

    def get_exit(self, exit_name):
        '''returns an exit corresponding to exit name
        if exit name is not in list, error is raised'''
        for exit in self._exit_list:
                if exit_name == exit:
                    return exit
        raise KeyError("Exit with name \'%s\' not in Location %s"
            % (exit_name, self.name))

    def __eq__(self, other):
        return self.name == other

    def __contains__(self, other):
        '''Overriding in operator
        Returns True if:
            if it is an exit or string:
                there exists an exit in _exit_list that matches
            if it is a Character or id:
                there exists a player with that id
        '''
        if isinstance(other, Exit) or isinstance(other, str):
            return other in self._exit_list
        #replace int with Player
        elif isinstance(other, character.Character):
            return other in self._character_list
        else:
            raise ValueError("Received %s, expected Exit/string, "
                             "Player/int" % type(other))

    def __str__(self, verbose=False):
        '''supplies a string
        if verbose is selected, description also supplied
        '''
        if verbose:
            return "%s:\n%s" % (self.name, self.description)
        else:
            return self.name

# explanation for this import statement being at the bottom
# location uses the Character class
# Character references Location class in body of Character class
import character
