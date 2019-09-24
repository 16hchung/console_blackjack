from enum import Enum
import numpy as np

Rank = Enum('Rank', 'A 2 3 4 5 6 7 8 9 10 J Q K')
Suit = Enum('Suit', 'Hearts Diamonds Clubs Spades')

class Card:
	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
		self.value = 10 if self.rank.value >= 10 else \
			     11 if self.rank == Rank.A   else \
			     self.rank.value

class Shoe:
	def __init__(self, n_decks, rand_state):
		# init cards (keep in arrays instead of card objects for efficiency)
		ranks, suits = self._generate_deck()
		self.ranks = n_decks * ranks
		self.suits = n_decks * suits

		rand_state = rand_state or np.random.RandomState()
		self._shuffle_idcs = list(range(len(self.ranks)))
		rand_state.shuffle(self._shuffle_idcs)
		self._position = 0

	@property
	def cards_left(self):
		return len(self.ranks) - self._position

	@staticmethod
	def _generate_deck():
		rank_values = [r.value for r in list(Rank)]
		ranks = []
		suits = []
		for suit in Suit:
			s_val = suit.value
			ranks += rank_values
			suits += [suit.value] * len(rank_values)
		return ranks, suits

	def draw_card(self):
		if self._position >= len(self.ranks):
			return None
		idx = self._shuffle_idcs[self._position]
		rank = self.ranks[idx]
		suit = self.suits[idx]
		self._position += 1
		return Card(Rank(rank), Suit(suit))
