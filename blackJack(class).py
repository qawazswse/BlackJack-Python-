import random


class AllPlayer:
    """
    Players have cards, and their own score of the cards they have.
    """
    def __init__(self, name):
        self.cards = []
        self.score = 0
        self.name = name

    def draw(self, card):
        """
        This is how players draw cards
        :param card: the card the player draws
        :return: nothing
        """
        self.cards.append(card)
        self.calculate(card)

    def calculate(self, card):
        """
        this is how to calculate the player's score.
        :param card: the card the player draws
        :return: nothing
        """
        card = card[1:]
        if card in [str(i) for i in range(11)]:
            self.score += int(card)
        elif card in 'JQK':
            self.score += 10
        else:
            self.score += 11
            for a in ''.join(self.cards):
                if a == 'A' and self.score > 21:
                    self.score -= 10

    def bust(self):
        """
        judge if the player bust or not
        :return: a Boolean value
        """
        if self.score > 21:
            print(f"{self.name} cards BUST!!!!!")
            return True
        return False


class Game:
    """
    The game, 'process()' is the main function defines how the game is processed
    """
    cards = []  # The pokers in the game.
    dealer = AllPlayer('')  # An instant of AllPlayer, this is a dealer.
    player = AllPlayer('')  # An instant of AllPlayer, this is a player.
    keep_draw = False   # Judge if the player choose to keep drawing cards or not.

    def __init__(self):
        self.wash()
        print("""Rules:
    - 1 player game\n    - player vs dealer\n    - Goal: get as close to 21 as possible\n    - over 21 is a BUST
    - face card values = 10\n    - Ace is 11 or 1, player decides\n    - other cards are just the value they have
    - player says hit, player gets one more card\n    - player says stand, dealer's turn
    - player goes first, first round, dealer gives player card
    - dealer also gives card to self, face up (player and dealer can see)
    - second round player goes and dealer gets card face down (unknown to all)\n    - dealer's turn:
        - turn over face down card\n            - if total is over 17, dealer stands
            - if total is 16 or less, dealer hits until at least 17 then stand
            - if one of the first 2 cards is an Ace:
                - if making it 11 makes gets between 17 and 21 then make 11, otherwise make it a 1 (to not go over)
    - at the end compare, everything is in favor of dealer:
        - if player busts, player loses, no need to compare or have dealer's turn
        - if dealer busts and player did not, player wins\n        - if dealer == player, dealer wins
        - if player is closer to 21 than dealer, player wins""")

    def game(self):
        """
        This exists for players to continue to play a new turn.
        :return: nothing
        """
        self.process()
        self.end_of_game()

    def process(self):
        """
        This is the main process of the game.
        :return: a Boolean value to tell win or lose.
        """
        self.draw(self.player)
        self.draw(self.dealer)
        self.keep_draw = self.hit_or_stand()
        if self.keep_draw:
            self.draw(self.player)
            if self.player.score == 21:
                print('You Win!')
                return True
        else:
            self.unseen_draw(self.dealer)
        print('Dealer draws another card')
        if self.keep_draw:
            while self.hit_or_stand():
                self.draw(self.player)
                if self.player.bust():
                    print('You Lose!')
                    return False
            print("Now, dealer's turn")
        print('Dealer has: ', ', '.join(self.dealer.cards))
        while not self.dealer.bust() and self.dealer.score < 17 and self.dealer.score < self.player.score:
            self.draw(self.dealer)
        if 21 >= self.dealer.score >= self.player.score:
            print('You Lose!')
            return False
        else:
            print('You Win!')
            return True

    def hit_or_stand(self):
        """
            Let player to choose Hit or Stand
            :return: a Boolean Value
        """
        if self.keep_draw:
            print(f'Now dealers card is {self.dealer.cards[0]} and another')
        else:
            print(f'Now dealers card is {self.dealer.cards[0]}')
        answer = input('"Hit" or "Stand" ? \n')
        if answer in {'Hit', 'hit', 'H', 'h'}:
            return True
        elif answer in {'Stand', 'stand', 'S', 's'}:
            return False
        else:
            print('input "Hit" or "Stand" please')
            return self.hit_or_stand()

    def draw(self, any_player):
        """
        This is how player and dealer draw a card.
        :param any_player: an instant of AllPlayer class.
        :return: nothing
        """
        any_player.draw(self.cards[-1])
        print(f'{any_player.name} draw: ', self.cards[-1])
        print(f'{any_player.name} cards: ', ', '.join(any_player.cards), ' score: ', any_player.score)
        self.cards.pop()

    def unseen_draw(self, any_player):
        """
        This is how dealer draw first two cards.
        :param any_player: an instant of AllPlayer class.
        :return: nothing
        """
        any_player.draw(self.cards[-1])
        print(f'{any_player.name} draw another card ')
        self.cards.pop()

    def wash(self):
        """
        this is how we wash cards for next turn, both player and dealer's cards have to be return back.
        :return: nothing
        """
        self.cards = [c + i for i in [str(num) for num in range(2, 11)]+['A', 'J', 'Q', 'K'] for c in '♦♥♠♣']
        random.shuffle(self.cards)
        self.player.__init__('Your')
        self.dealer.__init__("Dealer's")

    def end_of_game(self):
        """
        this function is used to let player to choose if he wanna play another time or quit.
        :return: nothing
        """
        answer = input('wanna play again? Y/N \n')
        if answer in 'Yy':
            self.wash()
            self.game()
        elif answer in 'Nn':
            print('Thank you for your time!')
        else:
            print("input 'Y' or 'N' please")
            self.end_of_game()


if __name__ == '__main__':
    game1 = Game()
    game1.game()
