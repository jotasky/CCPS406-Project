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
        self.maxhealth = allCharacters[ID]["health"]
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
    def interface(self, message, location):
        print(message, location)
    def move_to(self, direction, room_dict):
        # Check if room direction exists and is UNLOCKED
        room_status = room_dict[self.location].verify_move(direction)
        if(room_status == "UNLOCKED"):
            # Add character to the room they are moving to
            room_dict[room_dict[self.location].get_adj_room(direction)].char_add(self.ID)
            # Delete character from the room they are moving from
            room_dict[self.location].char_del(self.ID)
            # Update character location variable
            self.location = room_dict[self.location].get_adj_room(direction)
            self.interface("Successfully moved to ", self.location)

            # Check if room has been visited before, if yes play short descr if not play long description
            if(room_dict[self.location].get_visited() == "false"):
                print(room_dict[self.location].get_long_desc()) # Later do printing through interface. I do not like printing character class
                room_dict[self.location].set_visited("true")    # Make all printing done from the get() functions. So it can be reused in the look() functionality
            else:                                               # Issue with not printing first room location. Do it in the main function
                print(room_dict[self.location].get_short_desc())



        elif(room_status == "LOCKED"):
            self.interface("Unforturnately room is locked. Currently residing in ", self.location)

        else:
            self.interface("Unfortunately that direction is inaccessible residing in ", self.location)





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
        if(self.adjRooms[direction] != "NULL"):
            return self.locked[direction]
        else:
            return "NULL"

    # Delete char from room
    def char_del(self, char_ID):
        del self.characters[char_ID]

    # Add char to a room
    def char_add(self, char_ID):
        self.characters[char_ID] = char_ID

    # Returns the room ID pointed to by the direction
    def get_adj_room(self, direction):
        return self.adjRooms[direction]

    def get_long_desc(self):
        return self.longDesc
    def get_short_desc(self):
        return self.shortDesc

    def get_visited(self):
        return self.visited

    def set_visited(self, value):
        self.visited = value

