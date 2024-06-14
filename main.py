import new_classes
class Main:
    # Initialization function: create the room, character, and item dictionary to store objects
    def __init__(self):
        room_dict = {}
        char_dict = {}
        item_dict = {}

        # Loop through and create the room object dictionary
        for room in new_classes.allRooms:
            room_dict[room] = new_classes.Room(room)

        # Loop through and create the character dictionary
        for character in new_classes.allCharacters:
            char_dict[character] = new_classes.Character(character)

        # Loop through and create the item dictionary
        for item in new_classes.allItems:
            item_dict[item] = new_classes.Item(item)

        # Testing the character's move_to function
        char_dict["c1_player"].move_to("E", room_dict)
        char_dict["c1_player"].move_to("E", room_dict)
        char_dict["c1_player"].move_to("W", room_dict)

if __name__ == '__main__':
    main = Main()