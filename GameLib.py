from random import randint, choice, shuffle
from time import sleep

J = 11
Q = 12
K = 13
A = 14

class Card:
	name = None
	color = None
	number = None
	value = None

	def __init__(self, name, color, number):
		self.name = name
		self.color = color
		self.number = number

		if number == A or number == J:
			self.value = 1

		elif name == "Sinek 2":
			self.value = 2

		elif name == "Karo 10":
			self.value = 3

		else:
			self.value = 0

class Deck:
	cards = []

	def __init__(self):
		# adding numbered cards
		for i in range(2,11):
			self.cards.append(Card(f"Kupa {i}", "Kupa", i))
			self.cards.append(Card(f"Maça {i}", "Maça", i))
			self.cards.append(Card(f"Karo {i}", "Karo", i))
			self.cards.append(Card(f"Sinek {i}", "Sinek", i))

		# adding the rest
		for _color in ["Kupa", "Maça", "Karo", "Sinek"]:
			self.cards.append(Card(f"{_color} Valesi", _color, J))
			self.cards.append(Card(f"{_color} Kızı", _color, Q))
			self.cards.append(Card(f"{_color} Papazı", _color, K))
			self.cards.append(Card(f"{_color} As", _color, A))

		shuffle(self.cards)

	def give_card(self):
		card = self.cards[-1]
		self.cards.pop()
		return card

	def give_4_cards(self):
		return [self.give_card() for i in range(4)]

class Table:
	card_on_top = None
	pile = []

	# for string
	def get_card_on_top(self):
		if self.card_on_top is None:
			return "boş"

		else:
			return self.card_on_top.name

	def place_card(self, card):
		self.pile.append(card)
		self.card_on_top = card

	def refresh(self):
		self.card_on_top = None
		self.pile = []

class Player:
	name = None
	pisti_count = 0
	j_pisti_count = 0
	point = 0
	hand = []
	collected_cards = []

	def __init__(self, name):
		self.name = name

	def give_new_hand(self, pile):
		self.hand = [card for card in pile]

	def collect_cards(self, pile):
		for card in pile:
			self.collected_cards.append(card)

class Bot(Player):
	level = None
	NumberCounts = {}

	def __init__(self, name, level):
		super().__init__(name)
		self.level = level

		if level >= 3:
			for i in range(2, 11):
				self.NumberCounts.update({i:0})
			self.NumberCounts.update({J:0})
			self.NumberCounts.update({Q:0})
			self.NumberCounts.update({K:0})
			self.NumberCounts.update({A:0})

	def choose_card(self, card_on_top):
		if self.level == 1:

			# check for matching number
			for card in self.hand:
				if card.number == card_on_top.number:
					return card

			# if no -> random
			return choice(self.hand)

		elif self.level == 2:

			# check for matching number
			for card in self.hand:
				if card.number == card_on_top.number:
					return card

			# valuable card and -> jack
			if card_on_top.name in ["Karo 10", "Sinek 2", "Kupa As", \
			"Maça As", "Karo As", "Sinek As"]:
				print("Valuable card!\n")
				for card in self.hand:
					if card.number == J:
						return card

			# otherwise save the jack(s)
			selectable_cards = []
			for card in self.hand:
				if card.number != J:
					selectable_cards.append(card)

			if len(selectable_cards) > 0:
				return choice(selectable_cards)

			else:
				return choice(self.hand)

		elif self.level == 3:
			# check for matching number
			for card in self.hand:
				if card.number == card_on_top.number:
					return card

			# valuable card and -> jack
			if card_on_top.name in ["Karo 10", "Sinek 2", "Kupa As", \
			"Maça As", "Karo As", "Sinek As"]:
				print("Valuable card!\n")
				for card in self.hand:
					if card.number == J:
						return card

			# otherwise save the jack(s) & go with statistics
			selectable_cards = []
			for card in self.hand:
				if card.number != J:
					selectable_cards.append(card)

			if len(selectable_cards) > 0:
				print(self.NumberCounts)
				selectable_cards.sort(key = lambda x: self.NumberCounts[x.number], reverse=True)
				return selectable_cards[0]

			else:
				return choice(self.hand)

	def update_counting(self, card):
		if self.NumberCounts[card.number] < 4:
			self.NumberCounts[card.number] += 1

		else:
			print("!! ERROR: CARD COUNT CANNOT BE GREATER THAN 4")
			exit()

"""
HAND1 = [Card("Karo 2", "Karo", 2), Card("Karo 3", "Karo", 3),Card("Karo 4", "Karo", 4),Card("Karo Valesi", "Karo", J)]
CARD1 = Card("Karo 10", "Karo", 10)
HAND2 = [Card("Karo 2", "Karo", 2), Card("Karo 3", "Karo", 3),Card("Karo 4", "Karo", 4),Card("Karo Valesi", "Karo", J)]
HAND3 = [Card("Karo 2", "Karo", 2), Card("Karo 3", "Karo", 3),Card("Karo 4", "Karo", 4),Card("Karo 5", "Karo", 5)]
statistics = {2:1, 3:2, 4:1, 5:0}

bot = Bot("PC", 3)
bot.give_new_hand(HAND3)
bot.NumberCounts.update(statistics)
print([card.name for card in HAND3])
print(bot.choose_card(CARD1).name)
"""

class GameController:
	player1 = None
	player2 = None
	
	def get_choice(minn, maxx, text="Atılacak kart: "):
		c = input(text)
		print("")

		try:
			c = int(c)

		except ValueError:
			print("!! Sayı giriniz")
			c = get_choice(minn, maxx)

		else:
			if c < minn or c > maxx:
				print(f"!! Geçerli aralıkta bir sayı giriniz: {minn}-{maxx}")
				c = get_choice(minn, maxx)
		
		finally:
			return c

