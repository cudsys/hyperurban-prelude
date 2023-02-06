print("alright...fingers crossed!!!")
# endless text adventure game
# player progresses through an endless amount of rooms
# player has a name, health (hp), karma (kr) and an inventory (inv) array
# player starts with 50 health and 0 karma
# the game ends when the player reaches 0 hp or lower (physical death) OR when the player reaches -50 karma or lower (ego death)
# karma is gained by choosing choices that give karma (i.e. good deeds)
# karma can be lost by choosing choices that take karma (i.e. bad deeds, hurting people, etc.)
# rooms are picked randomly from rooms.json
# intensity level determines what rooms are picked and can be a number between 0 and 10 (rounded to one decimal place i.e. 4.6)
# difficulties are planned to be added to the game and will change the player's starting stats

# room generation system:
# each room contains the following attributes:
# name (string), description (string), skippable (boolean), choices (class), and intensity (number)
# choices are a class that contains the following attributes:
# text (string), outcomes (class)
# outcomes are a class that contains the following attributes:
# rate (number ranging from 1-100), effect (string) and text (string)
# if an outcome's rate is 100, that outcome will always be chosen
# the rate of all outcomes in a choice must add up to 100
# the first outcome in a choice is considered the best outcome and it's rate will be displayed along with the text when selecting a choice
# example:
# 1. Run for it! (30%)
# example of a room:
# {
    # "name": "a_thief",
    # "description": "A thief suddenly draws a knife from their pocket and points it at you. "Gimme something or I'll just take your life!",
    # "skippable": False,
    # "choices": [
        #     {
        #         "text": "Run for it!",
        #         "outcomes": [
            #         {
                #             "rate": 30,
                #             "effect": "next_room",
                #             "text": "You run for it!"
            #         },
            #
                #             "rate": 70,
                #             "effect": "instakill",
                #             "text": "Long story short, running away didn't work out."       

            #         },
            #     ]   

            #     ]
        #     },
        #     {
        #         "text": "Surrender a random item",
        #         "outcomes": [
            #         {
                #             "rate": 100,
                #             "effect": "inv_remove_random",
                #             "text": "You quickly surrender a random item to the theif. They run away."
            #         },
        #     ]
# }

# recap: rooms are objects that contain choice objects which contain outcome objects

# choice class
# each choice object contains the following attributes:
# text (string): the choice's text
# outcomes (array): the choice's outcomes which is an array of outcome objects
# when a choice is chosen, an outcome is chosen depending on the outcome's rate

# outcome class
# outcomes are objects that contain the following attributes:
# rate (number ranging from 1-100): determines the chance that the outcome will be chosen
# effect (string): determines what happens when the outcome is chosen
# text (string): the text that will be displayed when the outcome is chosen

# effects are parsed out of the text to determine what the effect will do
# list of all possible effects:
# "next_room": moves the player to the next room immediately after the outcome text is displayed
# "heal #": heals the player for # hp. hp cannot exceed 10.
# "hurt #": hurts the player for # hp. hp can exceed 0. (overkill)
# "praise #": praises the player for # kr. kr cannot exceed 50.
# "shun #": shuns the player for # kr. kr can exceed 0. (negative karma)
# "instakill": instantly kills the player (like "hurt #", but sets the player's hp to -99 instead of 0)
# "cancel": instantly kills the player's ego (like "shun #", but sets the player's karma to -50)
# "inv_add x": adds x items to the player's inventory
# "inv_remove x": removes x items from the player's inventory if possible
# "inv_remove_random": removes a random item from the player's inventory if possible

# get them modules
print("loading modules...")
import random
import os
import sys
import time
import math
import json
print("done!")
# each room is stored in a json file in the rooms folder
# import all the json files in the rooms folder and store them in a list called jsonrooms
print("loading rooms...")
jsonrooms = []
for filename in os.listdir("rooms"):
    if filename.endswith(".json"):
        jsonrooms.append(json.load(open("rooms/" + filename, "r")))
print("done! loaded {} rooms".format(len(jsonrooms)))











# initialize game variables
game = None

# game variables:
# current room number
# intensity level
# player variables

# game variables

        


    # next_room() is a function that generates a new room and advances the player to it
    
        
        




# initialize player variables (class)
class Player:
    def __init__(self, name):
        self.name = name        # name
        self.hp = 50            # health
        self.kr = 0             # karma
        self.inventory = []     # inventory

    def heal(self, amount):
        self.hp += amount
        print("+{} health".format(amount))
        if self.hp > 10:
            self.hp = 10
            print("...but you're maxed out!")

    def hurt(self, amount):
        self.hp -= amount
        print("-{} health".format(amount))

    def praise(self, amount):
        self.kr += amount
        print("+{} karma".format(amount))

    def shun(self, amount):
        self.kr -= amount
        print("-{} karma".format(amount))

    def instakill(self):
        self.hp = -99

    def cancel(self):
        self.kr = -50



# room class
class Room:
    def __init__(self, name, description, skippable, choices):
        self.name = name
        self.description = description
        self.skippable = skippable
        self.choices = choices


class Choice:
    def __init__(self, text, outcomes):
        self.text = text
        self.outcomes = outcomes

    def chooseOutcome(self):
        chosen = random.randint(0, len(self.outcomes) - 1)
        chosen_outcome = self.outcomes[chosen]
        chosen_outcome.rate = chosen_outcome.rate / 100
        chosen_outcome.effect = chosen_outcome.effect.lower()
        chosen_outcome.text = chosen_outcome.text.lower()
        return chosen_outcome
    
    # function that generates a string to display the choice's text along with the choice's success rate
    # example:
    # Run for it! (30%)
    def generateText(self):
        output = self.text + " ({}%)".format(self.outcomes[0].rate*100)
        return output





class Outcome:
    def __init__(self, rate, effect, text):
        self.rate = rate
        self.effect = effect
        self.text = text

    # cause() is a function that takes the effect string, parses it and runs the appropriate function

class Game:
    def __init__(self):
        self.goal = None            # win condition
        self.current_room = None    # current room
        self.rooms = 0              # rooms cleared
        self.intensity_level = 1    # intensity starts at 1
        # new player object with the temporary name "Player"
        # playe's name will be changed at the beginning of the game
        self.player = Player("Player")

    def next_room(self):
        self.rooms += 1
        self.current_room = None

    # generateRoom() is a function that creates a room object using data from a random room from rooms.json. the same process applies for the choices and outcomes of the room
    def generateRoom(self):
        # pick a random room from the rooms.json file
        room = jsonrooms[random.randint(0, len(jsonrooms) - 1)]
        # create a new room object using the room data but leave the choices array empty
        new_room = Room(room["name"], room["description"], room["skippable"], [])
        # for each choice in the room, create a new choice object and add it to the choices array
        for choice in room["choices"]:
            new_choice = Choice(choice["text"], [])
            # for each outcome in the choice, create a new outcome object and add it to the outcomes array
            for outcome in choice["outcomes"]:
                new_outcome = Outcome(outcome["rate"], outcome["effect"], outcome["text"])
                new_outcome.rate = new_outcome.rate / 100
                new_outcome.effect = new_outcome.effect.lower()
                new_outcome.text = new_outcome.text.lower()
                new_choice.outcomes.append(new_outcome)

            new_room.choices.append(new_choice)

        return new_room

    # game_over() is a function that ends the game and displays your results
    def game_over(self):
        print("GAME OVER!!")
        # cause of death (physical death or ego death)
        # if player hp is 0, physical death
        # if player hp is -10 or lower, overkill
        # if player hp is -50 or lower, ego death\
        # if none apply, display a special message
        if self.player.hp == 0:
            print("You died!")
        elif self.player.hp <= -10:
            print("You got destroyed!")
        elif self.player.kr <= -50:
            print("You're not wanted in this world anymore.")

        else:
            print("But...you're still alive? Interesting...")
        
        print("\n\nYou survived {} rooms before you died with {} karma.".format(self.rooms, self.player.kr))








def mainmenu():
    print("""
    __                                     __              
   / /_  __  ______  ___  _______  _______/ /_  ____ _____ 
  / __ \/ / / / __ \/ _ \/ ___/ / / / ___/ __ \/ __ `/ __ \\
 / / / / /_/ / /_/ /  __/ /  / /_/ / /  / /_/ / /_/ / / / /
/_/ /_/\__, / .___/\___/_/   \__,_/_/  /_.___/\__,_/_/ /_/ 
      /____/_/         
                          prelude                                    


1. start
2. about
3. quit
""")

    while True:
        match input():
            case "1":
                modeselect()
            case "2":
                print("""
this game serves as a precursor to hyperurban, a much bigger and more story rich game.

hyperurban prelude was made to experiment with the game's main mechanic of traversing the game world in moments.
                """)
            case "3":
                exit()
            case _:
                print("not an option")


def modeselect():
    print("""






S-S-S-S-SELECT YOUR MODE!!!

1. endless mode
a never-ending stream of moments, one after another. how far can you get?

2. samaritan mode (coming soon!)
reach a goal amount of karma as fast as possible.

3. ironman mode (coming soon!)
no inventory! how long can you last without items?


0. back to main menu
    """)

    while True:
        match input():
            case "1":
                difficultyselect()
            case "2":
                print("coming soon!")
            case "3":
                print("coming soon!")
            case "0":
                mainmenu()    
            case _:
                print("not an option")

def difficultyselect():
    print("""
    



S-S-S-S-SELECT YOUR DIFFICULTY!!!

1. normal: the way the game is meant to be played
below difficulties are coming soon!

2. hard: more difficult moments and more strict losing conditions
3. insane: for masochists whose dominatrix just so happens to be lady luck
4. ballistic: intensity starts at 10, 1 health, -49 karma. good luck! :)

0. back to mode selection
    """)

    match input():
        case "1":
            game = Game()
            game_loop()
        case "0":
            modeselect()
        case _:
            print("not an option")



def game_loop():
    while game.player.hp > 0 and game.player.kr > -50:
        if game.current_room == None:
            game.generateRoom()


    



print("alright lets do this shit\n\n\n\n")

mainmenu()