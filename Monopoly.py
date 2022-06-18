#___________________Import Needed Modules______________
import random
import sys
from random import randint

#___________________Define Needed Functions______________
playing = True

def move(current):
    match = False
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    value = die1 + die2
    after = current + value
    if after > 39:
        after -= 40
    return after

def roll():
    match = False
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    if die1 == die2:
        match = True
    return match

def buy(player):
    if player.money >= player.location.price:
        player.location.owner = player
        player.money -= player.location.price
    else:
        print("Insufficient Funds")

def chancecard(player, otherplayer):
    owned = []
    for each in board:
        if each.owner == player:
            owned.append(each)
    house = 0
    hotel = 0
    cardnum = random.randint(1,8)
    if cardnum == 1:
        print("Chance Card: Advance to St. Charles Place")
        player.location = board[11]
    elif cardnum == 2:
        print("Chance Card: Bank pays you a dividend of $50")
        player.money += 50
    elif cardnum == 3:
        print("Chance Card: Your building and loan matures, collect $100")
        player.money += 100
    elif cardnum == 4:
        print("Chance Card: You have been elected player of the board...Pay " + otherplayer.name + " $50")
        player.money -= 50
        otherplayer.money += 50
    elif cardnum == 5:
        print("Chance Card: You have just gotten a get out of jail free card!")
        player.jailcard += 1
    elif cardnum == 6:
        print("Chance Card: Go to Jail")
        player.location = board[10]
        player.injail = True
    elif cardnum == 7:
        print("Chance Card: Your properties need repairs! Pay $25 for each house and $100 for each hotel")
        for each in owned:
            if each.level == "house1" or each.level == "house2" or each.level == "house3":
                house += 1
            elif each.level == "hotel":
                hotel += 1
        moneyowed = (25 * house) + (100 * hotel)
        player.money -= moneyowed
        print("You just payed " + str(moneyowed) + " for repairs")
    elif cardnum == 8:
        print("Chance Card: Pay Poor Tax of $15")
        player.money -= 15

def communitychest(player):
    cardnum = random.randint(1,6)
    if cardnum == 1:
        print("Community Chest: Advance To Go")
        player.location = board[0]
    elif cardnum == 2:
        print("Community Chest: Collect $100")
        player.money += 100
    elif cardnum == 3:
        print("Community Chest: Collect $150")
        player.money += 150
    elif cardnum == 4:
        print("Community Chest: Pay Taxes of $50")
        player.money -= 50
    elif cardnum == 5:
        print("Community Chest: Go To Jail")
        player.location = board[10]
        player.injail = True
    elif cardnum == 6:
        print("Community Chest: You have just gotten a get out of jail free card")
        player.jailcard += 1

def upgrade(player):
    owned = []
    for each in board:
        if each.owner == player:
            owned.append(each)
    print("________________________________________________________________\nChoose an owned property to upgrade:")
    for each in owned:
        print(each.name + " - Upgrade Costs: " + str(each.uc) + ". Current Level: " + each.level)
    if len(owned) == 0:
        print("You have no properties to upgrade...keep playing!")
    else:
        while True:
            upprops = input("Enter the name of each property you want to upgrade (Type 'end' when done): ")
            if upprops == "end":
                print("________________________________________________________________")
                break
            else:
                for each in owned:
                    if upprops == each.name:
                        if each.type == "rental":
                            if player.money >= each.uc:
                                if each.level == "single":
                                    each.level = "house1"
                                    player.money -= each.uc
                                elif each.level == "house1":
                                    each.level = "house2"
                                    player.money -= each.uc
                                elif each.level == "house2":
                                    each.level = "house3"
                                    player.money -= each.uc
                                elif each.level == "house3":
                                    each.level = "hotel"
                                    player.money -= each.uc
                                elif each.level == "hotel":
                                    print("There is already a hotel here, cannot upgrade further")
                            else:
                                print("Insufficient Funds")
                            print("________________________________________________________________\nYou just upgraded " + each.name + " for " + str(each.uc) + " to " + each.level + ". Current balance: " + str(player.money))
                        else:
                            print("This type of property cannot be upgraded")

def mortgage(player):
    owned = []
    for each in board:
        if each.owner == player:
            owned.append(each)
    print("________________________________________________________________\nChoose an owned property to sell bank to the bank:")
    if len(owned) == 0:
        print("You have no properties to sell...time for bankruptcy?")
    else:
        for each in owned:
            print(each.name + ": " + str(each.findmort()) + " - Mortgage Value")
        while True:
            mortprops = input("Enter the name of each property you want to mortgage (Type 'end' when done): ")
            if mortprops == "end":
                print("________________________________________________________________")
                break
            else:
                for each in owned:
                    if mortprops == each.name:
                        each.owner = computer
                        player.money += each.findmort()
                        print("________________________________________________________________\nYou just sold " + each.name + " to the bank for " + str(each.mortgage) + ". Current balance: " + str(player.money))

def viewstatus(player):
    owned = []
    for each in board:
        if each.owner == player:
            owned.append(each)
    print("________________________________________________________________")
    print("Your current balance: " + str(player.money))
    if len(owned) == 0:
        print("You do not own any properties as of yet...Be on the lookout")
    else:
        print("Your property portfolio:")
        for each in owned:
            print("Name: " + each.name + ", Current Rent Price: " + str(each.findrent()), ", Property Type: " + each.level)
    print("________________________________________________________________")

def bankrupt(player):
    print("________________________________________________________________")
    owned = []
    for each in board:
        if each.owner == player:
            owned.append(each)
    player.playing = False
    for each in owned:
        each.owner = computer
    if player == player1:
        print(player1.name + " went bankrupt...Congratulations " + player2.name + ", you win!")
    elif player == player2:
        print(player2.name + " went bankrupt...Congratulations " + player1.name + ", you win!")
    sys.exit()

def endturn(player):
    if player.money < 0:
        mortgage(player)
    else:
        while True:
            command = input("Commands: 'e' - end turn, 'v' - view properties and balance, 'm' - mortgage, 'b' - declare bankruptcy: , 'u' - upgrade properties... ")
            if command == "e":
                break
            elif command == "v":
                viewstatus(player)
            elif command == "m":
                mortgage(player)
            elif command == "u":
                upgrade(player)
            elif command == "b":
                bankrupt(player)

def auction(auc1, auc2, auc1bal, auc2bal, prop, bid):
    bid.bidder = auc1
    auct = 1
    print("________________________________________________________________")
    print("Rules: Highest Bidder Wins, Press 'e' to drop out of the bid")
    print("Property: " + prop.name + ", Price: " + str(prop.price) + ", Rent: " + str(prop.findrent()))
    while True:
        if auct == 1:
            prompt = input(auc1.name + " please enter your bid...Current bid is at " + str(bid.price) + "... ")
            if bid.price > auc1bal:
                print("You do not have enough money to continue the bid...")
                break
            if prompt == "e":
                break
            elif int(prompt) > auc1bal:
                print("You do not have enough money to place this bid...")
            elif int(prompt) > bid.price:
                bid.price = int(prompt)
                bid.bidder = auc1
                auct = 2
            else:
                print("Enter a bid higher than the current value...")
        elif auct == 2:
            prompt = input(auc2.name + " please enter your bid...Current bid is at " + str(bid.price) + "... ")
            if bid.price > auc2bal:
                print("You do not have enough money to continue the bid...")
                break
            if prompt == "e":
                print("________________________________________________________________")
                break
            elif int(prompt) > auc2bal:
                print("You do not have enough money to place this bid...")
            elif int(prompt) > bid.price:
                bid.price = int(prompt)
                bid.bidder = auc2
                auct = 1
            else:
                print("Enter a bid higher than the current value...")
    if bid.bidder == player1:
        print("________________________________________________________________\nCongratulations " + player1.name + " you have won the bid. You now own " + prop.name)
        prop.owner = player1
        auc1bal -= bid.price
        player1.money = auc1bal
    elif bid.bidder == player2:
        print("________________________________________________________________\nCongratulations " + player2.name + " you have won the bid. You now own " + prop.name)
        prop.owner = player2
        auc2bal -= bid.price
        player2.money = auc2bal
    print("End of Auction")
    print("________________________________________________________________")

#_____________________Define Custom Data Types___________________

class player_profile:
    def __init__(player, color, token, money, location, name, playing, injail, jc):
        player.color = color
        player.token = token
        player.money = money
        player.location = location
        player.jailcard = jc
        player.name = name
        player.playing = playing
        player.injail = injail
        player.jailattempts = 3

class property_profile:
    def __init__(property, name, owner, price, single, propertytype, numloc, mortgage, level, h1, h2, h3, hotel, upgradecosts):
        property.name = name
        property.owner = owner
        property.price = price
        property.type = propertytype
        property.loc = numloc
        property.mortgage = mortgage
        property.level = level
        property.uc = upgradecosts
        property.single = single
        property.h1 = h1
        property.h2 = h2
        property.h3 = h3
        property.hotel = hotel

    def findrent(property):
        if property.level == "single" or property.level == "railroad":
            property.rent = property.single
        elif property.level == "house1":
            property.rent = property.h1
        elif property.level == "house2":
            property.rent = property.h2
        elif property.level == "house3":
            property.rent = property.h3
        elif property.level == "hotel":
            property.rent = property.hotel
        return property.rent

    def findmort(property):
        if property.level == "single" or property.level == "railroad":
            property.mortgage = property.mortgage
        elif property.level == "house1":
            property.mortgage = round(property.mortgage/4)
        elif property.level == "house2":
            property.mortgage = round(property.mortgage/4)
        elif property.level == "house3":
            property.mortgage = round(property.mortgage/3)
        elif property.level == "hotel":
            property.mortgage = round(property.mortgage/2)
        return property.mortgage


class thebid:
    def __init__(self, bidder, price):
        self.bidder = bidder
        self.price = price

#___________________Initialization Process_____________________#
starting_money = 2100

print("Welcome to Monopoly Duel - a two player monopoly showdown - Starting Money is $2100 and a colorset is not needed to upgrade properties...Please enter each player's information: ")

token = []
color = []
name = []
for x in range(2):
    name.append(input("Player " + str(x + 1) + " name: "))
    token.append(input("Player " + str(x + 1) + " token: "))
    color.append(input("Player " + str(x + 1) + " color: "))

computer = player_profile(None, None, None, None, "Computer", True, False, 0)

loc0 = property_profile("Mediterranean Avenue", computer, 60, 4, "rental", 1, 30, "single", 10, 30, 90, 250, 100)
loc1 = property_profile("Community Chest 1", computer, 0, 6, "CC", 2, 0, None, None, None, None, None, None)
loc2 = property_profile("Baltic Avenue", computer, 60, 10, "rental", 3, 30, "single", 15, 35, 100, 260, 100)
loc3 = property_profile("Income Tax 1", computer, 0, 150, "Tax", 4, 0, None, None, None, None, None, None)
loc4 = property_profile("Reading Railroad", computer, 200, 30, "rr", 5, 25, "railroad", None, None, None, None, None)
loc5 = property_profile("Oriental Avenue", computer, 100, 35, "rental", 6, 50, "single", 40, 70, 110, 300, 125)
loc6 = property_profile("Chance 1", computer, 0, 0, "Chance", 7, 0, None, None, None, None, None, None)
loc7 = property_profile("Vermont Avenue", computer, 100, 35, "rental", 8, 50, "single", 40, 45, 120, 310, 125)
loc8 = property_profile("Connetticut Avenue", computer, 120, 35, "rental", 9, 60, "single", 40, 50, 125, 315, 125)
loc9 = property_profile("Jail", computer, 0, 0, "visit", 10, 0, None, None, None, None, None, None)
loc10 = property_profile("St. Charles Place", computer, 140, 40, "rental", 11, 70, "single", 50, 55, 130, 320, 150)
loc11 = property_profile("Electric Company", computer, 150, 50, "rental", 12, 50, "single", None, None, None, None, None)
loc12 = property_profile("States Avenue", computer, 140, 40, "rental", 13, 70, "single", 60, 60, 140, 330, 150)
loc13 = property_profile("Virginia Avenue", computer, 150, 40, "rental", 14, 70, "single", 60, 70, 150, 350, 150)
loc14 = property_profile("Pennyslvania Railroad", computer, 200, 30, "rr", 15, 25, "railroad", None, None, None, None, None)
loc15 = property_profile("St. James Place", computer, 180, 45, "rental", 16, 90, "single", 60, 75, 155, 355, 180)
loc16 = property_profile("Community Chest 2", computer, 0, 0, "CC", 17, 0, None, None, None, None, None, None)
loc17 = property_profile("Tennesee Avenue", computer, 180, 45, "rental", 18, 90, "single", 60, 80, 160, 360, 180)
loc18 = property_profile("New York Avenue", computer, 200, 45, "rental", 19, 90, "single", 65, 85, 165, 365, 180)
loc19 = property_profile("Free Parking", computer, 0, 0, "CC", 20, 0, None, None, None, None, None, None)
loc20 = property_profile("Kentucky Avenue", computer, 220, 50, "rental", 21, 110, "single", 70, 90, 170, 370, 200)
loc21 = property_profile("Chance 2", computer, 0, 0, "Chance", 22, 0, None, None, None, None, None, None)
loc22 = property_profile("Indiana Avenue", computer, 220, 50, "rental", 23, 110, "single", 80, 100, 180, 380, 200)
loc23 = property_profile("Illionois Avenue", computer, 240, 50, "rental", 24, 110, "single", 85, 105, 185, 390, 200)
loc24 = property_profile("B. & O. Railroad", computer, 200, 30, "rr", 25, 25, "railroad", None, None, None, None, None)
loc25 = property_profile("Atlantic Avenue", computer, 260, 55, "rental", 26, 130, "single", 95, 115, 195, 410, 250)
loc26 = property_profile("Ventnor Avenue", computer, 260, 55, "rental", 27, 130, "single", 100, 120, 200, 415, 250)
loc27 = property_profile("Water Works", computer, 150, 50, "rental", 28, 50, "single", None, None, None, None, None)
loc28 = property_profile("Marvin Gardens", computer, 280, 55, "rental", 29, 130, "single", 105, 125, 205, 420, 250)
loc29 = property_profile("Go To Jail", computer, 0, 0, "gtjail", 30, 0, None, None, None, None, None, None)
loc30 = property_profile("Pacific Avenue", computer, 300, 60, "rental", 31, 150, "single", 110, 130, 215, 430, 260)
loc31 = property_profile("North Carolina Avenue", computer, 300, 60, "rental", 32, 150, "single", 115, 135, 220, 450, 260)
loc32 = property_profile("Community Chest 3", computer, 0, 0, "CC", 33, 0, None, None, None, None, None, None)
loc33 = property_profile("Pennsylvania Avenue", computer, 320, 60, "rental", 34, 150, "single", 120, 140, 230, 470, 260)
loc34 = property_profile("Short Line Railroad", computer, 200, 30, "rr", 35, 25, "railroad", None, None, None, None, None)
loc35 = property_profile("Chance 3", computer, 0, 0, "Chance", 36, 0, None, None, None, None, None, None)
loc36 = property_profile("Park Place", computer, 350, 65, "rental", 37, 175, "single", 150, 170, 250, 490, 300)
loc37 = property_profile("Luxury Tax", computer, 0, 250, "Tax", 38, 0, "single", None, None, None, None, None)
loc38 = property_profile("Boardwalk", computer, 400, 65, "rental", 39, 175, "single", 175, 200, 280, 500, 300)
loc39 = property_profile("Go", computer, 100, 200, "Go", 0, 0, "single", None, None, None, None, None)

board = [loc39, loc0, loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8, loc9, loc10, loc11, loc12, loc13, loc14, loc15, loc16, loc17, loc18, loc19, loc20, loc21, loc22, loc23, loc24, loc25, loc26, loc27, loc28, loc29, loc30, loc31, loc32, loc33, loc34, loc35, loc36, loc37, loc38]
player1 = player_profile(color[0], token[0], starting_money, board[0], name[0], True, False, 0)
player2 = player_profile(color[1], token[1], starting_money, board[0], name[1], True, False, 0)
bid = thebid(computer, 50)

#___________Playing Process_________________________________
while playing == True:
    sij = False
    turn = 1
    if turn == 1:
        while True:
            if player1.injail == False or sij == True:
                if sij == True:
                    break
                prompt1 = input("________________________________________________________________\n" + player1.name + ", you are currently standing on " + player1.location.name + "... Press 'r' to roll... ")
                print("________________________________________________________________ ")
                roll_loc = move(player1.location.loc)
                for each in board:
                    if each.loc == roll_loc:
                        player1.location = board[roll_loc]
                        break
                if player1.location.type == "CC":
                    communitychest(player1)
                    endturn(player1)
                    turn +=1
                    break
                elif player1.location.type == "Chance":
                    chancecard(player1, player2)
                    endturn(player1)
                    turn +=1
                    break
                elif player1.location.type == "visit":
                    print("Your are just visiting jail")
                    endturn(player1)
                    turn +=1
                    break
                elif player1.location.type == "gtjail":
                    print("You must go to jail")
                    player1.location = board[10]
                    player1.injail = True
                elif player1.location.type == "Tax":
                    print("Your need to pay your taxes...Pay 250!")
                    player1.money -= player1.location.rent
                    endturn(player1)
                    turn +=1
                    break
                elif player1.location.type == "Go":
                    print("Your just passed Go... Collect 200 dollars")
                    player1.money += 200
                    endturn(player1)
                    turn += 1
                    break
                elif (player1.location.type == "rental" or player1.location.type == "rr") and player1.location.owner == computer:
                    prompt2 = input("You just landed on " + str(player1.location.name) + " for $" + str(player1.location.price) + ". Press 'b' to buy or anything to auction...... ")
                    if prompt2 == "b":
                        buy(player1)
                        endturn(player1)
                        turn += 1
                        break
                    else:
                        auction(player1, player2, player2.money, player1.money, player1.location, bid)
                        endturn(player1)
                        turn += 1
                        break
                elif (player1.location.type == "rental" or player1.location.type == "rr") and player1.location.owner == player2:
                    rent_due = player1.location.findrent()
                    player1.money -= rent_due
                    player2.money += rent_due
                    print("You just landed on Player 2's Property: " + str(player1.location.name) + " You paid them " + str(rent_due))
                    endturn(player1)
                    turn +=1
                    break
            else:
                print("________________________________________________________________ ")
                player1.location = board[10]
                print("Attempts Left: " + str(player1.jailattempts) + ", Current Balance: " + str(player1.money) + ", Number of Jail Cards: " + str(player1.jailcard))
                while True:
                    inp = input("You are currently in jail...Pay $150, use a jailcard or roll a double to leave - press 'p' to pay, 'j' to use your get out of jailcard, 'r' to roll... ")
                    if inp == "p":
                        if player1.money >= 150:
                            print("You are now out of jail")
                            player1.injail = False
                            player1.money -= 150
                            turn = 1
                            break
                        else:
                            s = input("You don't have enough money, you can either roll or mortgage. Press 'm' to mortgage or 'e' to go back")
                            if s == "m":
                                mortgage(player1)
                    elif inp == "r":
                        if player1.jailattempts == 0:
                            print("You have no more attempts left, you must pay to leave")
                            if player1.money >= 150:
                                player1.injail = False
                                player1.money -= 150
                                player1.jailattempts = 3
                                turn = 1
                                print("________________________________________________________________ ")
                                print("You are out of jail now")
                                print("________________________________________________________________ ")
                                break
                            else:
                                print("You must mortgage your properties to gather enough money...If you don't then you will automatically be bankrputed")
                                mortgage(player1)
                                if player1.money < 150:
                                    bankrupt(player1)
                        elif player1.jailattempts > 0:
                            result = roll()
                            if result == True:
                                print("________________________________________________________________ ")
                                print("You are out of jail now")
                                print("________________________________________________________________ ")
                                player1.injail = False
                                player1.jailattempts = 3
                                turn = 1
                                break
                            else:
                                print("________________________________________________________________ ")
                                print(player1.name + ", you are still in jail")
                                print("________________________________________________________________ ")
                                player1.jailattempts -= 1
                                turn = 2
                                sij = True
                                endturn(player1)
                                break
                    elif inp == "j":
                        if player1.jailcard > 0:
                            print("________________________________________________________________ ")
                            print("You just used a jailcard to get out of jail")
                            print("________________________________________________________________ ")
                            player1.injail = False
                            player1.jailattempts = 3
                            turn = 1
                            player1.jailcard -= 1
                            break
                        else:
                            print("You do not have a jailcard")
                    else:
                        print("Please enter a valid input")
    if turn == 2:
        while True:
            if player2.injail == False or sij == True:
                if sij == True:
                    break
                prompt1 = input("________________________________________________________________\n" + player2.name + ", you are currently standing on " + player2.location.name + "... Press 'r' to roll... ")
                print("________________________________________________________________ ")
                roll_loc = move(player2.location.loc)
                for each in board:
                    if each.loc == roll_loc:
                        player2.location = board[roll_loc]
                        break
                if player2.location.type == "CC":
                    communitychest(player2)
                    endturn(player2)
                    turn +=1
                    break
                elif player2.location.type == "Chance":
                    chancecard(player2, player1)
                    endturn(player2)
                    turn +=1
                    break
                elif player2.location.type == "visit":
                    print("Your are just visiting jail")
                    endturn(player2)
                    turn +=1
                    break
                elif player2.location.type == "gtjail":
                    print("You must go to jail")
                    player2.location = board[10]
                    player2.injail = True
                elif player2.location.type == "Tax":
                    print("Your need to pay your taxes...Pay 250!")
                    player2.money -= player2.location.findrent()
                    endturn(player2)
                    turn +=1
                    break
                elif player2.location.type == "Go":
                    print("Your just passed Go... Collect 200 dollars")
                    player2.money += 200
                    endturn(player2)
                    turn += 1
                    break
                elif (player2.location.type == "rental" or player2.location.type == "rr") and player2.location.owner == computer:
                    prompt2 = input("You just landed on " + str(player2.location.name) + " for $" + str(player2.location.price) + ". Press 'b' to buy or anything to auction...... ")
                    if prompt2 == "b":
                        buy(player2)
                        endturn(player2)
                        turn += 1
                        break
                    else:
                        auction(player2, player1, player1.money, player2.money, player2.location, bid)
                        endturn(player2)
                        turn += 1
                        break
                elif (player2.location.type == "rental" or player2.location.type == "rr") and player2.location.owner == player1:
                    rent_due = player2.location.findrent()
                    player2.money -= rent_due
                    player1.money += rent_due
                    print("You just landed on Player 1's Property: " + str(player2.location.name) + " You paid them " + str(rent_due))
                    endturn(player2)
                    turn +=1
                    break
            else:
                print("________________________________________________________________ ")
                player2.location = board[10]
                print("Attempts Left: " + str(player2.jailattempts) + ", Current Balance: " + str(player2.money) + ", Number of Jail Cards: " + str(player2.jailcard))
                while True:
                    inp = input("You are currently in jail...Pay $150, use a jailcard or roll a double to leave - press 'p' to pay, 'j' to use your get out of jailcard, 'r' to roll... ")
                    if inp == "p":
                        if player2.money >= 150:
                            print("You are now out of jail")
                            player2.injail = False
                            player2.money -= 150
                            turn = 1
                            break
                        else:
                            s = input("You don't have enough money, you can either roll or mortgage. Press 'm' to mortgage or 'e' to go back")
                            if s == "m":
                                mortgage(player2)
                    elif inp == "r":
                        if player2.jailattempts == 0:
                            print("You have no more attempts left, you must pay to leave")
                            if player2.money >= 150:
                                player2.injail = False
                                player2.money -= 150
                                player2.jailattempts = 3
                                turn = 1
                                print("________________________________________________________________ ")
                                print("You are out of jail now")
                                print("________________________________________________________________ ")
                                break
                            else:
                                print("You must mortgage your properties to gather enough money...If you don't then you will automatically be bankrputed")
                                mortgage(player2)
                                if player2.money < 150:
                                    bankrupt(player2)
                        elif player2.jailattempts > 0:
                            result = roll()
                            if result == True:
                                print("________________________________________________________________ ")
                                print("You are out of jail now")
                                print("________________________________________________________________ ")
                                player2.injail = False
                                player2.jailattempts = 3
                                turn = 1
                                break
                            else:
                                print("________________________________________________________________ ")
                                print(player2.name + ", you are still in jail")
                                print("________________________________________________________________ ")
                                player2.jailattempts -= 1
                                turn = 2
                                sij = True
                                endturn(player2)
                                break
                    elif inp == "j":
                        if player2.jailcard > 0:
                            print("________________________________________________________________ ")
                            print("You just used a jailcard to get out of jail")
                            print("________________________________________________________________ ")
                            player2.injail = False
                            player2.jailattempts = 3
                            turn = 1
                            player2.jailcard -= 1
                            break
                        else:
                            print("You do not have a jailcard")
                    else:
                        print("Please enter a valid input")
