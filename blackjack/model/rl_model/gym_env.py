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
	def __init__(self, params_fname=None):
		# hit, stand, double down (later add insurance, split, etc)
		self.action_space = spaces.Discrete(len(Action))
		lower_bounds = np.zeros((len(state_space_upper_bounds)))
		self.observation_space = spaces.Box(
			low=lower_bounds,
			high=state_space_upper_bounds,
			dtype=np.float32
		)
		self.info_keys = ['money']
		self.params_fname = params_fname
		self.seed()
		self.player = None
		self.game   = None
		self.reset()

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]

	def step(self, action):
		done = False
		busted = self.game.handle_player_action(self.player, action)
		# if hit and < 21
		if action == Action.Hit and not busted \
					  and not self.player.hand.is_maxed: 
			reward = 0
			new_state = self.player.current_state
		else: # this hand is done
			if action == Action.Hit and busted:
				reward = -1
			else: # reached 21 or action was stand
				self.game.finish_dealer_hand()
				reward = self.game.settle_bet_with_player(self.player)
			new_state = self._new_hand()
		return np.array(new_state), reward, self.game.done, {'money':self.player.money}

	def reset(self):
		self.player = RLPlayer(max_decks, model_file=self.params_fname)
		self.player.bet = 1
		self.game = Blackjack([self.player], n_decks=max_decks, min_shoe_size=20, rand_state=self.np_random)
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

