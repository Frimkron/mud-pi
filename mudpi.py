#!/usr/bin/python2 

import socket
import select
import time
import os


class MudServer(object):

	class Client(object):
		
		socket = None
		address = ""
		buffer = ""
		lastcheck = 0
		name = None
		
		def __init__(self,socket,address,buffer,lastcheck):
			self.socket = socket
			self.address = address
			self.buffer = buffer
			self.lastcheck = lastcheck
			self.named = False
			
	EVENT_NEW_PLAYER = 1
	EVENT_PLAYER_LEFT = 2
	EVENT_COMMAND = 3
	
	READ_STATE_NORMAL = 1
	READ_STATE_COMMAND = 2
	READ_STATE_SUBNEG = 3
	
	TN_INTERPRET_AS_COMMAND = 255
	TN_ARE_YOU_THERE = 246
	TN_WILL = 251
	TN_WONT = 252
	TN_DO = 253
	TN_DONT = 254
	TN_SUBNEGOTIATION_START = 250
	TN_SUBNEGOTIATION_END = 240

	listen_socket = None
	clients = {}
	nextid = 0
	events = []

	def __init__(self):
		self.clients = {}
		self.nextid = 0
		self.events = []
		self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
		self.listen_socket.bind(("0.0.0.0",23))
		self.listen_socket.setblocking(False)
		self.listen_socket.listen(1)

	def update(self):
		self.events = []
		self._check_for_new_connections()
		self._check_for_disconnected()
		self._check_for_messages()
		
	def get_new_players(self):
		retval = []
		for ev in self.events:
			if ev[0] == self.EVENT_NEW_PLAYER: retval.append((ev[1],ev[2]))
		return retval
		
	def get_disconnected_players(self):
		retval = []
		for ev in self.events:
			if ev[0] == self.EVENT_PLAYER_LEFT: retval.append(ev[1])
		return retval
	
	def get_commands(self):
		retval = []
		for ev in self.events:
			if ev[0] == self.EVENT_COMMAND: retval.append((ev[1],ev[2],ev[3]))
		return retval

	def send_message(self,to,message):
		self._attempt_send(to,message+"\n")
		
	def shutdown(self):
		for cl in self.clients.values():
			cl.socket.shutdown()
			cl.socket.close()
		self.listen_socket.close()
	
	def _attempt_send(self,clid,data):
		try:
			self.clients[clid].socket.sendall(data)
		except KeyError: pass
		except socket.error:
			self._handle_disconnect(clid)
	
	def _check_for_new_connections(self):
		rlist,wlist,xlist = select.select([self.listen_socket],[],[],0)
		if self.listen_socket not in rlist: return
		joined_socket,addr = self.listen_socket.accept()	
		joined_socket.setblocking(False)
		self.clients[self.nextid] = MudServer.Client(joined_socket,addr[0],"",time.time())
		self._attempt_send(self.nextid,"What is your name?\n")
		self.nextid += 1		

	def _check_for_disconnected(self):
		for id,cl in self.clients.items():
			if time.time() - cl.lastcheck < 5.0: continue
			self._attempt_send(id,""+chr(self.TN_INTERPRET_AS_COMMAND)+chr(self.TN_ARE_YOU_THERE))
			cl.lastcheck = time.time()
				
	def _check_for_messages(self):
		for id,cl in self.clients.items():
			rlist,wlist,xlist = select.select([cl.socket],[],[],0)
			if cl.socket not in rlist: continue
			try:
				data = cl.socket.recv(4096)
				message = self._process_sent_data(cl,data)
				if message:
					message = message.strip()
					if not cl.named:
						self.events.append((self.EVENT_NEW_PLAYER,id,message))
						cl.named = True
					else:
						command,params = (message.split(" ",1)+["",""])[:2]
						self.events.append((self.EVENT_COMMAND,id,command.lower(),params))
			except socket.error:
				self._handle_disconnect(id)
				
	def _handle_disconnect(self,clid):
		del(self.clients[clid])
		self.events.append((self.EVENT_PLAYER_LEFT,clid))
				
	def _process_sent_data(self,client,data):
		message = None
		state = self.READ_STATE_NORMAL
		for c in data:
			if state == self.READ_STATE_NORMAL:
				if ord(c) == self.TN_INTERPRET_AS_COMMAND:
					state = self.READ_STATE_COMMAND
				elif c == "\n":
					message = client.buffer
					client.buffer = ""
				else:
					client.buffer += c
					
			elif state == self.READ_STATE_COMMAND:
				if ord(c) == self.TN_SUBNEGOTIATION_START:
					state = self.READ_STATE_SUBNEG
				elif ord(c) in (self.TN_WILL,self.TN_WONT,self.TN_DO,self.TN_DONT):
					state = self.READ_STATE_COMMAND
				else:
					state = self.READ_STATE_NORMAL
					
			elif state == self.READ_STATE_SUBNEG:
				if ord(c) == self.TN_SUBNEGOTIATION_END:
					state = self.READ_STATE_NORMAL					
		return message
						

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
mud = MudServer()
players = {}
while True:

	mud.update()
	
	for id,command,params in mud.get_commands():
		if id not in players: continue
	
		if command == "help":
			mud.send_message(id,"Commands:")
			mud.send_message(id,"  say <message>  - Says something out loud")
			mud.send_message(id,"  look           - Examines the surroundings")
			mud.send_message(id,"  go <exit>      - Moves through the exit specified")
			
		elif command == "say":
			data = "%s says: %s" % (players[id]["name"],params) 
			os.system('espeak -v english_wmids "%s"' % data)
			for pid,pl in players.items():
				if players[pid]["room"] == players[id]["room"]:
					mud.send_message(pid,data)
				
		elif command == "look":
			rm = rooms[players[id]["room"]]
			mud.send_message(id, rm["description"])
			mud.send_message(id, "Players here: %s" % ", ".join(playershere))
			mud.send_message(id, "Exits are: %s" % ", ".join(rm["exits"]))
			playershere = []
			for pid,pl in players.items():
				if players[pid]["room"] == players[id]["room"]:
					playershere.append(players[pid]["name"])
			
		elif command == "go":
			ex = params.lower()
			rm = rooms[players[id]["room"]]
			if ex in rm["exits"]:
				for pid,pl in players.items():
					if players[pid]["room"] == players[id]["room"] and pid!=id:
						mud.send_message(pid,"%s left via exit '%s'" % (players[id]["name"],ex))
				players[id]["room"] = rm["exits"][ex]
				rm = rooms[players[id]["room"]]
				for pid,pl in players.items():
					if players[pid]["room"] == players[id]["room"] and pid!=id:
						mud.send_message(pid,"%s arrived via exit '%s'" % (players[id]["name"],ex))
				mud.send_message(id,"You arrive at '%s'" % players[id]["room"])
			else:
				mud.send_message(id, "Unknown exit '%s'" % ex)
				
		else:
			mud.send_message(id, "Unknown command '%s'" % command)
	
	for id in mud.get_disconnected_players():
		if id not in players: continue
		for pid,pl in players.items():
			mud.send_message(pid,"%s quit the game" % players[id]["name"])
		del(players[id])
		
	for id,name in mud.get_new_players():
		players[id] = { 
			"name": name ,
			"room": "Tavern",
		}
		for pid,pl in players.items():
			mud.send_message(pid,"%s entered the game" % players[id]["name"])
		mud.send_message(id,"Welcome to the game, %s. Have fun!" % players[id]["name"])
		mud.send_message(id,rooms[players[id]["room"]]["description"])
		
mud.shutdown()
		
