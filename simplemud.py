"""    
A simple Multi-User Dungeon (MUD) game. Players can talk to each other, examine
their surroundings and move between rooms.

Some ideas for things to try adding:
    * More rooms to explore
    * An 'emote' command e.g. 'emote laughs out loud' -> 'Mark laughs out loud'
    * A 'whisper' command for talking to individual players
    * A 'shout' command for yelling to players in all rooms
    * Items to look at in rooms e.g. 'look fireplace' -> 'You see a roaring, glowing fire'
    * Items to pick up e.g. 'take rock' -> 'You pick up the rock'
    * Monsters to fight
    * Loot to collect
    * Saving players accounts between sessions
    * A password login
    * A shop from which to buy items

author: Mark Frimston - mfrimston@gmail.com
"""

import logging

# import the MUD server class
from mudserver import MudServer

# structure defining the rooms in the game. Try adding more rooms to the game!
rooms = {
    "Tavern": {
        "description": "You're in a cozy tavern warmed by an open fire.",
        "exits": { "outside": "Outside" },
    },
    "Outside": {
        "description": "You're standing outside a tavern. It's raining.",
        "exits": { "inside": "Tavern" },
    }
}

# stores the players in the game
players = {}

# set up logging to file
logging.basicConfig(filename="mud.log",level=logging.INFO,format="[%(levelname)s] %(message)s")

# start the server
mud = MudServer()

# main game loop. We loop forever (i.e. until the program is terminated)
while True:


    # 'update' must be called in the loop to keep the game running and give
    # us up-to-date information
    mud.update()
    
    
    # go through any newly connected players
    for id in mud.get_new_players():
    
        # add the new player to the dictionary, noting that they've not been
        # named yet.
        # The dictionary key is the player's id number. Start them off in the 
        # 'Tavern' room.
        # Try adding more player stats - level, gold, inventory, etc
        players[id] = { 
            "name": None,
            "room": "Tavern",
        }
        
        # send the new player a prompt for their name
        mud.send_message(id,"What is your name?")
        
    
    # go through any recently disconnected players    
    for id in mud.get_disconnected_players():
    
        # if for any reason the player isn't in the player map, skip them and 
        # move on to the next one
        if id not in players: continue
        
        # go through all the players in the game
        for pid,pl in players.items():
            # send each player a message to tell them about the diconnected player
            mud.send_message(pid,"%s quit the game" % players[id]["name"])
            
        # remove the player's entry in the player dictionary
        del(players[id])
    
    
    # go through any new commands sent from players
    for id,command,params in mud.get_commands():
    
        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players: continue
    
        # if the player hasn't given their name yet, use this first command as their name
        if players[id]["name"] is None:
            
            players[id]["name"] = command
            
            # go through all the players in the game
            for pid,pl in players.items():
                # send each player a message to tell them about the new player
                mud.send_message(pid,"%s entered the game" % players[id]["name"])
            
            # send the new player a welcome message
            mud.send_message(id,"Welcome to the game, %s. Type 'help' for a list of commands. Have fun!" % players[id]["name"])
            
            # send the new player the description of their current room
            mud.send_message(id,rooms[players[id]["room"]]["description"])
                
        # each of the possible commands is handled below. Try adding new commands
        # to the game!
    
        # 'help' command
        elif command == "help":
        
            # send the player back the list of possible commands
            mud.send_message(id,"Commands:")
            mud.send_message(id,"  say <message>  - Says something out loud, e.g. 'say Hello'")
            mud.send_message(id,"  look           - Examines the surroundings, e.g. 'look'")
            mud.send_message(id,"  go <exit>      - Moves through the exit specified, e.g. 'go outside'")
            
        # 'say' command
        elif command == "say":
            
            # go through every player in the game
            for pid,pl in players.items():
                # if they're in the same room as the player
                if players[pid]["room"] == players[id]["room"]:
                    # send them a message telling them what the player said
                    message = "%s says: %s" % (players[id]["name"],params)
                    mud.send_message(pid,message)
                    # log the message
                    logging.info(message)
                    
        # 'look' command
        elif command == "look":
        
            # store the player's current room
            rm = rooms[players[id]["room"]]
            
            # send the player back the description of their current room
            mud.send_message(id, rm["description"])
            
            playershere = []
            # go through every player in the game
            for pid,pl in players.items():
                # if they're in the same room as the player
                if players[pid]["room"] == players[id]["room"]:
                    # add their name to the list
                    playershere.append(players[pid]["name"])
                    
            # send player a message containing the list of players in the room
            mud.send_message(id, "Players here: %s" % ", ".join(playershere))
            
            # send player a message containing the list of exits from this room
            mud.send_message(id, "Exits are: %s" % ", ".join(rm["exits"]))
                        
        # 'go' command
        elif command == "go":
            
            # store the exit name
            ex = params.lower()
            
            # store the player's current room
            rm = rooms[players[id]["room"]]
            
            # if the specified exit is found in the room's exits list
            if ex in rm["exits"]:
            
                # go through all the players in the game
                for pid,pl in players.items():
                    # if player is in the same room and isn't the player sending the command
                    if players[pid]["room"] == players[id]["room"] and pid!=id:
                        # send them a message telling them that the player left the room
                        mud.send_message(pid,"%s left via exit '%s'" % (players[id]["name"],ex))
                        
                # update the player's current room to the one the exit leads to
                players[id]["room"] = rm["exits"][ex]
                rm = rooms[players[id]["room"]]
                
                # go through all the players in the game
                for pid,pl in players.items():
                    # if player is in the same (new) room and isn't the player sending the command
                    if players[pid]["room"] == players[id]["room"] and pid!=id:
                        # send them a message telling them that the player entered the room
                        mud.send_message(pid,"%s arrived via exit '%s'" % (players[id]["name"],ex))
                        
                # send the player a message telling them where they are now
                mud.send_message(id,"You arrive at '%s'" % players[id]["room"])
                
            # the specified exit wasn't found in the current room
            else:
                # send back an 'unknown exit' message
                mud.send_message(id, "Unknown exit '%s'" % ex)
                
        # some other, unrecognised command
        else:
            # send back an 'unknown command' message
            mud.send_message(id, "Unknown command '%s'" % command)
                
