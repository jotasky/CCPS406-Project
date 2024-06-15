import new_classes
import random
import json
from typing import Dict
from new_classes import Parser


with open("dialogue.json", "r") as file:
    dialogue = json.load(file)
class Game:


    def __init__(self):
        self.room_dict = {}
        self.char_dict = {}

        # Initialize rooms and characters
        self.init_rooms()
        self.init_characters()
        # Set the player character
        self.playerChar = self.char_dict["c1_player"]
        self.parser = Parser(self.playerChar, self.room_dict, self.char_dict)

        self.final_dialogue_shown = False

    def init_rooms(self):
        # Loop through and create the room object dictionary
        for room in new_classes.allRooms:
            self.room_dict[room] = new_classes.Room(room)

    def init_characters(self):
        # Loop through and create the character dictionary
        for character in new_classes.allCharacters:
            self.char_dict[character] = new_classes.Character(character)

    def main(self):
        pass

    
    print("\n".join(dialogue["intro"]))
    def gameLoop(self):
        while self.playerChar.dead == "False":
            
            self.parser.parse_command()
            for char in self.char_dict:
                self.char_dict[char].update(self.char_dict, self.room_dict, self.playerChar.ID)
            if self.playerChar.location == "r13" and not self.final_dialogue_shown:
                print("\n".join(dialogue["final boss"]))
                self.final_dialogue_shown = True
            if self.char_dict["c2_thanos"].dead == "True":
                print("\n".join(dialogue["outro_win"]))
                self.playerChar.inspect()
                break

if __name__ == "__main__":
    game = Game()
    game.main()
    game.gameLoop()
    if(game.playerChar.dead == "True"):
        print("\n".join(dialogue["outro_lose"]))
