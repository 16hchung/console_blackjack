import curses as crs
import math
from enum import Enum

WinPosition = Enum('WinPosition', 'Top Message Lplayer Rplayer')
WinProportions = { # % of screen: (top, bottom, left right)
	WinPosition.Top: [0, .5, 0, 1],
	WinPosition.Message: [.5, .625, 0, 1],
	WinPosition.Lplayer: [.625, 1, 0, .5],
	WinPosition.Rplayer: [.625, 1, .5, 1],
}

class ConsoleHelper:

	def __init__(self, screen):
		self.screen = screen
		self.n_rows, self.n_cols = screen.getmaxyx()
		self.win_positions = {pos:False for pos in WinPosition}

	def new_window(self, pos, header=None):
		if self.win_positions[pos]:
			return None
		coords = self.coords_for_position(pos)
		window = crs.newwin(*coords)
		[_,_,t,l] = coords
		window.border()
		if header != None:
			window.addstr(1, 1, header)
		window.refresh()
		return window

	def clear_window(self, window):
		window.clear()
		window.refresh()

	def get_string(self):
		return ''

	def coords_for_position(self, pos):
		scale_t, scale_b, scale_l, scale_r = WinProportions[pos].copy()
		t = int(math.ceil(self.n_rows * scale_t))
		l = int(math.ceil(self.n_cols * scale_l))
		b = int(self.n_rows * scale_b)
		r = int(self.n_cols * scale_r)
		return (b-t, r-l, t, l)

