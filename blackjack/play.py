from curses import wrapper as crs_wrapper

from .model.player import Player
from .controller.console_helper import ConsoleHelper
from .controller.blackjack_controller import BlackjackController

def show_intro():
	pass

def start_game(screen):#, player_name, player_money):
	# init models
	human = Player('bob')#player_name, player_money)
#	rl_model = Player()

	# init curses-related objects and start gameplay
	cns_helper = ConsoleHelper(screen)
	blackjack_controller = BlackjackController(
		cns_helper,
		[human]
	)
	blackjack_controller.start_gameplay_loop()


def main():
	show_intro()
	crs_wrapper(start_game)

if __name__=='__main__':
	main()
