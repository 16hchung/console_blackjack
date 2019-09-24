import gym
from gym import spaces
from gym.utils import seeding

import numpy as np

from ..cards import Shoe, Rank, Suit
from ..player import Action
from ..rl_player import RLPlayer
from ..gameplay import Blackjack, max_decks
from .decider import state_space_upper_bounds


class BlackjackEnv(gym.Env):
	def __init__(self):
		# hit, stand, double down (later add insurance, split, etc)
		self.action_space = spaces.Discrete(len(Action))
		lower_bounds = np.zeros((len(state_space_upper_bounds)))
		self.observation_space = spaces.Box(
			low=lower_bounds,
			high=state_space_upper_bounds,
			dtype=np.float32
		)
		#self.observation_space = spaces.Tuple((
		#	# num aces per deck in shoe
		#	spaces.Discrete(max_cards_per_deck),
		#	# num 2/3/4 per deck in shoe
		#	spaces.Discrete(max_cards_per_deck * 3), 
		#	# num 5/6/7 per deck in shoe
		#	spaces.Discrete(max_cards_per_deck * 3), 
		#	# num 8/9   per deck in shoe
		#	spaces.Discrete(max_cards_per_deck * 2),
		#	# num 10-valued per deck in shoe
		#	spaces.Discrete(max_cards_per_deck * 4),
		#	# player hand value
		#	spaces.Discrete(32),
		#	# hand contains usable ace
		#	spaces.Discrete(2),
		#	# dealer's card value
		#	spaces.Discrete(10),
		#	# approx num decks left
		#	spaces.Discrete(8)
		#))
		self.seed()
		self.player = None
		self.game   = None
		self.reset()

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]

	def step(self, action):
		done = False
		action_e = Action(action+1) # python enum indexing starts at 1
		busted = self.game.handle_player_action(self.player, action_e)
		# if hit and < 21
		if action_e == Action.Hit and not busted \
					  and not self.player.hand.is_maxed: 
			reward = 0
			new_state = self.player.current_state
		else: # this hand is done
			if action_e == Action.Hit and busted:
				reward = -1
			else: # reached 21 or action was stand
				self.game.finish_dealer_hand()
				reward = self.game.settle_bet_with_player(self.player)
			new_state = self._new_hand()
		return np.array(new_state), reward, self.game.done, {'money':self.player.money}

	def reset(self):
		self.player = RLPlayer(max_decks)
		self.game = Blackjack([self.player], n_decks=max_decks, min_shoe_size=10, rand_state=self.np_random)
		state = self._new_hand()
		return np.array(state)

	def _new_hand(self):
		# if player gets natural blackjack, not useful for training
		self.game.deal_hand_to_player(self.player)
		while self.player.hand.is_blackjack:
			self.game.deal_hand_to_player(self.player)
		self.player.place_bet()
		self.game.start_dealer_hand()
		return self.player.current_state
