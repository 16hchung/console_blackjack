import torch
import numpy as np

from .rl_model.decider import DQN
from .player import Player, Action
from .cards import Card, Rank, Suit
#from .rl_model.decider import Decider

class RLPlayer(Player):
	def __init__(self, n_decks, *kargs, model_file=None, **kwargs):
		super().__init__(*kargs, name='Me (the computer)', **kwargs)

		n_suits = len(Suit)
		n_ranks = len(Rank)
		self.n_aces_left  = n_suits * n_decks
		self.n_23or4_left = n_suits * n_decks * 3
		self.n_56or7_left = n_suits * n_decks * 3
		self.n_8or9_left  = n_suits * n_decks * 2
		self.n_10val_left = n_suits * n_decks * 4
		self.n_total_left = n_suits * n_decks * n_ranks

		self.dealer_card = None

		# init neural net
		if model_file:
			self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
			self.policy_net = DQN().to(self.device).float()
			self.policy_net.load_state_dict(torch.load(model_file))
			self.policy_net.eval()

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

	@property
	def current_state_tensor(self):
		return torch.from_numpy(np.array(self.current_state)).float().to(self.device)

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
		if not model_file:
			return Action.Hit
		with torch.no_grad():
			net_result = self.policy_net(self.current_state_tensor).max(0)[1].view(1,1).item()
			return Action(1+net_result)

		#self.decider
