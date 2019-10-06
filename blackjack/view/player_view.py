from .hand_view import HandView
from ..controller.console_helper import WinPosition as WinPos

class PlayerView:
	money_coords = [1, 1]
	money_width = 15

	def __init__(self, cns_helper, player_name, player_money, is_player1):
		self.cns_helper = cns_helper
		win_pos = WinPos.Lplayer if is_player1 else WinPos.Rplayer
		self.window = cns_helper.new_window(win_pos, 'PLAYER: ' + player_name)
		self.hand_view = HandView(self.window, cns_helper, 4, 1)
		# money label setup
		self.update_money_label(player_money)

	def update_money_label(self, money):
		width = self.money_width
		money_str = 'Money: ${0: <{width}}'.format(money, width=width)
		self.cns_helper.print_str(self.window, money_str, *self.money_coords)

	def card_dealt(self, card):
		self.hand_view.add_card(card)

	def cards_dealt(self, cards):
		for card in cards:
			self.card_dealt(card)

	def hand_done(self):
		self.hand_view.clear()

