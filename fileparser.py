import json
from location import Location, Exit
from character import CharacterClass
from numbers import Number
import os
import sys
import importlib
'''
module that holds all parsers for file IO
'''
'''
General approach: Build objects based on static traits (name, description, etc.)
Dependencies are deferred until after the fact
This highlights a key note: that all dynamic attributes (i.e. attributes
defined in other files, or redefined at run time) should not be included
in the constructor.
Example:
Exits should be added after locations are made. Items should be added
to locations after locations and items are both made.
'''

class Dependency(Exception):
    ''' Class representing Dependence upon another dynamic object
    Contains:
        dependent : the filename that, when imported, created this dependency
        name : the name of the depended upon object
        classname : the assumed class of the dependend upon object
        resolution : a function that must be executed once this is resolved
    Usage note: 
        Confirm that dependency is actually resolved before resolving it
    '''

    def __init__(self, dependent, name, classname, resolution):
        self.dependent = dependent
        self.name = name
        self.classname = classname
        self.resolution = resolution
    
    def __str__(self):
        return "%s on %s of %s" \
                % (self.dependent, self.name, self.classname)

    def resolve(self):
        '''calls the resolution function'''
        self.resolution()
        eprint("Resolved dependency:\n%s" % str(self))
    
    def fail_message(self):
        '''supplies a message when depended upon object failed'''
        return "Dependent on %s, which failed to import." % self.name 
    
    def unresolved_message(self):
        '''supplies a message when depended upon object was never imported'''
        return "Dependent on %s, which doesn\'t exist." % self.name


class BaseParser:
    ''' a generic Parser to derive class-specific Parsers from
    contains:
        success_list : list of all successfully parsed objects
        depened_list : list of all yet-handled dependencies
        fail_list : list of all failures, with reasons for failing
        self.library : points to a library of objects of different
            classes. this will be used to link multiple parsers 
            together, so that, for instance, LocationParser can 
            see which objects have been passed through ItemParser
        self.fail_library : points to a library of objects that
            filed to parse
    
    When deriving from Parser, you must override import_file,
    defining a method to actually parse a file containing your
    desired object

    For the file-import method:
    Append a Dependency to the depend_list as necessary.
    '''
    def __init__(self, parsing_class, library, fail_library):
        self.success_list = {}
        self.depend_list = []
        self.fail_list = {}
        self.library = library
        self.fail_library = fail_library
        self.library[parsing_class] = self.success_list
        self.fail_library[parsing_class] = self.fail_list
 
    def resolve_dependencies(self):
        for depend in list(self.depend_list):
            if depend.name in self.library[depend.classname]:
                # dependency is ready to resolve
                depend.resolve()
                self.depend_list.remove(depend)
            elif depend.name in self.fail_library[depend.classname]:
                # dependency cannot be resolved because desired object
                # failed to import
                self.fail_list[depend] = depend.fail_message()
                self.depend_list.remove(depend)
            else:
                # dependency cannot be resolved because desired object
                # does not exist
                self.fail_list[depend] = depend.unresolved_message()
                self.depend_list.remove(depend)

    def all_to_str(self):
        '''cheap method to get an output for all values in each list'''
        output = "SUCCESS LIST\n"
        for success in self.success_list:
            output += str(success) + "\n"
        output += "DEPENDENCY LIST\n"
        for depend in self.depend_list:
            output += str(depend) + "\n"
        output += "FAILURE LIST\n"
        for name, reason in self.fail_list.items():
            output += str(name) + " :\n\t"
            output += str(reason) + "\n"
        return output


    def handle_import(self, filename):
        '''imports a file, handling possible failure'''
        try:
            imported_object = self.import_file(filename)
            self.success_list[str(imported_object)] = imported_object
        except Exception as ex:
            self.fail_list[filename] = ex

    def import_file(self, filename):
        '''implement this in the derived class'''
        pass


class LocationParser(BaseParser):
    '''Class for a Location-Specific parser'''

    def __init__(self, library={}, fail_library={}):
        # calling the constructor of BaseParser
        super().__init__(Location, library, fail_library)
    
    def import_file(self, filename):
        '''imports a Location from a json specified by [filename]'''

        # loading in json data
        with open(filename, "r") as location_file:
            json_data = json.load(location_file)

        # creating the location using its static attributes
        imported_location = Location(json_data["name"], 
                                    json_data["description"])
    
        # looking at each exit
        exit_list = []
        for exit in json_data["exits"]:
            destination_name = exit["destination"]
            names = exit["names"]
            ''' dilemma: we have no guarantee that destination has been
            imported yet, or that it even exists
            solution: create a depedency

            dependency needs a resolution function
            this function will be executed when we are ready to resolve
            note how variables not local to the scope are referenced
            look up "closure" if you want more information
            '''
            def resolve(destination_name=destination_name, names=names):
                # loading in destination
                destination = self.library[Location][destination_name]
                # creating an exit
                imported_exit = Exit(destination, *names)
                # adding exit to location
                imported_location.add_exit(imported_exit)
            dependency =  Dependency(imported_location, destination_name,
                                     Location, resolve)
            exit_list.append(dependency)
        self.depend_list.extend(exit_list)
        return imported_location

#make an optional "starting_location field for the json"
class CharacterParser(BaseParser):
    '''Class for Character-Specific parsing'''

    def __init__(self, library={}, fail_library={}):
        # Call the constructor from BaseParser
        super().__init__(CharacterClass, library, fail_library)
    
    def import_file(self, filename):
        '''Imports a Character from a json sepecified by [filename]'''

        # Try to read the json file
        with open(filename, 'r') as character_file:
            json_data = json.load(character_file)
        
        # Get the data out of the file
        imported_name = json_data["name"]
        imported_path = json_data["path"]

        # Check to make sure that the name and frequency are the right types
        if not isinstance(imported_name, str):
            raise TypeError('Wrong type when parsing character name or frequency')
        
        # Make sure the script exists
        if not os.path.exists(imported_path):
            raise IOError('Character path does not exist')
        
        # Try to get the script file from the json data
        module = importlib.import_module(imported_path.replace('.py', '').replace('/', '.'))
        character_class = module.__dict__[imported_name]

        # Check to see if the class imported actually exists
        if character_class is None:
            raise IOError("Could not find character class when parsing")
        # Return a new instance of the imported class
        if "frequency" in json_data:
            character_class.frequency = float(json_data["frequency"])
        return character_class


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def parse_all_files(parser, *files):
       '''parses all files with specified parser'''
       for filename in files:
           parser.handle_import(filename)


def import_files(**paths):
    '''parses all files in paths
    parsing occurs in the correct order
    returns a "library"
    '''
    library = {}
    fail_library = {}
    # creating our two parsers, linked to the libraries
    locations  = LocationParser(library, fail_library)
    char_classes = CharacterParser(library, fail_library)
    eprint(paths)
    if "locations" in paths:
        eprint("parsing locations")
        parse_all_files(locations, *paths["locations"])
        eprint(locations.all_to_str())
    # in the future, import items next
    if "chars" in paths:
        eprint("parsing char_classes")
        parse_all_files(char_classes, *paths["chars"])
        eprint(char_classes.all_to_str())
    locations.resolve_dependencies()
    char_classes.resolve_dependencies()
    return library


def get_filenames(directory, ext=""):
    '''returns all filenames in [directory] with extension [ext]'''
    return [directory + name for name in os.listdir(directory) \
            if name.endswith(ext)]
