
from .card_templates import card_templates, rank_placeholder

class HandView:
	card_offset = 5

	def __init__(self, window, cns_helper, min_l, min_t):
		self.window = window
		self.min_l = min_l
		self.min_t = min_t
		self.win_h, self.win_w = window.getmaxyx()
		self.card_idx = 0
		self.cns_helper = cns_helper

	def add_card(self, card):
		card_str = self.card_string(card)
		self.cns_helper.print_str(
			self.window, 
			card_str,
			self.min_t,
			self.min_l + self.card_offset * self.card_idx
		)
		self.card_idx += 1

	def clear(self):
		self.card_idx = 0
		self.cns_helper.clear_window_rect(
			self.window,
			self.min_t, self.win_h,
			self.min_l, self.win_w
		)

	@staticmethod
	def card_string(card):
		template = card_templates[card.suit]
		padded_rank = '{0: <2}'.format(card.rank.name)
		card_str = template.replace(rank_placeholder, padded_rank, 1)
		padded_rank = '{0: >2}'.format(card.rank.name)
		card_str = card_str.replace(rank_placeholder, padded_rank, 1)
		return card_str
