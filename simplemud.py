#!/usr/bin/env python
import time
import sys
import logging
import threading
import queue
import enum
# import the MUD server class
from mudserver import MudServer, Event, EventType

# Setup the logger
logging.basicConfig(format='%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("muddyswamp.log"),
        logging.StreamHandler(sys.stdout)
    ])

#prints to stderr
def err_print(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

VERBOSE_PRINT = False
def v_print(*args, **kwargs):
	if VERBOSE_PRINT:
		err_print(*args, **kwargs)

# Basic enum for the type of server command
class ServerCommandEnum(enum.Enum):
    BROADCAST_MESSAGE=0
    GET_PLAYERS=1

# Simple wrapper class for a server-side command
class ServerComand:
    def __init__(self, command_type, params):
        self.command_type = command_type
        self.params = params

# structure defining the rooms in the game. Try adding more rooms to the game!
rooms = {
    "Tavern": {
        "description": "You're in a cozy tavern warmed by an open fire.",
        "exits": {"outside": "Outside"},
    },
    "Outside": {
        "description": "You're standing outside a tavern. It's raining.",
        "exits": {"inside": "Tavern"},
    }
}

class MudServerWorker(threading.Thread):
    def __init__(self, q, *args, **kwargs):
        self.q = q
        self.players = {}
        self.keep_running = True
        super().__init__(*args, **kwargs)
    
    # Cannot call mud.shutdown() here because it will try to call the sockets in run on the final go through
    def shutdown(self):
        self.keep_running = False
    
    def run(self):
        logging.info("Starting server.")
        self.mud = MudServer()
        logging.info("Server started successfully.")
        # main game loop. We loop forever (i.e. until the program is terminated)
        while self.keep_running:

            # pause for 1/5 of a second on each loop, so that we don't constantly
            # use 100% CPU time
            time.sleep(0.2)

            try:
                server_command = self.q.get(block=False)
                if server_command is not None:
                    if server_command.command_type == ServerCommandEnum.BROADCAST_MESSAGE:
                        self.mud.send_message_to_all(server_command.params)
                    elif server_command.command_type == ServerCommandEnum.GET_PLAYERS:
                        logging.info("Players: ")
                        for pid, pl in self.players.items():
                            logging.info("{}:{}".format(pid, pl))

            except Exception:
                pass

            # 'update' must be called in the loop to keep the game running and give
            # us up-to-date information
            self.mud.update()

            # handle events on the server_queue
            while (len(self.mud.server_queue) > 0):
                event = self.mud.server_queue.popleft()
                logging.info(event)

                id = event.id
                if event.type is EventType.PLAYER_JOIN:
                    # add the new player to the dictionary, noting that they've not been
                    # named yet.
                    # The dictionary key is the player's id number. We set their room to
                    # None initially until they have entered a name
                    logging.info("Player %s joined." % event.id)
                    self.players[id] = {
                        "name": None,
                        "room": None,
                    }
                    #prompt the user for their name
                    self.mud.send_message(id, "What is your name?")
                elif event.type is EventType.MESSAGE_RECEIVED:
                    # splitting into command + params to make porting the code easier
                    command, params = (event.message.split(" ", 1) + ["", ""])[:2]
                    logging.debug("Event message: " + event.message)
                    # all these elifs will be replaced with "character.parse([input])"
                    if self.players[id]["name"] is None:
                        self.players[id]["name"] = event.message.split(" ")[0]
                        self.players[id]["room"] = "Tavern"
                        # send each player a message to tell them about the new player
                        self.mud.send_message_to_all("%s entered the game" % self.players[id]["name"])
                        self.mud.send_message(id, "Welcome to the game, %s. " %
                                                                self.players[id]["name"]
                                    + "Type 'help' for a list of commands. Have fun!")
                    # 'help' command
                    elif command == "help":

                        # send the player back the list of possible commands
                        self.mud.send_message(id, "Commands:")
                        self.mud.send_message(id, "  say <message>  - Says something out loud, "
                                            + "e.g. 'say Hello'")
                        self.mud.send_message(id, "  look           - Examines the "
                                            + "surroundings, e.g. 'look'")
                        self.mud.send_message(id, "  go <exit>      - Moves through the exit "
                                            + "specified, e.g. 'go outside'")

                    # 'say' command
                    elif command == "say":

                        # go through every player in the game
                        for pid, pl in self.players.items():
                            # if they're in the same room as the player
                            if self.players[pid]["room"] == self.players[id]["room"]:
                                # send them a message telling them what the player said
                                self.mud.send_message(pid, "{} says: {}".format(
                                                            self.players[id]["name"], params))

                    # 'look' command
                    elif command == "look":

                        # store the player's current room
                        rm = rooms[self.players[id]["room"]]

                        # send the player back the description of their current room
                        self.mud.send_message(id, rm["description"])

                        playershere = []
                        # go through every player in the game
                        for pid, pl in self.players.items():
                            # if they're in the same room as the player
                            if self.players[pid]["room"] == self.players[id]["room"]:
                                # ... and they have a name to be shown
                                if self.players[pid]["name"] is not None:
                                    # add their name to the list
                                    playershere.append(self.players[pid]["name"])

                        # send player a message containing the list of players in the room
                        self.mud.send_message(id, "Players here: {}".format(
                                                                ", ".join(playershere)))

                        # send player a message containing the list of exits from this room
                        self.mud.send_message(id, "Exits are: {}".format(
                                                                ", ".join(rm["exits"])))

                    # 'go' command
                    elif command == "go":

                        # store the exit name
                        ex = params.lower()

                        # store the player's current room
                        rm = rooms[self.players[id]["room"]]

                        # if the specified exit is found in the room's exits list
                        if ex in rm["exits"]:

                            # go through all the players in the game
                            for pid, pl in self.players.items():
                                # if player is in the same room and isn't the player
                                # sending the command
                                if self.players[pid]["room"] == self.players[id]["room"] \
                                        and pid != id:
                                    # send them a message telling them that the player
                                    # left the room
                                    self.mud.send_message(pid, "{} left via exit '{}'".format(
                                                                self.players[id]["name"], ex))

                            # update the player's current room to the one the exit leads to
                            self.players[id]["room"] = rm["exits"][ex]
                            rm = rooms[self.players[id]["room"]]

                            # go through all the players in the game
                            for pid, pl in self.players.items():
                                # if player is in the same (new) room and isn't the player
                                # sending the command
                                if self.players[pid]["room"] == self.players[id]["room"] \
                                        and pid != id:
                                    # send them a message telling them that the player
                                    # entered the room
                                    self.mud.send_message(pid,
                                                    "{} arrived via exit '{}'".format(
                                                                self.players[id]["name"], ex))

                            # send the player a message telling them where they are now
                            self.mud.send_message(id, "You arrive at '{}'".format(
                                                                    self.players[id]["room"]))

                        # the specified exit wasn't found in the current room
                        else:
                            # send back an 'unknown exit' message
                            self.mud.send_message(id, "Unknown exit '{}'".format(ex))

                    # some other, unrecognised command
                    else:
                        # send back an 'unknown command' message
                        self.mud.send_message(id, "Unknown command '{}'".format(command))


                elif event.type is EventType.PLAYER_DISCONNECT:
                    logging.info("Player %s left" % event.id)
                    #if the player has been added to the list, they must be removed
                    if event.id in self.players:
                        self.mud.send_message_to_all("%s quit the game" % self.players[event.id]["name"])
                        del(self.players[id])
        # Shut down the mud instance after the while loop finishes
        self.mud.shutdown()

# Create a threadsafe queue for commands entered on the server side
q = queue.Queue()
# Create an instance of the thread and start it
thread = MudServerWorker(q)
thread.setName("MudServerThread")
thread.start()

# Look for input on the server and send it to the thread
while True:
    try:
        command, params = (input("").split(" ", 1) + ["", ""])[:2]
        if command == "broadcast":
            q.put(ServerComand(ServerCommandEnum.BROADCAST_MESSAGE, u"\u001b[32m" + "[Server] " + params + u"\u001b[0m"))
        elif command == "players":
            q.put(ServerComand(ServerCommandEnum.GET_PLAYERS, ""))
        elif command == "stop":
            q.put(ServerComand(ServerCommandEnum.BROADCAST_MESSAGE, u"\u001b[32m" + "[Server] " + "Server shutting down..." + u"\u001b[0m"))
            break
        elif command == "help":
            logging.info("Server commands are: \n" \
            " broadcast [message] - Broadcasts a message to the entire server\n"\
            " players - Prints a list of all players\n" \
            " stop - Stops the server")
        else:
            logging.info("Command not recognized. Type help for a list of commands.")
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt detected. Shutting down.")
        q.put(ServerComand(ServerCommandEnum.BROADCAST_MESSAGE, u"\u001b[32m" + "[Server] " + "Server shutting down..." + u"\u001b[0m"))
        break


# Shut down the server gracefully
logging.info("Shutting down server")
thread.shutdown()
thread.join()
logging.info("Server shutdown. Good bye!!")