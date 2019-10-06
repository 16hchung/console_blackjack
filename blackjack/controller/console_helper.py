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
			window.addstr(0, 2, header)
		window.refresh()
		return window

	def coords_for_position(self, pos):
		scale_t, scale_b, scale_l, scale_r = WinProportions[pos].copy()
		t = int(math.ceil(self.n_rows * scale_t))
		l = int(math.ceil(self.n_cols * scale_l))
		b = int(self.n_rows * scale_b)
		r = int(self.n_cols * scale_r)
		return (b-t, r-l, t, l)

	@classmethod
	def safe_trim_rect(cls, window, t, b, l, r):
		t = max(t,1)
		b = min(b,window.getmaxyx()[0]-1)
		l = max(l,1)
		r = min(r,window.getmaxyx()[1]-1)
		return t, b, l, r

	@classmethod
	def clear_window_rect(cls, window, t, b, l, r):
		t, b, l, r = cls.safe_trim_rect(window, t, b, l, r)
		for y in range(t, b):
			for x in range(l, r):
				window.addch(y,x,' ')
		window.refresh()

	@classmethod
	def print_str(cls, window, text, t=1, l=1):
		lines = text.splitlines()
		w = max(len(line) for line in lines)
		h = len(lines)
		t, b, l, r = cls.safe_trim_rect(window, t, t+h, l, l+w)
		# print each line (no newlines, bc don't want to overwrite characters to the right)
		for i in range(b-t):
			line = lines[i]
			window.addnstr(t, l, line, r-l)
			t += 1
		window.refresh()

