
card_offset = 5

class HandView:
	def __init__(self, window, min_l, min_t):
		self.window = window
		self.min_l = min_l
		self.min_t = min_t
		self.card_idx = 0

	def add_card(self, card):
		self.card_idx += 1
		pass

	def clear(self):
		self.card_idx = 0
		pass
