import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True # used for the while loop
playerBust = False #used for player bust check
dealerBust = False #used for dealer bust check
winValue = -1 #0 for player win / 1 for dealer win
playAgain = True

class Card:

    def __init__(self,suit,rank):

        self.suit = suit
        self.rank = rank

    def __str__(self):

        return(f'{self.rank} of {self.suit}')

class Deck:

    def __init__(self):

        self.deck = []

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand:

    def __init__(self):

        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)

        if card.rank == 'Ace':
            self.aces += 1

        self.value += values[card.rank] #valoarea cartii adaugate
    
    def adjust_for_ace(self):
        #verific daca value e mai mare ca 11 si daca valuarea ultimei carti adaugate e 11 adica e as
        if self.value > 11 and self.cards[-1].rank == 'Ace':
            self.value -= 10


class Chips:
    
    def __init__(self,bet):

        self.total = 100
        self.bet = bet
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

#ask user for bet
def take_bet():

    while True:
        try:
            return int(input('How much would you like to bet?'))
        except:
            print('ERROR: Please input an integer')

def hit(deck,hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace() 

def hit_or_stand(deck,hand):

    global playing 

    while True:

        hit1 = input('Do you want to hit? y or n: ')
            
        if hit1 == 'y':

            hit(deck,hand)
            break

        elif hit1 == 'n':

            playing = False
            break

        else:

            print('please input y or n')


#va arata toate cartile atat pt dealer cat si pt player
def show_all(player,dealer):

    print('Player cards: ')

    for i in range(len(player.cards)):

            print(f'{player.cards[i]}')
    
    print(f'{player.value}')
    print('\n')

    print('Dealer cards: ')

    for i in range(len(dealer.cards)):
        
            print(f'{dealer.cards[i]}')

    print(f'{dealer.value}')

#nu va arata prima carte a dealerului
def show_some(player,dealer):

    print('Player cards: \n')

    for i in range(len(player.cards)):

        print(f'{player.cards[i]}')

    print(f'{player.value}')
    print('\n')

    print('Dealer cards: \n')

    for i in range(len(dealer.cards)):

        if i == len(dealer.cards) - 1:
                break

        print(f'{dealer.cards[i + 1]}')

    print('\n')

def player_busts(player):

        global winValue

        winValue = 1

        print('Player busts with {} \n'.format(player.value))


def dealer_busts(dealer):

    global dealerBust
    global winValue

    if dealer.value > 21:

        dealerBust = True
        winValue = 0
        print('Dealer busts with {} '.format(dealer.value))

def player_wins(player,dealer):

    global winValue

    if player.value > dealer.value and playerBust == False:

        winValue = 0

        print('Player wins with {} over {}'.format(player.value, dealer.value))
  
def dealer_wins(player,dealer):
    
    global winValue

    if dealer.value >= player.value and dealerBust == False:

        winValue = 1

        print('Dealer wins with {} over {}'.format(dealer.value, player.value))
    
def play_scenarios(player,dealer):
    dealer_busts(dealer)
    player_wins(player,dealer)
    dealer_wins(player,dealer)

def play_again():

    global playAgain

    while True:

        again = input('Would you like to play again, y or n ?')

        if again == 'y':
            break
        elif again == 'n':
            playAgain = False
            break
        else:
            print('Please input y or n')

print('Welcome to my BlackJack game, your starting sum is 100$')

while True:

    # playAgain = True
    # playing = True
    #creez un deck si il amestec
    deck = Deck()
    deck.shuffle()

    #creez mainile si impart 2 carti
    player = Hand()
    dealer = Hand()

    hit(deck,player)
    hit(deck,player)

    hit(deck,dealer)
    hit(deck,dealer)

    #iau bet-ul player-ului
    playerBet = take_bet()
    chips = Chips(playerBet)

    #arat cartile , dealer-ul va avea prima carte face-down
    show_some(player,dealer)

    while playing:

        #if not wanna hit => break
        hit_or_stand(deck,player)

        if playing == True:#showing cards each step
            show_some(player,dealer)

        #if bust break
        if player.value > 21:

            player_busts(player)
            playerBust = True
            break

        else:#hit dealer
            if dealer.value < 17:
                hit(deck,dealer)

    if playerBust == False: #executed only if player does not bust
        show_all(player,dealer)

    #play winning scenarios
    play_scenarios(player,dealer)

    if winValue == 0:
        chips.win_bet()
    elif winValue == 1:
        chips.lose_bet()
    else:
        pass

    print('Your total is {}$'.format(chips.total))

    play_again()

    if playAgain == False:
        break
    else:
        pass

