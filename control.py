import location
from abc import ABCMeta, abstractmethod
import queue

class Controller(metaclass=ABCMeta):
    '''Abstract base class for implementing a Controller
    self.receiver refers to the object under control
    this is most frequently a character

    a Controller acts as two streams
    a stream of instructions
        controlled by read_cmd and internal logic
    a stream of feedback messages to player
        controlled by write_msg and internal logic

    How to handle writing commands, and reading messages is
    decided by implementation.
    '''

    def __init__(self):
        '''a character must be pointed to, so we set to None'''
        self.receiver = None

    def assume_control(self, receiver):
        '''detaches a given character from its 
        controller, then attaches it to self
        for multiple concurrent controllers, this
        method may need to be extended
        '''
        receiver.detach()
        receiver.attach(self)

    def __add__(self, other):
        if not isinstance(other, Controller):
            raise TypeError("Cannot add non-Controller to Controller")
        # return MultiController(self, other)
 
    @abstractmethod
    def read_cmd(self):
        '''reads a comand, removes it from the queue'''
        pass
    
    @abstractmethod
    def write_msg(self, msg):
        '''writes a message to the message queue'''
        pass

    @abstractmethod
    def has_msg(self):
        '''returns true if there are messages to read'''
        pass
    
    @abstractmethod
    def has_cmd(self):
        '''returns true if there are commands to read'''
        pass


class MultiController(Controller):
    '''A wrapper for multiple controllers
    Note that this is itself a controller, meaning that
    MultiControllers can be built from other controllers
    
    The potential usecase for this would be if you had
    multiple players controlling a character, or a player
    and an AI fighting for control.

    Example usecase:
    player1 = Player(1)
    player2 = Player(2)
    multiplayer = MultiController(player1, player2)
    multiplayer.assume_control(DarkWizard("Dueling Spirit"))

    This would create a character which responds to the commands
    of both players simultaneously.
    '''
    def __init__(self, *controllers):
        self._ctrl_list = []
        for ctrl in controllers:
            assert isinstance(ctrl, Controller)
            # if ctrl is a multicontroller, we can directly extend it
            # into the ctrl_list, reducing recursive calls
            if isinstance(ctrl, MultiController):
                self._ctrl_list.extend(ctrl)
            # otherwise, it must be a regular Controller
            else:
                self._ctrl_list.append(ctrl)
    
    def assume_control(self, receiver):
        '''call the default Controller assume_control
        also make sure that all ctrls have a reference
        to the receiver
        '''
        super().assume_control(receiver)
        for ctrl in self:
            ctrl.receiver = receiver
    
    def __iter__(self):
        '''this method makes MultiController iterable
        this makes it possible to unpack the MultiController,
        as in __init__, and access specific controllers
        '''
        for ctrl in self._ctrl_list:
            yield ctrl
    
    def read_cmd(self):
        '''reads the first available message to be found'''
        for ctrl in self:
            if ctrl.has_cmd():
                return ctrl.read_cmd()
        #throw an error? 
    
    def write_msg(self, msg):
        '''sends a feedback message to all controllers'''
        for ctrl in self:
            ctrl.write_msg(msg)

    def has_msg(self):
        '''returns true if any controller has unanswered message'''
        return any(ctrl.has_msg() for ctrl in self)
    
    def has_cmd(self):
        '''returns true if any controller has a new command'''
        return any(ctrl.has_cmd() for ctrl in self)

#TODO: create a receiver base class?     

class Player(Controller):
    '''Player class assigns Controllers to each client ID
    '''
    player_ids = {}

    def __init__(self, id):
        if id in self.player_ids:
            raise Exception("ID already taken: %s" % id)
        self.id = id
        self.player_ids[id] = self
        self.receiver = None
        self._command_queue = queue.Queue()
        self._message_queue = queue.Queue()
    
    def poke(self):
        '''temporary method, used if running in 1 thread
         if only one thread is used, and the main loop
        of thread is handling Server Events, then the only
        way to update the characters, is through updating
        directly after adding a cmd to the queue

        in future multithreaded versions, this will be removed
        '''
        self.receiver.update()
        try:
            self.receiver.update()
        except AttributeError:
            pass

    def read_cmd(self):
        '''returns a command from the queue
        intended to be called from self.characte    
        '''
        return self._command_queue.get()
    
    def write_msg(self, msg):
        self._message_queue.put(msg)

    def has_cmd(self):
        return not self._command_queue.empty()
    
    def has_msg(self):
        return not self._message_queue.empty()     
    
    @classmethod
    def send_command(self, id, command):
        '''provides a means to rapidly multiplex commands
        in the main Server Event loop
        
        will send the command to the appropriate's player's queue
        ''' 
        player = Player.player_ids[id]
        player._command_queue.put(command)
        #this must be done in the non-threaded version
        #otherwise, the Character will never do anything
        player.poke()

    @classmethod
    def receive_messages(self):
        '''iterates over every player, yielding ids and messages
        note that this method is costly, and it might make 
        more since to make Player.message_queue containg these
        tuples
        '''
        for id, player in Player.player_ids.items():
            while player.has_msg():
                yield (id, player._message_queue.get())

    @classmethod
    def remove_player(self, id):
        '''Properly remove a player after disconnect'''
        player = Player.player_ids[id]
        try:
            # detach the player
            player.receiver.detach()
        except AttributeError:
            # self.character is most likely None
            pass
        del Player.player_ids[id]

            
#TODO: implement a system for creating nonplayers based on file
class Nonplayer:
    '''Nonplayer acts as a stream of incoming data
    '''
    pass