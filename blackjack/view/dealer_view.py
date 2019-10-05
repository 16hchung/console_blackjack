from .hand_view import HandView
from ..controller.console_helper import WinPosition as WinPos

class DealerView:
	def __init__(self, cns_helper):
		self.window = cns_helper.new_window(WinPos.Top, 'DEALER')
		self.hand_view = HandView(self.window, 3, 2)
