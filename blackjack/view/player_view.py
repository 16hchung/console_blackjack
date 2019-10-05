from .hand_view import HandView
from ..controller.console_helper import WinPosition as WinPos

class PlayerView:
	def __init__(self, cns_helper, player, is_player1):
		win_pos = WinPos.Lplayer if is_player1 else WinPos.Rplayer
		self.window = cns_helper.new_window(win_pos, 'PLAYER: ' + player.name)
		self.hand_view = HandView(self.window, 3, 2)
