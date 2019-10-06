
from ..model.gameplay import Blackjack
from ..model.player import Action
from ..model.rl_player import RLPlayer
from ..model.cards import Rank, Suit
from ..view.dealer_view import DealerView
from ..view.player_view import PlayerView
from ..view.info_view import InfoView

class BlackjackController(Blackjack):
	quit_key = 'q'
	hit_key = 'h'
	stand_key = 's'
	cont_key = ' '
	cont_descr = 'SPACE'

	bet_mult = 10

	def __init__(self, cns_helper, *kargs, n_decks=5, **kwargs):
		super().__init__(*kargs, n_decks=n_decks, **kwargs)
		self.cns_helper = cns_helper
		self.dealer_view, self.info_view, self.player_views = self.init_views()

	###################################################################################################
	##################                     RESET FUNCTIONS                            #################
	###################################################################################################

	def init_views(self):
		deck_size = len(Rank) * len(Suit)
		dealer_view = DealerView(self.cns_helper, deck_size * self.n_decks)
		info_view = InfoView(self.cns_helper)
		player_views = []
		for i, player in enumerate(self.players):
			player_view = PlayerView(
				self.cns_helper, 
				player.name, player.money,
				not i
			)
			player_views.append(player_view)
		return dealer_view, info_view, player_views

	def reset(self):
		self.dealer_view.hand_done()
		for view in self.player_views:
			view.hand_done()
		self.wait_user_inpt(
			'Press {} to start new round'.format(self.cont_descr), 
			lambda s: s == self.cont_key
		)

	def shuffle_shoe(self):
		self.shoe.shuffle()
		self.dealer_view.reset()
		for player in self.players:
			player.shoe_shuffled()
		self.print_msg_and_wait('Shoe was getting small, so reshuffled.')

	###################################################################################################
	##################                     DEALING LIFECYCLE                          #################
	###################################################################################################

	def start_gameplay_loop(self):
		do_quit = False
		while not do_quit:
			self.reset()
			self.take_bets()
			self.start_dealer_hand()
			self.deal_player_hands()
			self.loop_player_actions()
			self.finish_dealer_hand()
			self.settle_bets()
			quit_resp = self.wait_user_inpt('Continue (any key) or quit ({})?'.format(self.quit_key))
			do_quit = quit_resp == self.quit_key
			if self.done:
				self.shuffle_shoe()

	def take_bets(self):
		for i, player in enumerate(self.players):
			player.place_bet()
			if isinstance(player, RLPlayer):
				continue
			bet = int(self.wait_user_inpt(
				'Place your bet: Press 1 to bet $10, 2 for $20, ... 5 for $50',
				lambda s: s.isdigit() and 1 <= int(s) <= 5
			))
			player.bet = bet * self.bet_mult
			self.info_view.clear()

	def get_player_action(self, player):
		if isinstance(player, RLPlayer):
			action = player.action()
			action_string = 'hit' if action == Action.Hit else 'stand'
			self.print_msg_and_wait('{} decided to {}.'.format(player.name, action_string))
		else:
			# Model shouldn't know anything about user input, so this gets handled by controller
			action_letter_options = [self.hit_key, self.stand_key]
			action_letter = self.wait_user_inpt(
				'Hit ({}) or stand ({})?'.format(*action_letter_options),
				lambda s: s in action_letter_options
			)
			action = Action.Hit if action_letter == self.hit_key else Action.Stand
		return action

	def start_dealer_hand(self):
		super().start_dealer_hand()
		card = self.dealer_hand.cards[0]
		self.dealer_view.hand_card_added(card)

	def _deal_card(self):
		card = super()._deal_card()
		self.dealer_view.card_dealt()
		return card

	def deal_player_hands(self):
		for i, player in enumerate(self.players):
			view = self.player_views[i]
			self.deal_hand_to_player(player)
			view.cards_dealt(player.hand.cards)
			if player.hand.is_blackjack:
				self.print_msg_and_wait('{} got blackjack!'.format(player.name))
		self.print_msg_and_wait('Initial hands have been dealt.')

	def loop_player_actions(self):
		n_players = len(self.players)
		def ready_to_settle_bets():
			return [player.is_turn_done for player in self.players].count(True) == n_players

		while not ready_to_settle_bets():
			for i, player in enumerate(self.players):
				self.get_and_handle_player_action(player, self.player_views[i])

	def get_and_handle_player_action(self, player, view):
		if player.is_turn_done:
			return
		action = self.get_player_action(player)
		busted = self.handle_player_action(player, action)
		if action == Action.Hit:
			view.card_dealt(player.hand.cards[-1])
		if busted:
			view.update_money_label(player.money)
			self.print_msg_and_wait(
				'{}\'s hand busted, losing ${} :('.format(
					player.name, player.bet * self.bet_mult 
			))

	def finish_dealer_hand(self):
		super().finish_dealer_hand()
		self.dealer_view.hand_cards_added(self.dealer_hand.cards[1:])
		self.print_msg_and_wait('Dealer\'s hand has been finished.')

	def settle_bets(self):
		for i, player in enumerate(self.players):
			reward = self.settle_bet_with_player(player)
			view = self.player_views[i]
			self.display_bet_result(player, view, reward)

	def display_bet_result(self, player, view, reward):
		if reward == None: return
		view.update_money_label(player.money)
		if reward > 0:
			self.print_msg_and_wait('{} beat the dealer!'.format(player.name))
		elif reward < 0:
			self.print_msg_and_wait('{} lost to the dealer :('.format(player.name))
		else:
			self.print_msg_and_wait('{} tied with the dealer :/'.format(player.name))

	###################################################################################################
	##################                     HELPER FUNCTIONS                           #################
	###################################################################################################

	def wait_user_inpt(self, prompt=None, condition=lambda s: True):
		if prompt:
			self.info_view.print_text(prompt)
		result = str(chr(self.info_view.window.getch()))
		while not condition(result):
			result = str(chr(self.info_view.window.getch()))
		return result

	def print_msg_and_wait(self, msg):
		self.wait_user_inpt(
			msg + ' Press {} to continue'.format(self.cont_descr),
			lambda s: s == self.cont_key
		)






