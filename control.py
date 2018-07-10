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

    def __str__(self):
        return "id: %s receiver: %s" % (self.id, self.receiver)

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

class Receiver(metaclass=ABCMeta):
    '''Abstract base class for implementing a Receiver
    self.controller refers to the object under control
    this is most frequently a Player
    
    a Receiver has three features.
    a detach method, used to remove completely from a controller
        (the controller should updated as well)
    an attach method, to begin listening to a controller()
        (the controller should be updated as well)
    an update method, which will be called periodically
        this method usually handles input from the controller
    '''
    def __init__(self):
        self.controller = None
    
    @abstractmethod
    def attach(self, controller):
        '''attach to [controller]'''
        pass
    
    @abstractmethod
    def detach(self):
        '''detach from controller'''
        pass

    @abstractmethod
    def update(self):
        '''periodically called function'''
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        '''overriding __subclasshook___, this affects isinstance() and issubclass()
        any Class implementing the 3 important methods is considered a subclass
        '''
        return all([hasattr(subclass, 'attach'), hasattr(subclass, 'detach'),
                    hasattr(subclass, 'update')])


class Monoreceiver:
    '''A simple receiver that implements the 3 methods in a direct fashion.
    Compare to a Multireceiver, which is constructed from multiple smaller receivers.
    '''

    def __init__(self):
        self.controller = None
   
    def attach(self, controller):
        '''attach to [controller] to begin listening for input'''
        if controller == self.controller:
            # controller is already attached
            # this also breaks a recursive loop that starts with Controller.assume_control
            return
        self.detach()
        # updating this receiver and the controller
        self.controller = controller
        self.controller.receiver = self
    
    def detach(self):
        '''sets controller to none, and removes any unnecessary functions'''
        if self.controller is not None:
            self.controller.receiver = None
        self.controller = None
    
    def update():
        '''must be implemented by subclasses'''
        pass

#TODO: for message history, keep track of the index and replace that way
# this prevents a lot of resizing, and makes the structure more threadsafe 
class Multireceiver(Monoreceiver):
    '''A conglomerate of multiple receivers, listening to one controller
    
    The Multireceiver acts as a giant Monoreceiver, working like so:
        attaching the Multireceiver to a controller attaches all 
    subreceivers to that controller
        detaching the Multireceiver detaches all subreceivers
        updating the Multireceiver updates all subreceivers

    The Multireceiver also has two traits:
    fragile [default: false]:
        If True, any subreceivers that are detached from their DummyController
        are removed from the lsit upon update()
    filter [default: false]:
        If True, repeated messages from different sources are filtered out
        For instance, if two characters are in the same location, the controller receive
        all dialogue twice. We can filter this out instead.

    Implementation note:
    Uses a set of DummyControllers, passing commands to each one
    Each subreceiver is set to listen to a corresponding DummyController
    This is suboptimal, more elegant solutions are welcomed.
    '''

    class DummyController(Controller):
        '''Straightforward implementation of Controller, intending to pass
        commands from the parent multireceiver to the subreceivers
        '''
        def __init__(self, multireceiver, receiver):
            self.multireceiver = multireceiver
            self.receiver = receiver
            self._command_queue = queue.Queue()
        
        def has_cmd(self):
            return not self._command_queue.empty()
        
        def has_msg(self):
            try: 
                self.multireceiver.controller.has_msg()
            except AttributeError:
                # controller is None
                pass

        def read_cmd(self):
            return self._command_queue.get()
        
        def add_cmd(self, cmd):
            self._command_queue.put(cmd)
        
        def write_msg(self, msg):
            self.multireceiver._message(self.receiver, msg)

    def __init__(self, *subreceivers, **kwargs):
        self.controller = None
        self.messages = queue.Queue()
        self._sub_dict = {}
        for sub in subreceivers:
            assert(isinstance(sub, Receiver))
            self._sub_dict[sub] = \
                self.DummyController(self, sub)
        self.msg_history = []
        self.msg_history_size = len(self._sub_dict) * 2
        self.filter ='filter' in kwargs and kwargs['filter']
        self.fragile = 'fragile' in kwargs and kwargs['fragile']

    def __iter__(self):
        '''overriding __iter__
        iterating over a Multireceiver yields the subreceivers
        '''
        for sub in self._sub_dict.keys():
            yield sub
    
    def attach(self, controller):
        '''attaches the Multireceiver, including all subreceivers'''
        # attach the controller to the multireceiver
        super().attach(controller)
        # attach each subreceiver to its DummyController
        for sub in self:
            self._sub_dict[sub].assume_control(sub)

    def detach(self):
        '''detaches the Multireceiver, including all subreceivers'''
        # detaching the controller to overall Multireceiver
        super().detach()
        # detaching each subreceiver to the overall Multireceiver
        for sub in self:
            sub.detach()

    def _check_detached(self):
        '''remove any subreceivers that have been attached to other controllers'''
        for sub, ctrl in dict(self._sub_dict).items():
            # detect if subreceiver has been attached to another controller
            if sub.controller != ctrl and sub.controller is not None:
                # send a message to the multireceiver, and remove from dictionary
                self.controller.write_msg("Lost connection wtih %s" % sub)
                del self._sub_dict[sub]
                self.outgoing_size = int(len(self._sub_dict) * 1.5)

    def _message(self, receiver, message):
        '''send a message to the controller of this multireceiver
        intended to be called by the DummyControllers
        '''
        # if filter is True, then we need to check the recent history
        if self.filter:
            # remove any old messages
            while len(self.msg_history) > self.msg_history_size:
                self.msg_history.pop(0)
            # if the same message has been recently sent by the
            for sub, msg in self.msg_history:
                if msg == message and sub != receiver:
                    return
            else:
                self.msg_history.append((receiver, message))
        
        if self.controller is not None:
            if (len(self.msg_history) == 0 or self.msg_history[-1][0] != receiver) \
                and self.filter:
                self.controller.write_msg("[%s]" % receiver)
            self.controller.write_msg(message)

    def update(self):
        '''update the Multireceiver, and all subreceivers'''
        if self.fragile:
            self._check_detached()
        # pass commands onto DummyControllers
        while self.controller.has_cmd():
            cmd = self.controller.read_cmd()
            for dummy in self._sub_dict.values():
                dummy.add_cmd(cmd)
        # update the subreceivers
        for sub in self:
            sub.update()