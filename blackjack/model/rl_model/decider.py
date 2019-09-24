import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F

max_cards_per_deck = 20 # estimated
state_space_upper_bounds = np.array([
	max_cards_per_deck,     # num aces per deck in shoe
	max_cards_per_deck * 3, # num 2/3/4 per deck in shoe
	max_cards_per_deck * 3, # num 5/6/7 per deck in shoe
	max_cards_per_deck * 2, # num 8/9   per deck in shoe
	max_cards_per_deck * 4, # num 10-valued per deck in shoe
	32,                     # player hand value
	2,                      # hand contains usable ace
	10,                     # dealer's card value
	8                       # approx num decks left
])
input_dim = len(state_space_upper_bounds)
n_actions = 2 # don't use player.Action enum bc don't want circular dependency

class DQN(nn.Module):
	def __init__(self):
		super().__init__()
		self.fc1 = nn.Linear(input_dim, 10)
		self.fc2 = nn.Linear(10, n_actions)
		self.dropout = nn.Dropout(p=.1)

	def forward(self, x):
		x = self.fc1(x)
		x = self.dropout(x)
		x = torch.tanh(x)
		x = self.fc2(x)
		return torch.tanh(x)
