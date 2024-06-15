import json
from typing import Dict
import random

random.seed(1)

with open("characters.json", "r") as file:
    allCharacters = json.load(file)

with open("rooms.json", "r") as file:
    allRooms = json.load(file)

with open("items.json", "r") as file:
    allItems = json.load(file)


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
        self.state = "normal"
        self.location = allCharacters[ID]["location"]
        self.playable = allCharacters[ID]["playable"]
        self.aggro = allCharacters[ID]["aggro"]
        self.recent_move = allCharacters[ID]["recent_move"]
        self.dead = allCharacters[ID]["dead"]

    def inspect(self):
        # Shows the character's stats
        print(self.description)
        print(f"{self.health} / {self.maxhealth}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Evasion: {self.evasion}")
        print(f"State: {self.state}")
        if(self.curItem != ""):
            print("Holding: " + allItems[self.curItem]["name"])
        else:
            print("Holding: None")
        print(allRooms[self.location]["name"])

    def look(self, room_dict):
        # Provides room description
        print(room_dict[self.location].name)
        print(room_dict[self.location].shortDesc)
        for item in room_dict[self.location].items:
            print((allItems[item]["name"]))

    def getInventory(self):
        # Prints player inventory
        print(self.name + "'s inventory", self.inventory)

    def grab(self, item, room_dict):
        # Check if item exists in room
        if item in room_dict[self.location].items:
            for i in range(len(room_dict[self.location].items)):
                # Remove item from room
                if room_dict[self.location].items[i] == item:
                    room_dict[self.location].items.pop(i)
                    break
            # Add item to player inventory
            self.inventory.append(item)
            self.updateStats(item)
            print(self.name, "has picked up", allItems[item]["name"], "\n"+
                  allItems[item]["desc"])
        # Message in case item doesn't exist in room
        else:
            print("There is no such item here")
            return

    def equip(self, item):
        # Checks if item is already equipped
        if self.curItem == item:
            print("You are already have this item equipped")
            return
        # Checks if the item is a weapon, if weapon then it is equipped
        itemtype = allItems[item]["type"]
        if item in self.inventory and itemtype == "weapon":
            prevItem = "i00_blank"
            if self.curItem != "":
                prevItem = self.curItem

            self.curItem = item
            self.updateAttack(prevItem)
            print("You have equipped", allItems[item]["name"])
        # Message for case non-weapon
        elif itemtype != "weapon":
            print("You cannot equip this item.")
        # Message for case weapon not in inventory
        else:
            print("You do not have", allItems[item]["name"], "in your inventory")

    def move_to(self, direction, room_dict):
        # Check if room direction exists and is UNLOCKED
        room_status = room_dict[self.location].verify_move(direction)
        if (room_status == "UNLOCKED"):
            # Add character to the room they are moving to
            room_dict[room_dict[self.location].get_adj_room(
                direction)].char_add(self.ID)
            # Delete character from the room they are moving from
            room_dict[self.location].char_del(self.ID)
            # Update character location variable
            self.location = room_dict[self.location].get_adj_room(direction)
            print(self.name, "successfully moved to ",
                  room_dict[self.location].name)
            #Update recent move
            self.recent_move = direction

            # Check if room has been visited before, if yes play short descr if not play long description
            if (room_dict[self.location].get_visited() == "false"):
                print(room_dict[self.location].get_long_desc())
                room_dict[self.location].set_visited(
                    "true"
                )  # Make all printing done from the get() functions. So it can be reused in the look() functionality
            else:  # Issue with not printing first room location. Do it in the main function
                print(room_dict[self.location].get_short_desc())

        elif (room_status == "LOCKED"):
            for i in range(len(self.inventory)):
                if self.inventory[i] == "i12_key":
                    room_dict[self.location].locked[direction] = "UNLOCKED"
                    self.inventory.pop(i)
                    print("Key used and door unlocked")
                    # Add character to the room they are moving to
                    room_dict[room_dict[self.location].get_adj_room(
                        direction)].char_add(self.ID)
                    # Delete character from the room they are moving from
                    room_dict[self.location].char_del(self.ID)
                    # Update character location variable
                    self.location = room_dict[self.location].get_adj_room(
                        direction)
                    print(self.name, "successfully moved to ",
                          room_dict[self.location].name)
                    #Update recent move
                    self.recent_move = direction

                    # Check if room has been visited before, if yes play short descr if not play long description
                    if (room_dict[self.location].get_visited() == "false"):
                        print(room_dict[self.location].get_long_desc())
                        room_dict[self.location].set_visited(
                            "true"
                        )  # Make all printing done from the get() functions. So it can be reused in the look() functionality
                    else:  # Issue with not printing first room location. Do it in the main function
                        print(room_dict[self.location].get_short_desc())
                    return
            print("Unforturnately room is locked. Currently residing in ",
                  self.location)

        elif (room_status == "B_LOCKED"):
            for i in range(len(self.inventory)):
                if self.inventory[i] == "i13_bosskey":
                    room_dict[self.location].locked[direction] = "UNLOCKED"
                    self.inventory.pop(i)
                    print("Key used and door unlocked")
                    # Add character to the room they are moving to
                    room_dict[room_dict[self.location].get_adj_room(
                        direction)].char_add(self.ID)
                    # Delete character from the room they are moving from
                    room_dict[self.location].char_del(self.ID)
                    # Update character location variable
                    self.location = room_dict[self.location].get_adj_room(
                        direction)
                    print(self.name, "successfully moved to ",
                          room_dict[self.location].name)
                    #Update recent move
                    self.recent_move = direction

                    # Check if room has been visited before, if yes play short descr if not play long description
                    if (room_dict[self.location].get_visited() == "false"):
                        print(room_dict[self.location].get_long_desc())
                        room_dict[self.location].set_visited(
                            "true"
                        )  # Make all printing done from the get() functions. So it can be reused in the look() functionality
                    else:  # Issue with not printing first room location. Do it in the main function
                        print(room_dict[self.location].get_short_desc())
                    return
            print(
                "Unforturnately room is locked and can only be opened by the boss key. Currently residing in ",
                self.location)
        else:
            print("Unfortunately that direction is inaccessible residing in ",
                  self.location)

    def updateHealth(self, amount, room_dict):
        initial_health = self.health
        self.health += amount
        # If health is below 50%, the character enrages
        if self.health <= self.maxhealth / 2:
            self.enrage()
        # Updates the players health according to max health
        if self.health > self.maxhealth:
            self.health = self.maxhealth

        # Kills the player if health is <= 0
        elif self.health <= 0:
            self.health = 0
            self.die(room_dict)

        return self.health - initial_health

    def updateStats(self, item):
        # Update character stats according to items in inventory
        self.defense += allItems[item]["defense"]
        self.evasion += allItems[item]["evasion"]

    def updateAttack(self, prevItem):
        # Update attack stat based on equipped item
        self.attack -= allItems[prevItem]["damage"]
        self.attack += allItems[self.curItem]["damage"]

    def enrage(self):
        # Enrages the character when they reach 50% health
        if self.health <= self.maxhealth / 2 and self.state != "enraged":
            print(f"{self.name} has enraged!")
            self.health += round(self.health / 2)
            self.attack = round(self.attack * 1.25)
            self.defense = round(self.defense * 1.25)
            self.state = "enraged"
        else:
            return

    def die(self, room_dict):
        # Kills the character and removes them from the game/ends the game
        print(self.name, "has died.")
        self.dump(room_dict)
        self.dead = "True"

    # Dumps character's inventory on death
    def dump(self, room_dict):
        while self.inventory:
            item = self.inventory[0]
            print(self.name, "Dropped", allItems[item]["name"])
            room_dict[self.location].items.append(item)
            self.inventory.remove(item)
            if self.curItem == item:
                self.curItem = ""

    # Drops specified item
    def drop(self, item, room_dict):
        if item in self.inventory:
            print(self.name, "Dropped", allItems[item]["name"])
            room_dict[self.location].items.append(item)
            self.inventory.remove(item)
            if self.curItem == item:
                self.curItem = ""

    def consume(self, item, room_dict):
        item_id = item
        # Checks if item is in inventory
        if item in self.inventory:
            item_data = allItems[item]  #retrieves all datao
            # Checks if item is a health consumable
            if item_data["type"] == "health":
                # Updates character health
                health_recovered = self.updateHealth(item_data["health"],
                                                     room_dict)
                print("You have consumed", item_data["name"], "and recovered",
                      health_recovered, "health")
                self.inventory.remove(item_id)
            # Message for case item is not a consumable
            else:
                print("You cannot consume that.")
        # Message for case item is not in inventory
        else:

            print("You do not have", allItems[item]["name"],
                  "in your inventory.")

    def attack_target(self, target_id, char_dict, room_dict):
        target = char_dict[target_id]

        #Check if target in same room as player
        if target.location != self.location:
            print(self.name + "'s attack missed")
            return

        # Probability of hitting attack
        hit_chance = random.randint(1, target.evasion)

        if (hit_chance != target.evasion):
            # Attack power is equal to base attack + equipped weapon attack
            target.updateHealth(-((self.attack) - (target.defense)), room_dict)
            # if (self.curItem == ""):
            #     target.updateHealth(-(self.attack), room_dict)
            # else:
            #     target.updateHealth(
            #         -(self.attack + allItems[self.curItem]["damage"]),
            #         room_dict)
            if(target.dead == "False"):
                print(self.name, "successfully attacked", target.name,
                  "Their health is", target.health)
        else:
            print(self.name + "'s attack missed")

    # Ai that plays during enemy turn
    def update(self, char_dict, room_dict, player_ID):
        if (self.dead == "True" or self.playable == "True"):
            pass
        elif ((player_ID in room_dict[self.location].characters) and self.aggro == {}):
            self.aggro[player_ID] = player_ID
        # Second priority is attacking player if in room
        elif (player_ID in room_dict[self.location].characters and self.aggro):
            self.aggro[player_ID] = player_ID
            self.attack_target(player_ID, char_dict, room_dict)
        # First priority is picking up items in room
        elif (room_dict[self.location].items):
            self.grab(room_dict[self.location].items[0], room_dict)
        # Third priority is chasing player if aggro
        elif (self.aggro
              and ((player_ID not in room_dict[self.location].characters))):
            self.move_to(char_dict[player_ID].recent_move, room_dict)


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
        if (self.adjRooms[direction] != "NULL"):
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
        
class Item:

    def __init__(self, ID):
        self.ID = ID
        self.name = allItems[ID]["name"]
        self.type = allItems[ID]["type"]
        self.health = allItems[ID]["health"]
        self.damage = allItems[ID]["damage"]
        self.evasion = allItems[ID]["evasion"]
        self.desc = allItems[ID]["desc"]


class Parser:
    #initializing character and room objects
    def __init__(self, character, room_dict, char_dict):
        self.character = character
        self.room_dict = room_dict
        self.char_dict = char_dict
        self.translation_dict = {
            "Torch": "i01_torch",
            "Small Health Potion": "i02_smallhealthpot",
            "Large Health Potion": "i03_largehealthpot",
            "Rusty sword": "i04_rustysword",
            "Iron Chestplate": "i05_ironchestplate",
            "Neymar's Shinpads": "i06_neymarsshinpads",
            "Thor's Hammer": "i07_thorshammer",
            "Voidwyrm Scalemail": "i08_voidwyrmscalemail",
            "Killmonger's Vambraces": "i09_killmongersvambraces",
            "Edward's Katana": "i10_edwardskatana",
            "Cloak of Evasion": "i11_cloakofevasion",
            "Normal Room Key": "i12_key",
            "Boss Room Key": "i13_bosskey",
            "Sven": "name",
            "Thanos": "c2_thanos",
            "Neymar": "c3_neymar",
            "Aang": "c4_aang",
            "Kratos": "c5_kratos",
            "Rose": "c6_rose",
            "Killmonger": "c7_killmonger",
            "Edward Kenway": "c8_edward kenway",
            "Maleficar": "c9_maleficar"
        }

    def handle_die(self, _):
        self.character.die(self.room_dict)

    #handles the getInventory command
    def handle_getInventory(self):
        self.character.getInventory()

    #handle_move method will move the character to the room they want to move to
    def handle_move_to(self, direction):
        #if direction is not empty
        if direction in ["N", "W", "E", "S"]:
            #call move_to method on character object
            self.character.move_to(direction, self.room_dict)
        #if direction not entered, then ask the user to enter a direction
        else:
            print("Invalid direction! Choose N or E or W or S")

    #handle_grab method will add the item to the character's inventory
    def handle_grab(self, item, room_dict):
        #if item is not empty
        if item in allItems:
            #then grab the item and add it to the character's inventory
            self.character.grab(item, room_dict)
        else:
            print("nothing to grab!")

    #handles look command, prints the location name, room description, and items in the room
    def handle_look(self, _):
        self.character.look(self.room_dict)

    #handles equipping the items
    def handle_equip(self, item):
        #if items is in player's inventory
        if item in self.character.inventory:
            #then equip it
            self.character.equip(item)
        else:
            print("The item is not in your inventory")

    def handle_consume(self, item):
        if item in self.character.inventory:
            self.character.consume(item, self.room_dict)

    def handle_enrage(self, _):
        self.character.enrage()

    def handle_attack(self, target_id):
        #look for the target in the room
        if target_id in self.room_dict[self.character.location].characters:
            #if found then attack
            self.character.attack_target(target_id, self.character.char_dict,
                                         self.room_dict)

    def handle_drop(self, item):
        if item in self.character.inventory:
            self.character.drop(item, self.room_dict)

    def handle_attack_target(self, target_id):
        self.character.attack_target(target_id, self.room_dict)

    def user_input(self):
        return (input("> "))

    #parsing user input
    def parse_command(self):

        command = self.user_input().lower().strip()
        if " " not in command:
            trimmed_command = command.strip()
            if trimmed_command == "inspect":
                self.character.inspect()
            elif trimmed_command == "inventory":
                self.character.getInventory()
            elif trimmed_command == "look":
                self.character.look(self.room_dict)

        else:
            #if the command is more than 2 words, split into verb and noun
            split_command = command.split(" ", 1)
            verb = split_command[0].lower().strip()
            # Clean up noun, remove apostrophe and spaces
            noun = split_command[1].lower().replace("'", "").strip()
            #check if the command exists in commands' dictionary
            if verb == 'grab':
                if noun == 'torch':
                    self.character.grab(self.translation_dict["Torch"],
                                        self.room_dict)

                elif noun == 'small health potion':
                    self.character.grab(
                        self.translation_dict["Small Health Potion"],
                        self.room_dict)
                elif noun == 'large health potion':
                    self.character.grab(
                        self.translation_dict["Large Health Potion"],
                        self.room_dict)
                elif noun == 'rusty sword':
                    self.character.grab(self.translation_dict["Rusty sword"],
                                        self.room_dict)
                elif noun == 'iron chestplate':
                    self.character.grab(
                        self.translation_dict["Iron Chestplate"],
                        self.room_dict)
                elif noun == 'neymars shinpads':
                    self.character.grab(
                        self.translation_dict["Neymar's Shinpads"],
                        self.room_dict)
                elif noun == "thors hammer":
                    self.character.grab(self.translation_dict["Thor's Hammer"],
                                        self.room_dict)
                elif noun == 'voidwyrm scalemail':
                    self.character.grab(
                        self.translation_dict["Voidwyrm Scalemail"],
                        self.room_dict)
                elif noun == 'killmongers vambraces':
                    self.character.grab(
                        self.translation_dict["Killmonger's Vambraces"],
                        self.room_dict)
                elif noun == 'edwards katana':
                    self.character.grab(
                        self.translation_dict["Edward's Katana"],
                        self.room_dict)
                elif noun == 'cloak of evasion':
                    self.character.grab(
                        self.translation_dict["Cloak of Evasion"],
                        self.room_dict)
                elif noun == 'normal room key':
                    self.character.grab(
                        self.translation_dict["Normal Room Key"],
                        self.room_dict)
                elif noun == 'boss room key':
                    self.character.grab(self.translation_dict["Boss Room Key"],
                                        self.room_dict)

                else:
                    print(f"{noun} not found.")

            if verb == "drop":
                if noun == 'torch':
                    self.character.drop(self.translation_dict["Torch"],
                                        self.room_dict)
                elif noun == 'small health potion':
                    self.character.drop(
                        self.translation_dict["Small Health Potion"],
                        self.room_dict)
                elif noun == 'large health potion':
                    self.character.drop(
                        self.translation_dict["Large Health Potion"],
                        self.room_dict)
                elif noun == 'rusty sword':
                    self.character.drop(self.translation_dict["Rusty sword"],
                                        self.room_dict)
                elif noun == 'iron chestplate':
                    self.character.drop(
                        self.translation_dict["Iron Chestplate"],
                        self.room_dict)
                elif noun == 'neymars shinpads':
                    self.character.drop(
                        self.translation_dict["Neymar's Shinpads"],
                        self.room_dict)
                elif noun == 'thors hammer':
                    self.character.drop(self.translation_dict["Thor's Hammer"],
                                        self.room_dict)
                elif noun == 'voidwyrm scalemail':
                    self.character.drop(
                        self.translation_dict["Voidwyrm Scalemail"],
                        self.room_dict)
                elif noun == 'killmongers vambraces':
                    self.character.drop(
                        self.translation_dict["Killmonger's Vambraces"],
                        self.room_dict)
                elif noun == 'edwards katana':
                    self.character.drop(
                        self.translation_dict["Edward's Katana"],
                        self.room_dict)
                elif noun == 'cloak of evasion':
                    self.character.drop(
                        self.translation_dict["Cloak of Evasion"],
                        self.room_dict)
                elif noun == 'normal room key':
                    self.character.drop(
                        self.translation_dict["Normal Room Key"],
                        self.room_dict)
                elif noun == 'boss room key':
                    self.character.drop(self.translation_dict["Boss Room Key"],
                                        self.room_dict)
                else:
                    (print(f"{noun} not found."))
                    
            if verb == "equip":
                if noun == 'torch':
                    self.character.equip(self.translation_dict["Torch"])
                elif noun == 'small health potion':
                    self.character.equip(
                        self.translation_dict["Small Health Potion"])
                elif noun == 'large health potion':
                    self.character.equip(
                        self.translation_dict["Large Health Potion"])
                elif noun == 'rusty sword':
                    self.character.equip(self.translation_dict["Rusty sword"])
                elif noun == 'iron chestplate':
                    self.character.equip(
                        self.translation_dict["Iron Chestplate"])
                elif noun == 'neymars shinpads':
                    self.character.equip(
                        self.translation_dict["Neymar's Shinpads"])
                elif noun == 'thors hammer':
                    self.character.equip(
                        self.translation_dict["Thor's Hammer"])
                elif noun == 'voidwyrm scalemail':
                    self.character.equip(
                        self.translation_dict["Voidwyrm Scalemail"])
                elif noun == 'killmongers vambraces':
                    self.character.equip(
                        self.translation_dict["Killmonger's Vambraces"])
                elif noun == 'edwards katana':
                    self.character.equip(
                        self.translation_dict["Edward's Katana"])
                elif noun == 'cloak of evasion':
                    self.character.equip(
                        self.translation_dict["Cloak of Evasion"])
                elif noun == 'normal room key':
                    self.character.equip(
                        self.translation_dict["Normal Room Key"])
                elif noun == 'boss room key':
                    self.character.equip(
                        self.translation_dict["Boss Room Key"])
                else:
                    print(f"{noun} not found.")

            if verb == "consume":
                if noun == 'small health potion':
                    self.character.consume(
                        self.translation_dict["Small Health Potion"],
                        self.room_dict)
                elif noun == 'large health potion':
                    self.character.consume(
                        self.translation_dict["Large Health Potion"],
                        self.room_dict)
                else:
                    print(f"{noun} not found.")

            if verb == "attack":
                if noun == 'aang':
                    self.character.attack_target(self.translation_dict["Aang"],
                                                 self.char_dict,
                                                 self.room_dict)
                elif noun == 'kratos':
                    self.character.attack_target(
                        self.translation_dict["Kratos"], self.char_dict,
                        self.room_dict)
                elif noun == 'rose':
                    self.character.attack_target(self.translation_dict["Rose"],
                                                 self.char_dict,
                                                 self.room_dict)
                elif noun == 'killmonger':
                    self.character.attack_target(
                        self.translation_dict["Killmonger"], self.char_dict,
                        self.room_dict)
                elif noun == 'edward kenway':
                    self.character.attack_target(
                        self.translation_dict["Edward Kenway"], self.char_dict,
                        self.room_dict)
                elif noun == 'maleficar':
                    self.character.attack_target(
                        self.translation_dict["Maleficar"], self.char_dict,
                        self.room_dict)
                elif noun == 'neymar':
                    self.character.attack_target(
                        self.translation_dict["Neymar"], self.char_dict,
                        self.room_dict)
                elif noun == 'thanos':
                    self.character.attack_target(
                        self.translation_dict["Thanos"], self.char_dict,
                        self.room_dict)
                else:
                    print(f"{noun} not found.")

            if verb == "move":
                if noun == 'north':
                    self.character.move_to("N", self.room_dict)
                elif noun == 'east':
                    self.character.move_to("E", self.room_dict)
                elif noun == 'west':
                    self.character.move_to("W", self.room_dict)
                elif noun == 'south':
                    self.character.move_to("S", self.room_dict)

                #if it does, then call the corresponding method
