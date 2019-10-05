from .hand_view import HandView
from ..controller.console_helper import WinPosition as WinPos

class PlayerView:
	def __init__(self, cns_helper, player_name, player_money, is_player1):
		self.cns_helper = cns_helper
		win_pos = WinPos.Lplayer if is_player1 else WinPos.Rplayer
		self.window = cns_helper.new_window(win_pos, 'PLAYER: ' + player_name)
		self.hand_view = HandView(self.window, cns_helper, 3, 1)
		# money label setup
		self.money_coords = [1, 1]
		self.money_width = 15
		self.update_money_label(player_money)

	def update_money_label(self, money):
		pass

	def card_dealt(self, card):
		self.hand_view.add_card(card)

	def hand_done(self):
		self.hand_view.clear()

