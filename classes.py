import json
import random
from typing import Dict

CHAR_STATES = ["normal", "enraged"]


with open("characters.json", "r") as file:
  allCharacters = json.load(file)

with open("dialogue.json", "r") as file:
  allDialogue = json.load(file)

with open("items.json", "r") as file:
  allItems = json.load(file)

with open("rooms.json", "r") as file:
  allRooms = json.load(file)

with open("turnCounter.json", "r") as file:
  turnCounter_data = json.load(file) 


# def equip(self, item: Item):
#   for item in self.inventory:
#     if item.name.lower() == item_name.lower():
#       print(f"Equipped {item.name}.")
#       return item
#   print(f"You do not have {item_name} in your inventory.")
#   return None

# def unequip(self, item_name):
#       print(f"Unequipped {item.name}.")

class Character:
  registry = {}
  names = {}

  def __init__(self, ID):
    self.registry[ID] = self
    self.ID = ID
    self.name = allCharacters[ID]["name"]
    self.names[self.name.upper()] = self.ID
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
    self.locationObj = Room.registry[self.location] #initializing object location

  def moveTo(self, direction):
    nextRoom = self.locationObj.adjRooms[direction]
    if nextRoom == "NULL":
      print("You cannot move that way.")
      return
    nextLocationObj = Room.registry[nextRoom]
    self.locationObj.characters.remove(self.ID)
    self.locationObj = nextLocationObj
    self.location = nextRoom
    self.locationObj.characters.append(self.ID)
    print("You have entered: " + self.locationObj.name)

    if not self.locationObj.visited:
      print(self.locationObj.longDesc)
      self.locationObj.playerVisited = True
    else:
      print(self.locationObj.shortDesc)

  def attack(self, attacker, target):
    damage = attacker.attack - target.defense
    if damage > 0:
      target.updateHealth(-damage)
    print(f"{attacker.name} attacks {target.name} for {damage} damage!")
    
  def get_inventroy(self):
    return self.inventory

  def pickUp(self, item):
    if item.ID in self.locationObj.items:
      self.locationObj.items.remove(item.ID)
      self.inventory.append(item.ID)
      print("You have picked up: " + item)
    else:
      print("There is no " + item + " here.")
      return

  def updateHealth(self, amount):
    self.health += amount
    if self.health < 0:
      self.health = 0
    if self.health > self.maxhealth:
      self.health = self.maxhealth

  def equip(self, item):
    if self.curItem == item.ID:
      print("You already have that equipped.")
      return
    if item.ID in self.inventory:
      self.curItem = item.ID
      print("You have equipped: " + item)
    else:
      print("You do not have that item.")
      return
  def inspect(self, item):
    print(item.desc)

  def enrage(self):
    self.state["enraged"] = True
    self.attack *= 2
    self.defense *= 0.75
    self.health = self.maxhealth
    print(self.state["enraged"])

  def look(self):
    print(self.locationObj.shortDesc)
    # for item in self.locationObj.items:
    #   print(item)
    # for char in self.locationObj.characters:
    #   print(char)
  
  def show_inventroy(self):
    for item in self.inventory:
      print(item)

  def consume(self, item_name):
    for item in self.inventory:
      if (item.name.lower() == item_name.lower()) and item.type == 'health':
        self.health = min(self.maxhealth, self.health + item.health)
        self.inventory.remove(item)
        print(f"Consumed {item.name}, health is now {self.health}.")
        # return True
      else:
        print(f"You do not have {item_name} in your inventory.")
        return

  def __str__(self):
    return f"{self.name} ({self.description})"

class Item:
    registry = {}
    names = {}

    def __init__(self, ID):
      self.registry[ID] = self
      self.ID = ID
      self.name = allItems[ID]["name"]
      self.names[self.name.upper()] = self.ID
      self.type = allItems[ID]["type"]
      self.health = allItems[ID]["health"]
      self.damage = allItems[ID]["damage"]
      self.defense = allItems[ID]["defense"]
      self.evasion = allItems[ID]["evasion"]
      self.desc = allItems[ID]["desc"]

class Room:
    registry = {}
    names = {}

    def __init__(self, ID):
      self.registry[ID] = self
      self.ID = ID
      self.name = allRooms[ID]["name"]
      self.names[self.name.upper()] = self.ID

      self.adjRooms = allRooms[ID]["adjRooms"]
      self.locked = allRooms[ID]["locked"]
      self.visited = allRooms[ID]["visited"]
      self.items = allRooms[ID]["items"]
      self.characters = allRooms[ID]["characters"]
      self.longDesc = allRooms[ID]["longDesc"]
      self.shortDesc = allRooms[ID]["shortDesc"]

    def connect_room(self, direction: str, room: 'Room'):
      self.adjRooms[direction] = room

    def add_item(self, item: Item):   
      self.items.append(item)

    def remove_item(self, item: Item):
      self.items.remove(item)

    def add_character(self, character: 'Character'):
      self.characters.append(character)

    def remove_character(self, item: Item):
      self.items.remove(item)

class Model:
  def __init__(self,json_files: Dict[str, str]):
      self.json_files = json_files
      self.turn_counter = turnCounter_data["turnCounter"]
      self.player = Character.registry["c1_player"]
      self.enemies = [Character.registry[char_id] 
                      for char_id in Character.registry if char_id != "c1_player"]
      self.rooms= Room.registry
      self.items = Item.registry
      self.characters = Character.registry
      self.dialogue = allDialogue
      self.current_dialogue = self.dialogue["intro"]
      self.current_dialogue_index = 0
      self.current_dialogue_line = 0
      self.current_dialogue_line_index = 0
      self.current_dialogue_line_length = len(self.current_dialogue)
      self.current_dialogue_line_text = self.dialogue[self.current_dialogue_index]
      self.current_dialogue_line_text_index = 0
      self.current_dialogue_line_text_length = len(self.current_dialogue_line_text)
      self.current_dialogue_line_text_char = self.current_dialogue_line_text

  def load_data(self):
    for room_id in allRooms:
      Room(room_id)
    for item_id in allItems:
      Item(item_id)
    for char_id in allCharacters:
      Character(char_id)  

  def save_data(self):
    with open(self.json_files["turnCounter"], "w") as file:
      json.dump(turnCounter_data, file, indent= 4)


  def get_player(self):
    return self.player

  def get_enemies(self):
    for enemy in self.enemies:
      if enemy.playable:
        return enemy
    return None

class Controller:
  def __init__(self, model: Model, view: View):
    self.model = model
    self.view = view
    self.parser = Parser
    # key and method pairs to handle user input commands
    
    player = Character("c1_player")
    
    self.commands = {
      "look" : player.look,
      "go": self.handle_go,
      "attack": self.handle_attack,
      "grab": self.handle_grab,
      "inventory": self.handle_inventory,
      "equip": self.handle_equip,
      "enrage": self.handle_enrage,
      "inspect": self.handle_inspect,
      "move": self.handle_move,
    }
    
  def start_game(self):
    self.view.display_message("Welcome to the game!")
    current_room = self.model.get_player_position()
    room_description = self.model.get_room_description(current_room)
    self.view.display_message("Good luck!")
    self.view.display_room_description(room_description)
    self.view.display_message("Type 'quit' or 'exit' to end the game.")

    while True:
      command = self.view.get_user_input()
      if command in ["exit", "quit"]:
        break
      self.handle_command(command)
      
  def handle_command(self, command: str):
    action, target = self.parser.parse_command(command) 
    if action in self.commands:
      self.commands[action](target)
    else:
      self.view.display_message("Invalid command. Please try again.")

  def handle_look(self, _):
    current_room = self.model.get_player_position()
    room_description = self.model.get_room_description(current_room)
    self.view.display_room_description(room_description)

  def handle_go(self, direction: str):
    if direction:
      self.Character.moveTo(direction)
    else:
      self.view.display_message("Please specify a direction.")

  def handle_attack(self, _):
    player = self.model.get_player()
    target = self.model.get_enemies()
    if target:
      self.model.attack(player, target)
    else:
      self.view.display_message("There are no enemies in this room.")
    
class Parser:
  def __init__(self, command: str):
    self.command = command

  def parse_command(self, command: str) -> tuple:
    action, target = command.split(" ", 1)
    return action, target

