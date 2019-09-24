from .cards import Card, Rank

class Hand:
	def __init__(self, cards):
		self.cards = cards
		self._is_soft = None
		self._value = None
		self._set_value()

	@property
	def value(self):
		return self._value

	@property
	def is_bust(self):
		return self._value > 21

	@property
	def is_soft(self):
		return self._is_soft

	@property
	def is_blackjack(self):
		return len(self.cards) ==2 and self.value == 21

	@property
	def is_maxed(self):
		return self.value == 21

	def _set_value(self):
		self._is_soft = False
		self._value = 0
		n_aces = 0
		for card in self.cards:
			if card.rank == Rank.A:
				n_aces += 1
			else:
				self._value += card.value
		# handle aces in hand
		for _ in range(n_aces):
			if self._value > 10:
				self._value += 1
			else:
				self._is_soft = True
				self._value += 11
		return self._value

	def add_card(self, card):
		self.cards.append(card)
		self._set_value()
