from .hand_view import HandView
from ..controller.console_helper import WinPosition as WinPos
from ..model.gameplay import max_decks

class DealerView:
	def __init__(self, cns_helper):
		self.window = cns_helper.new_window(WinPos.Top, 'DEALER')
		self.hand_view = HandView(self.window, cns_helper, 4, 1)
		# shoe size label
		self.shoe_size_coords = [1,1]
		self.shoe_size_width = len(str(max_decks*52))

	def card_dealt(self, card):
		self.hand_view.add_card(card)

	def hand_done(self):
		self.hand_view.clear()
