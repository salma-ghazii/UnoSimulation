import random
class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number
  
class Player:
    def __init__(self, name):
        self.name = name
        self.cards = [] 

def legal(card, curr):
    if card==None:
        return None
    return (card.color == curr.color) or (card.number == curr.number) or curr.color == "wild" or card.color == "wild"

def checkWinner(players):
    winner = 0
    for player in players:
            if len(player.cards) == 0:
                winner = player.name
                break
    return winner

def switchTurn(reverse, skip, turn):
    if reverse: 
        if skip:
            match turn:
                case 0:
                    turn = 2
                case 1:
                    turn = 3
                case 2 | 3:
                    turn -= 2
        else:
            if turn > 0:
                turn -= 1
            else:
                turn = 3
    else:
        if skip:
                match turn:
                    case 2:
                        turn = 0
                    case 3:
                        turn = 1
                    case 0 | 1:
                        turn += 2
        else:
            if turn < 3:
                turn+=1
            else:
                turn = 0
    return turn

def randomLegal(player, curr):
    global cards
    tries = 1
    card = player.cards.pop()
    draw = False
    while not legal(card, curr):
        if tries >= len(player.cards):
            player.cards.insert(0, card)
            draw = True
            break
        player.cards.insert(0, card)
        card = player.cards.pop()
        if len(cards) == 0:
            cards = create_deck()
        tries+=1
    if draw:
        return None
    else:
        return card
    

def mostColor(player):
    colors = [0, 0, 0, 0, 0]
    for c in player.cards:
        match c.color:
            case "blue":
                colors[0]+=1
            case "red":
                colors[1]+=1
            case "yellow":
                colors[2]+=1
            case "green":
                colors[3]+=1
            case "wild":
                colors[4]+=1
    match colors.index(max(colors)):
            case 0:
                return "blue"
            case 1:
                return "red"
            case 2:
                return "yellow"
            case 3:
                return "green"
            case 4:
                return "wild"
        
def mostNumber(player):
    numbers=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+2", "skip", "reverse", "wild", "+4 wild"]
    count=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for c in player.cards:
        count[numbers.index(c.number)]+=1
    return numbers[count.index(max(count))]




#player strats
#play by color- play1
#play by number- play2 
#save special for last- play3
#random legal- play4
def play(player, curr):
    special = ["+2", "skip", "reverse", "wild", "+4 wild"]
    draw = False
    hand = player.cards
    card = None
    match player.name:
        case "player1":
            for c in hand:
                if c.color == curr.color and legal(c, curr):
                    player.cards.remove(c)
                    card = c
                    break
            if card == None:
                card = randomLegal(player, curr)
            if card == None:
                return True, None
        case "player2":
            for c in hand:
                if c.number == curr.number and legal(c, curr):
                    player.cards.remove(c)
                    card = c
                    break
            if card == None:
                card = randomLegal(player, curr)
            if card == None:
                return True, None
        case "player3":
            for c in hand:
                if c.number not in special:
                    if c.number == curr.number or c.color == curr.color:
                        player.cards.remove(c)
                        card = c
                        break
            if card == None:
                card = randomLegal(player, curr)
            if card == None:
                return True, None
        case "player4":
            card = randomLegal(player, curr)
            if card == None:
                return True, None
            
    return False, card


#player strats
#play by color in hand most - play1
#play by number number in hand most - play2 
#save special for last- play3
#random legal- play4
    
def play2(player, curr):
    special = ["+2", "skip", "reverse", "wild", "+4 wild"]
    draw = False
    hand = player.cards
    card = None
    match player.name:
        case "player1":
            color = mostColor(player)
            for c in hand:
                if c.color == color and legal (c, curr):
                    player.cards.remove(c)
                    card = c
                    break
            if card == None:
                card = randomLegal(player, curr)
            # print(f'card is {card.number} {card.color}')
            if card == None:
                return True, None
        case "player2":
            number = mostNumber(player)
            for c in hand:
                if c.number == number and legal (c, curr):
                    player.cards.remove(c)
                    card = c
                    break
            if card == None:
                card = randomLegal(player, curr)
            # print(f'card is {card.number} {card.color}')
            if card == None:
                return True, None
        case "player3":
            # for c in hand:
            #     if c.number not in special:
            #         if c.number == curr.number or c.color == curr.color:
            #             player.cards.remove(c)
            #             card = c
            #             break
            # if card == None:
            #     card = randomLegal(player, curr)
            # if card == None:
            #     return True, None
            card = randomLegal(player, curr)
            if card == None:
                return True, None
            
            
        case "player4":
            card = randomLegal(player, curr)
            if card == None:
                return True, None
            
    return False, card

#play function used to make random moves for all the players (25% win rate for each player)
def play3(player, curr):
    draw = False
    hand = player.cards
    card = None
    card = randomLegal(player, curr)
    if card == None:
        return True, None
    
    return False, card
            


def create_deck():
    global cards
    cards = []
    colors=["blue", "red", "yellow", "green"] 
    numbers=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+2", "skip", "reverse"] #excludes wild cards
    special = ["wild", "skip", "reverse", "+2", "+4 wild"]
    for color in colors:
        for number in numbers:
            for i in range(2):
                cards.append(Card(color, number))
    for i in range(4):
        cards.append(Card("wild", "+4 wild"))
        cards.append(Card("wild", "wild"))
    return cards

def printCards(player):
    for card in player.cards:
        print(card.color, card.number)


def run_game():
    #create deck
    cards = create_deck()

    #create players
    player1 = Player("player1")
    player2 = Player("player2")
    player3 = Player("player3")
    player4 = Player("player4")
    players = [player1, player2, player3, player4]
    random.shuffle(cards)
    for i in range(7):
        for player in players:
            player.cards.append(cards.pop())
            if len(cards) == 0:
                    cards = create_deck()

    #set games variables
    winner = None
    turn = pull = 0
    curr = cards.pop()
    if len(cards) == 0:
        cards = create_deck()
    reverse = plusTwo = plusFour = False

    #main game loop
    while winner==None:
        if len(cards)==0:
            cards = create_deck()
        skip = False

        #check for winner
        if checkWinner(players):
            return checkWinner(players)
        player = players[turn]

        #draw from special cards if prev. player
        if plusTwo:
            # print("pull count is: " + str(pull))
            for card in player.cards:
                if card.number == "+2":
                    player.cards.remove(card)
                    pull+=2
                    break
            for i in range(pull):
                player.cards.append(cards.pop())
                if len(cards) == 0:
                    cards = create_deck()
            plusTwo = False
            pull=0
            continue

        if plusFour:
            for card in player.cards:
                if card.number == "+4 wild":
                    player.cards.remove(card)
                    pull+=4
                    break
            for i in range(pull):
                player.cards.append(cards.pop())
                if len(cards) == 0:
                    cards = create_deck()
            plusFour = False
            pull=0
            continue

        # card = player.cards.pop()
        if len(cards) == 0:
            cards = create_deck()
        draw = False

        #print game state (hand of current player)
        # print("current cards of " + player.name)
        # printCards(player)

        draw, card = play2(player, curr)
        
        # print current game state (current card counts and draw/played card)
        # print("Current card is " + curr.color + " " + curr.number)
        # if not draw:
        #     print(player.name + " put down a " + card.color + " " + card.number)
        # else:
        #     print(player.name + " drew a card")
        # print("Current card counts: ")
        # for p in players:
        #     print(p.name + ": " + str(len(p.cards)))


        if checkWinner(players):
            return checkWinner(players)
        if draw:
            player.cards.append(cards.pop())

        #special cards
        if not draw:
            if card.number == "reverse":
                reverse = not reverse
            if card.number == "skip":
                skip  = True
            if card.number == "+2":
                plusTwo = True
                pull+=2
            if card.number == "+4 wild":
                plusFour = True
                pull+=4
            curr = card
        #switch to next player
        turn = switchTurn(reverse, skip, turn)

    return winner.name


# run simulation 10,000 times and print win rate of each player
one = two = three = four = 0
n=10000
for i in range(n):
    win = run_game()   
    match win:
        case "player1":
            one+=1
        case "player2":
            two+=1
        case "player3":
            three+=1
        case "player4":
            four+=1

print("player1:{}  player2:{}  player3:{}  player4:{}  ".format(one/n, two/n , three/n, four/n))

# print(run_game())
