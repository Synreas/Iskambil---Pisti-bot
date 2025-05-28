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

		while self.cards[-4].number == J:
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

	def __init__(self, name="Sen"):
		self.name = name

	def give_new_hand(self, pile):
		self.hand = [card for card in pile]

	def collect_cards(self, pile):
		for card in pile:
			self.collected_cards.append(card)

class Bot(Player):
	level = None
	NumberCounts = {}

	def __init__(self, name="Bilgisayar", level=2):
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
		if card_on_top is None:
			card_on_top = Card("X", "X", 0)

		# check for matching number
		for card in self.hand:
			if card.number == card_on_top.number:
				return card

		# no matching numbers		
		if self.level == 1:
			# choose a random card
			return choice(self.hand)

		else:
			# valuable card and -> jack
			if card_on_top.value > 0:
				print("Valuable card!\n")
				for card in self.hand:
					if card.number == J:
						return card

			# otherwise save the jack(s)
			selectable_cards = []
			for card in self.hand:
				if card.number != J:
					selectable_cards.append(card)

			if self.level == 2:
				# choose a random card	
				if len(selectable_cards) > 0:
					return choice(selectable_cards)

				else:
					return choice(self.hand)
			else:
				# choose based on the statistics
				if len(selectable_cards) > 0:
					for card in range(2,15):
						"""
						if self.NumberCounts[card]>0:
							print(card,"->",self.NumberCounts[card], \
								"*" if card in [x.number for x \
								in self.hand] else "")
						"""
					selectable_cards.sort(\
						key = lambda x: self.NumberCounts[x.number],reverse=True)

					# highest count ->  choose
					if self.level == 3:
						return selectable_cards[0]

					else:
						# except for Aces and valuable cards
						if len(selectable_cards) > 2 and \
						selectable_cards[0].value > 0:
							i = 1
							# card value is more important than frequency
							while i < len(selectable_cards):
								if self.NumberCounts[selectable_cards[i].number]\
								>=self.NumberCounts[selectable_cards[0].number]-1\
								and selectable_cards[i].value <= \
								selectable_cards[0].value:
									return selectable_cards[i]
								i += 1
						else:
							return selectable_cards[0]

				else:
					return choice(self.hand)

	def update_counting(self, card):
		if self.level < 3:
			return 0
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
statistics = {2:4, 3:2, 4:1, 5:3}

bot = Bot("PC", 2)
bot.give_new_hand(HAND2)
bot.NumberCounts.update(statistics)
print([card.name for card in HAND2])
print(bot.choose_card(CARD1).name)
"""

class GameController:
	t = None
	t_calc = None
	player = None
	bot = None
	table = None
	deck = None
	
	def __init__(self, t_const=0.5, t_calc=2):
		self.t = t_const
		self.t_calc = t_calc

	def get_choice(self, minn, maxx, text="Atılacak kart: "):
		c = input(text)
		if c in ["exit", "-exit", "--exit"]:
			exit()
		print("")

		try:
			c = int(c)

		except:
			print("!! Sayı giriniz")
			c = self.get_choice(minn, maxx, text)

		else:
			if c < minn or c > maxx:
				print(f"!! Geçerli aralıkta bir sayı giriniz: {minn}-{maxx}")
				c = self.get_choice(minn, maxx, text)
		
		finally:
			return c

	def set_table(self, text="Kartlar dağıtılıyor..."):
		self.table = Table()
		self.deck = Deck()

		for card in self.deck.give_4_cards():
			self.table.place_card(card)

		if self.table.get_card_on_top() != "boş":
			self.bot.update_counting(self.table.card_on_top)

		print(text,"\n")
		sleep(self.t)

	def set_player(self):
		name = input("Adın: ")
		if name.isspace():
			name = "Sen"
		self.player = Player(name)

	def set_bot(self):
		level = self.get_choice(1, 4, f"Zorluk seviyesini seçiniz (1-4): ")
		self.bot = Bot("Bilgisayar", level)

	def print_table(self):
		print("Ortadaki kart:", self.table.get_card_on_top(), "\n")
		sleep(self.t)

	def print_player_hand(self):
		print("Elindeki kartlar")
		print("----------------")

		for i in range(len(self.player.hand)):
			print(f"{i+1} -> {self.player.hand[i].name}")

		print("")

	def compare_card(self, card):
		# (win, pisti, j_pisti)
		win=False
		pisti=False
		j_pisti=False

		if len(self.table.pile) == 0:
			return (win,pisti,j_pisti)

		# checking pisti conditions
		if len(self.table.pile) == 1:
			if card.number == J:
				win=True
				if self.table.card_on_top.number == J:
					j_pisti=True
			elif card.number == self.table.card_on_top.number:
				win=True
				pisti=True

		elif card.number == J or card.number == self.table.card_on_top.number:
			win=True

		return (win, pisti, j_pisti)

	def play_a_tour(self):
		self.print_table()
		self.print_player_hand()

		# player's tours
		chosen_card = self.player.hand[self.get_choice(1,4) - 1]
		print(f"{self.player.name} ortaya {chosen_card.name} attı")
		self.bot.update_counting(chosen_card)

		results = self.compare_card(chosen_card)
		self.table.place_card(chosen_card)
		if results[0]: # win the round
			print("Ortadakileri aldın!")
			sleep(self.t)
			# first count pisti
			if results[1]: # 1 pisti
				self.player.pisti_count += 1
				print("Pişti!!")

			elif results[2]: # 1 j_pisti
				self.player.j_pisti_count += 1
				print("VALE PİŞTİSİ !!!")

			# then arrange the table
			self.player.collect_cards(self.table.pile)
			self.table.refresh()

		self.player.hand.remove(chosen_card)

		# bot's tour
		chosen_card = self.bot.choose_card(self.table.card_on_top)
		print(f"{self.bot.name} ortaya {chosen_card.name} attı", "\n")

		results = self.compare_card(chosen_card)
		self.table.place_card(chosen_card)

		if results[0]: # win the round
			print(f"{self.bot.name} ortadakileri aldı.")
			# first count pisti
			if results[1]: # 1 pisti
				print("Pişti!!")
				self.bot.pisti_count += 1

			elif results[2]: # 1 j_pisti
				print("VALE PİŞTİSİ !!!")
				self.bot.j_pisti_count += 1

			# then arrange the table
			self.bot.collect_cards(self.table.pile)
			self.table.refresh()

		self.bot.hand.remove(chosen_card)

	def play_a_round(self):
		self.player.give_new_hand(self.deck.give_4_cards())
		bot_hand = self.deck.give_4_cards()
		for card in bot_hand:
			self.bot.update_counting(card)
		self.bot.give_new_hand(bot_hand)

		for tour in range(1, 5):
			self.play_a_tour()

	def calculate_points(self):
		print("\n", "Puanlar hesaplanıyor...")
		sleep(self.t_calc)

		for card in self.player.collected_cards:
			self.player.point += card.value

		for card in self.bot.collected_cards:
			self.bot.point += card.value

		self.player.point += (self.player.pisti_count +\
		 self.player.j_pisti_count * 2) * 10

		self.bot.point += (self.bot.pisti_count +\
		 self.bot.j_pisti_count * 2) * 10

		if len(self.player.collected_cards) >= len(self.bot.collected_cards):
			self.player.point += 3

		print(f"{self.player.name}: {self.player.point} puan")
		print(f"{self.bot.name}: {self.bot.point} puan")
		print("")

		if self.player.point >= self.bot.point:
			print("Sen kazandın!")

		else:
			print(self.bot.name, "kazandı!")



