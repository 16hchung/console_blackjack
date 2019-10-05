from curses import wrapper as crs_wrapper

from .model.player import Player
from .model.rl_player import RLPlayer
from .model.gameplay import max_decks, min_decks
from .controller.console_helper import ConsoleHelper
from .controller.blackjack_controller import BlackjackController

def input_with_condition(prompt, reprompt, valid_check):
	print(prompt)
	result = input()
	while not valid_check(result):
		print(reprompt)
		result = input()
	return result

def show_intro():
	player_name = input_with_condition(
		'What is your name?',
		'Name must be <= 20 characters',
		lambda s: len(s) <= 20
	)
	player_money = int(input_with_condition(
		'How much money are you starting with? (please input a multiple of 10)',
		'Money must be an integer multiple of 10, less than 10^10',
		lambda s: s.isdigit() and int(s) % 10 == 0 and int(s) < 10e10
	))
	n_decks = int(input_with_condition(
		'How many decks should be in the shoe?',
		'Number of decks must be <= {} and >= {}'.format(max_decks, min_decks),
		lambda s: s.isdigit() and min_decks <= int(s) <= max_decks
	))
	input_with_condition(
		'Is your window the appropriate size: INSERT ROWS COLS? (y/n)', #TODO
		'Is your window the appropriate size: INSERT ROWS COLS? (y/n)', #TODO
		lambda s: s == 'y',
	)
	return n_decks, player_name, player_money

def init_models(n_decks, player_name, player_money):
	print('Please wait while I load my reinforcement learning-trained player...')
	human = Player(player_name, player_money)
	rl_model = RLPlayer(n_decks, model_file='params_state_dict.pkl')
	return human, rl_model

def start_game(screen, n_decks, human, rl_player):
	# init curses-related objects and start gameplay
	cns_helper = ConsoleHelper(screen)
	blackjack_controller = BlackjackController(
		cns_helper,
		[rl_player, human],
		n_decks=n_decks
	)
	blackjack_controller.start_gameplay_loop()

def main():
	user_prefs = show_intro()
	human, rl_player = init_models(*user_prefs)
	n_decks,_,_ = user_prefs
	crs_wrapper(start_game, n_decks, human, rl_player)

if __name__=='__main__':
	main()
