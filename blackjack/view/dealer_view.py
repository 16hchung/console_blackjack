from .hand_view import HandView
from ..controller.console_helper import WinPosition as WinPos
from ..model.gameplay import max_decks

class DealerView:
	shoe_size_coords = [1,1]
	shoe_size_width = len(str(max_decks*52))

	def __init__(self, cns_helper, shoe_size):
		self.cns_helper = cns_helper
		self.window = cns_helper.new_window(WinPos.Top, 'DEALER')
		self.hand_view = HandView(self.window, cns_helper, 4, 1)
		# shoe size label
		self._shoe_size = 0
		self.shoe_size = shoe_size
		self.orig_shoe_size = shoe_size

	@property
	def shoe_size(self):
		return self._shoe_size

	@shoe_size.setter
	def shoe_size(self, value):
		self._shoe_size = value
		width = self.shoe_size_width
		shoe_str = 'Cards left in shoe: {0: <{width}}'.format(self._shoe_size, width=width)
		self.cns_helper.print_str(self.window, shoe_str, *self.shoe_size_coords)

	def hand_card_added(self, card):
		self.hand_view.add_card(card)

	def hand_cards_added(self, cards):
		for card in cards:
			self.hand_card_added(card)

	def card_dealt(self):
		self.shoe_size = self.shoe_size - 1

	def reset(self):
		self.shoe_size = self.orig_shoe_size

	def hand_done(self):
		self.hand_view.clear()
