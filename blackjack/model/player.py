from enum import Enum

Action = Enum('Action', 'Hit Stand')# DoubleDown')

class Player:
	def __init__(self, name=None, money=100):
		self.name = name
		self.money = money
		self.hand = None
		self.is_turn_done = True
		self._bet = 1

	def card_was_drawn(self, card):
		pass # must override in sub class

	def dealer_card_set(self, card):
		pass # must override in sub class

	def action(self):
		return Action.Hit # must override in sub class

	def maxed_hand(self):
		self.is_turn_done = True

	def settle_bet(self, did_win, bet_ratio=1):
		self.is_turn_done = True
		amt = int(bet_ratio * self._bet)
		if did_win == None:
			pass # tied
		elif did_win:
			self.money += amt
		else:
			self.money -= amt

	def place_bet(self):
		self.is_turn_done = False
		return self._bet
