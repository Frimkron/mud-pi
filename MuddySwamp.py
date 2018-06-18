#!/usr/bin/env python
import time
import sys
import logging
# import the MUD server class
from mudserver import MudServer, Event, EventType

# Setup the logger
logging.basicConfig(format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s',
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

# stores the players in the game
players = {}

logging.info("Starting server")

# start the server
mud = MudServer()

logging.info("Server started successfully")

# main game loop. We loop forever (i.e. until the program is terminated)
while True:

    # pause for 1/5 of a second on each loop, so that we don't constantly
    # use 100% CPU time
    time.sleep(0.2)

    # 'update' must be called in the loop to keep the game running and give
    # us up-to-date information
    mud.update()

    # handle events on the server_queue
    while (len(mud.server_queue) > 0):
        event = mud.server_queue.popleft()
        logging.info(event)

        id = event.id
        if event.type is EventType.PLAYER_JOIN:
            # add the new player to the dictionary, noting that they've not been
            # named yet.
            # The dictionary key is the player's id number. We set their room to
            # None initially until they have entered a name
            logging.info("Player %s joined." % event.id)
            players[id] = {
                "name": None,
                "room": None,
            }
            #prompt the user for their name
            mud.send_message(id, "What is your name?")
        elif event.type is EventType.MESSAGE_RECEIVED:
            # splitting into command + params to make porting the code easier
            command, params = (event.message.split(" ", 1) + ["", ""])[:2]
            logging.debug("Event message: " + event.message)
            # all these elifs will be replaced with "character.parse([input])"
            if players[id]["name"] is None:
                players[id]["name"] = event.message.split(" ")[0]
                players[id]["room"] = "Tavern"
                # send each player a message to tell them about the new player
                mud.send_message_to_all("%s entered the game" % players[id]["name"])
                mud.send_message(id, "Welcome to the game, %s. " %
                                                           players[id]["name"]
                             + "Type 'help' for a list of commands. Have fun!")
            # 'help' command
            elif command == "help":

                # send the player back the list of possible commands
                mud.send_message(id, "Commands:")
                mud.send_message(id, "  say <message>  - Says something out loud, "
                                    + "e.g. 'say Hello'")
                mud.send_message(id, "  look           - Examines the "
                                    + "surroundings, e.g. 'look'")
                mud.send_message(id, "  go <exit>      - Moves through the exit "
                                    + "specified, e.g. 'go outside'")

            # 'say' command
            elif command == "say":

                # go through every player in the game
                for pid, pl in players.items():
                    # if they're in the same room as the player
                    if players[pid]["room"] == players[id]["room"]:
                        # send them a message telling them what the player said
                        mud.send_message(pid, "{} says: {}".format(
                                                    players[id]["name"], params))

            # 'look' command
            elif command == "look":

                # store the player's current room
                rm = rooms[players[id]["room"]]

                # send the player back the description of their current room
                mud.send_message(id, rm["description"])

                playershere = []
                # go through every player in the game
                for pid, pl in players.items():
                    # if they're in the same room as the player
                    if players[pid]["room"] == players[id]["room"]:
                        # ... and they have a name to be shown
                        if players[pid]["name"] is not None:
                            # add their name to the list
                            playershere.append(players[pid]["name"])

                # send player a message containing the list of players in the room
                mud.send_message(id, "Players here: {}".format(
                                                        ", ".join(playershere)))

                # send player a message containing the list of exits from this room
                mud.send_message(id, "Exits are: {}".format(
                                                        ", ".join(rm["exits"])))

            # 'go' command
            elif command == "go":

                # store the exit name
                ex = params.lower()

                # store the player's current room
                rm = rooms[players[id]["room"]]

                # if the specified exit is found in the room's exits list
                if ex in rm["exits"]:

                    # go through all the players in the game
                    for pid, pl in players.items():
                        # if player is in the same room and isn't the player
                        # sending the command
                        if players[pid]["room"] == players[id]["room"] \
                                and pid != id:
                            # send them a message telling them that the player
                            # left the room
                            mud.send_message(pid, "{} left via exit '{}'".format(
                                                        players[id]["name"], ex))

                    # update the player's current room to the one the exit leads to
                    players[id]["room"] = rm["exits"][ex]
                    rm = rooms[players[id]["room"]]

                    # go through all the players in the game
                    for pid, pl in players.items():
                        # if player is in the same (new) room and isn't the player
                        # sending the command
                        if players[pid]["room"] == players[id]["room"] \
                                and pid != id:
                            # send them a message telling them that the player
                            # entered the room
                            mud.send_message(pid,
                                            "{} arrived via exit '{}'".format(
                                                        players[id]["name"], ex))

                    # send the player a message telling them where they are now
                    mud.send_message(id, "You arrive at '{}'".format(
                                                            players[id]["room"]))

                # the specified exit wasn't found in the current room
                else:
                    # send back an 'unknown exit' message
                    mud.send_message(id, "Unknown exit '{}'".format(ex))

            # some other, unrecognised command
            else:
                # send back an 'unknown command' message
                mud.send_message(id, "Unknown command '{}'".format(command))


        elif event.type is EventType.PLAYER_DISCONNECT:
            logging.info("Player %s left" % event.id)
            #if the player has been added to the list, they must be removed
            if event.id in players:
                mud.send_message_to_all("%s quit the game" % players[event.id]["name"])
                del(players[id])