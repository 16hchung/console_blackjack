from .cards import Card, Shoe
from .hand import Hand
from .player import Action, Player

max_decks = 8
min_decks = 2
max_players = 3

class Blackjack:
	def __init__(self, players, n_decks=5, min_shoe_size=30, rand_state=None):
		if len(players) > max_players or len(players) < 1:
			raise ValueError(
				'Number of players must be between 1 and {}'.format(max_players)
			)
		if n_decks > max_decks or n_decks < min_decks:
			raise ValueError(
				'Number of decks must be between {} and {}'.format(min_decks,max_decks)
			)
		self.shoe = Shoe(n_decks, rand_state)
		self.n_decks = n_decks
		self.min_shoe_size = min_shoe_size
		self.players = players
		self.dealer_hand = None

	@property
	def done(self):
		return self.shoe.cards_left <= self.min_shoe_size

	def _deal_card(self):
		card = self.shoe.draw_card()
		if not card:
			return None
		for player in self.players:
			player.card_was_drawn(card)
		return card

	def deal_card_to_player(self, player):
		card = self._deal_card()
		player.hand.add_card(card)

	def deal_hand_to_player(self, player):
		cards = []
		cards.append(self._deal_card())
		cards.append(self._deal_card())
		player.hand = Hand(cards)
		if player.hand.is_blackjack:
			player.maxed_hand()

	def handle_player_action(self, player, action):
		''' handles player action and returns whether or not player's hand busted'''
		if player.is_turn_done:
			return False

		if action == Action.Hit:
			self.deal_card_to_player(player)
			if player.hand.is_bust:
				player.settle_bet(False)
				return True
			elif player.hand.is_maxed:
				player.maxed_hand()
		elif action == Action.Stand:
			player.is_turn_done = True
		else:
			pass
		return False

	def start_dealer_hand(self):
		card = self._deal_card()
		self.dealer_hand = Hand([card])
		for player in self.players:
			player.dealer_card_set(card)

	def finish_dealer_hand(self):
		# reveal other card
		self.dealer_hand.add_card(self._deal_card())
		if self.dealer_hand.is_blackjack:
			return

		# hit until reach 17
		while self.dealer_hand.value < 17:
			self.dealer_hand.add_card(self._deal_card())
		# hit soft 17
		if self.dealer_hand.value == 17 and self.dealer_hand.is_soft:
			self.dealer_hand.add_card(self._deal_card())

	def settle_bet_with_player(self, player):
		if player.hand.is_bust:
			return None

		bet_ratio = 0
		if self.dealer_hand.is_blackjack and player.hand.is_blackjack:
			player_won = None
		elif player.hand.is_blackjack or self.dealer_hand.is_bust:
			player_won = True
			bet_ratio = 1.5
		elif self.dealer_hand.value == player.hand.value:
			player_won = None
		else:
			player_won = self.dealer_hand.value < player.hand.value
			bet_ratio = 1
		player.settle_bet(player_won, bet_ratio)
		reward = bet_ratio * (1 if player_won else -1)
		return reward

