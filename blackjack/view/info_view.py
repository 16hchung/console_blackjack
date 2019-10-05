
from ..controller.console_helper import WinPosition as WinPos

class InfoView:
	def __init__(self, cns_helper, default_msg=''):
		self.window = cns_helper.new_window(WinPos.Message, 'INSRUCTIONS')
		self.h, self.w = self.window.getmaxyx()
		self.border = 1
		self.default_msg = default_msg
		self.cns_helper = cns_helper

	def clear(self):
		self.cns_helper.clear_window_rect(
			self.window, 
			self.border, self.h-self.border,
			self.border, self.w-self.border
		)

	def print_text(self, text):
		#clear original text
		self.clear()
		# print text
		self.cns_helper.print_str(self.window, text)
