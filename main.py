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
# "gameover": causes a game over immediately, regardless of health or karma
# "cancel": instantly kills the player's ego (like "shun #", but sets the player's karma to -50)
# "inv_add x": adds x items to the player's inventory
# "inv_remove x": removes x items from the player's inventory if possible
# "inv_remove_random": removes a random item from the player's inventory if possible

# get them modules
print("loading modules...")
import random
import os
import json
print("done!")
# each room is stored in a json file in the rooms folder
# import all the json files in the rooms folder and store them in a list called jsonrooms except for template.json
print("loading rooms...")
jsonrooms = []
for filename in os.listdir("rooms"):
    if filename.endswith(".json") and filename!= "template.json":
        jsonrooms.append(json.load(open("rooms/" + filename, "r")))
print("done! loaded {} rooms".format(len(jsonrooms)))

# initialize game variables


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
        self.hp = 10            # health
        self.maxhp = 10         # max health
        self.kr = 0             # karma
        self.inventory = []     # inventory

    def heal(self, amount):
        self.hp += amount
        print("+{} health".format(amount))
        if self.hp > self.maxhp:
            self.hp = self.maxhp
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
        print("Mortis.")

    def cancel(self):
        self.kr = -50
        print("Shame on you!")


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

    # chooseOutcome() is a function that chooses a random outcome from a list of outcomes
    # however, the chance of an outcome being chosen is determined by the outcome's rate
    # we can use random.choices() to weight the outcomes by their rate
    def chooseOutcome(self):
        # put the rates of the outcomes into a list
        rates = []
        for outcome in self.outcomes:
            rates.append(outcome.rate)
        # use random.choices() to pick an outcome, using the rates list as weights
        choice = random.choices(self.outcomes, weights=rates, k=1)[0]
        return choice

    
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
                new_outcome.text = new_outcome.text
                new_choice.outcomes.append(new_outcome)

            new_room.choices.append(new_choice)

        return new_room

    # game_over() is a function that ends the game and displays your results
    def game_over(self):
        print("\n\n\nGAME OVER!!")
        # cause of death (physical death or ego death)
        # if player hp is 0, physical death
        # if player hp is -10 or lower, overkill
        # if player hp is -50 or lower, ego death\
        # if none apply, display a special message
        if self.player.hp <= 0:
            print("You died!")
        elif self.player.hp <= -10:
            print("You got destroyed!")
        elif self.player.kr <= -50:
            print("You're not wanted in this world anymore.")

        else:
            print("But...you're still alive? Interesting...")
        
        print("\n\nYou survived {} moments before dying with {} karma.\n".format(self.rooms, self.player.kr))
        input("Press enter to continue...")
        mainmenu()


    def parseOutcome(self, text):
        text = text.split(" ")
        match text[0]:
            case "heal":
                self.player.heal(int(text[1]))
            case "hurt":
                self.player.hurt(int(text[1]))
            case "praise":
                self.player.praise(int(text[1]))
            case "shun":
                self.player.shun(int(text[1]))
            case "instakill":
                self.player.instakill()
            case "cancel":
                self.player.cancel()
            case _:
                print("Nothing happened... (invalid effect?)")
        # if any of the losing conditions are met, game_over() is called
        if self.player.kr <= -50 or self.player.hp <= 0:
            self.game_over()

                
            


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
        match input("> "):
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
        match input("> "):
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

    match input("> "):
        case "1":
            game_loop()
        case "0":
            modeselect()
        case _:
            print("not an option")


def game_loop():
    game = Game()
    game.player.name = input("What is your name? > ")
    if game.player.name == "":
        game.player.name = "Hailey"

    while game.player.hp > 0 and game.player.kr > -50:
        error_msg = "What would you like to do? > "
        state = "choosing"
        game.current_room = game.generateRoom()
        
        # print room number and description
        while game.current_room is not None:
            print("\n\n\n\n\n\n\n\n\n\n\n\n")
            match state:
                case "choosing":
                     print("Moment {0}\n\n{1}".format(game.rooms + 1, game.current_room.description))

                     i = 1
                     for choice in game.current_room.choices:
                        print("{}. ".format(i) + choice.generateText())
                        i += 1
                case "result":
                    print("\n\n\n{0}".format(current_outcome.text))
                    game.parseOutcome(current_outcome.effect)
                    print("\n{0}       {1}/{3} HP | {2} KR".format(game.player.name, game.player.hp, game.player.kr, game.player.maxhp))
                    input("Press enter to continue...")
                    state = "choosing"
                    game.next_room()
                    break
                    



           
            
            # print player stats
            print("\n{0}       {1}/{3} HP | {2} KR".format(game.player.name, game.player.hp, game.player.kr, game.player.maxhp))
            # accept player input
            
            current_choice = input(error_msg)
            # check if the choice is between 1 and the length of the room choices
            if current_choice == "":
                error_msg = "That is not a valid choice. Please try again. > "
            elif int(current_choice) > len(game.current_room.choices) or int(current_choice) < 1:
                error_msg = "That is not a valid choice. Please try again. > "
                
            else:
                # the selected choice is indexed at current_choice - 1
                current_outcome = game.current_room.choices[int(current_choice) - 1].chooseOutcome()
                state = "result"


print("alright lets do this shit\n\n\n\n")

# fun fact: this is where the game actually starts
mainmenu()