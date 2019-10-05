
from ..model.gameplay import Blackjack
from .console_helper import WinPosition as WinPos

class BlackjackController(Blackjack):
	def __init__(self, cns_helper, *kargs, **kwargs):
		super().__init__(*kargs, **kwargs)
		self.cns_helper = cns_helper
		self.dealer_win, self.rl_win, self.human_win, self.msg_win = self.init_windows()
		self.dealer_win.getch()

	def init_windows(self):
		dealer_win = self.cns_helper.new_window(WinPos.Top)
		rl_win = self.cns_helper.new_window(WinPos.Lplayer)
		human_win = self.cns_helper.new_window(WinPos.Rplayer)
		msg_win = self.cns_helper.new_window(WinPos.Message)
		return dealer_win, rl_win, human_win, msg_win

	def start_gameplay_loop(self):
		pass
