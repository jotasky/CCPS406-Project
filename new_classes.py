import json
from typing import Dict

with open("characters.json", "r") as file:
  allCharacters = json.load(file)

with open("rooms.json", "r") as file:
  allRooms = json.load(file)

class Character:
    def __init__(self, ID):
        self.ID = ID
        self.name = allCharacters[ID]["name"]
        self.classType = allCharacters[ID]["class"]
        self.health = allCharacters[ID]["health"]
        self.maxhealth = allCharacters[ID]["maxHealth"]
        self.attack = allCharacters[ID]["attack"]
        self.defense = allCharacters[ID]["defense"]
        self.evasion = allCharacters[ID]["evasion"]
        self.level = allCharacters[ID]["level"]
        self.inventory = allCharacters[ID]["inventory"]
        self.description = allCharacters[ID]["description"]
        self.curItem = allCharacters[ID]["curItem"]
        self.state = allCharacters[ID]["state"]
        self.location = allCharacters[ID]["location"]
        self.playable = allCharacters[ID]["playable"]
        self.locationObj = Room.registry[self.location]

    def move_to(self, direction, room_dict):
        # Check if room direction exists
        if(room_dict[self.location].verify_move(direction)):

    def interface(self, action):



class Room:
    def __init__(self, ID):
      self.ID = ID
      self.name = allRooms[ID]["name"]
      self.adjRooms = allRooms[ID]["adjRooms"]
      self.locked = allRooms[ID]["locked"]
      self.visited = allRooms[ID]["visited"]
      self.items = allRooms[ID]["items"]
      self.characters = allRooms[ID]["characters"]
      self.longDesc = allRooms[ID]["longDesc"]
      self.shortDesc = allRooms[ID]["shortDesc"]

    # Check whether room is accessible
    def verify_move(self, direction):
        if(self.adjRooms[direction] == "UNLOCKED"):
            return True
        else:
            return False

    # Delete char from room
    def char_del(self, char_ID):
        del self.characters[char_ID]
        del allRooms[self.ID]["characters"][char_ID]

    # Add char to a room
    def char_add(self, char_ID):
        self.characters[char_ID]