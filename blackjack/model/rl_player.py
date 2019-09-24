from .player import Player, Action
from .cards import Card, Rank, Suit
#from .rl_model.decider import Decider

class RLPlayer(Player):
	def __init__(self, n_decks, *kargs, **kwargs):
		super().__init__(*kargs, **kwargs)

		n_suits = len(Suit)
		n_ranks = len(Rank)
		self.n_aces_left  = n_suits * n_decks
		self.n_23or4_left = n_suits * n_decks * 3
		self.n_56or7_left = n_suits * n_decks * 3
		self.n_8or9_left  = n_suits * n_decks * 2
		self.n_10val_left = n_suits * n_decks * 4
		self.n_total_left = n_suits * n_decks * n_ranks

		self.dealer_card = None

	@property
	def current_state(self):
		n_decks_left = self.n_total_left / len(Suit) / len(Rank)
		def n_left_per_deck(n_left):
			return n_left / n_decks_left
		state = (
			n_left_per_deck(self.n_aces_left),
			n_left_per_deck(self.n_23or4_left),
			n_left_per_deck(self.n_56or7_left),
			n_left_per_deck(self.n_8or9_left),
			n_left_per_deck(self.n_10val_left),
			self.hand.value,
			int(self.hand.is_soft),
			min(self.dealer_card.value, 10),
			n_decks_left
		)
		return state

	def card_was_drawn(self, card):
		if card.rank == Rank.A:
			self.n_aces_left -= 1
		elif 2 <= card.value <= 4:
			self.n_23or4_left -= 1
		elif 5 <= card.value <= 7:
			self.n_56or7_left -= 1
		elif 8 <= card.value <= 9:
			self.n_8or9_left -= 1
		else:
			self.n_10val_left -= 1
		self.n_total_left -= 1

	def dealer_card_set(self, card):
		self.dealer_card = card

	def action(self):
		return Action.Hit
		#self.decider
