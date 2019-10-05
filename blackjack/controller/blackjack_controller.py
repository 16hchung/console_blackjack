
from ..model.gameplay import Blackjack
from ..view.dealer_view import DealerView
from ..view.player_view import PlayerView
from ..view.info_view import InfoView

class BlackjackController(Blackjack):
	def __init__(self, cns_helper, *kargs, **kwargs):
		super().__init__(*kargs, **kwargs)
		self.cns_helper = cns_helper
		self.dealer_view, self.info_view, self.player_views = self.init_views()
		self.dealer_view.card_dealt(self._deal_card())
		self.dealer_view.window.getch()

	def init_views(self):
		dealer_view = DealerView(self.cns_helper)
		info_view = InfoView(self.cns_helper)
		player_views = []
		for i, player in enumerate(self.players):
			player_view = PlayerView(
				self.cns_helper, 
				player.name, player.money,
				not i
			)
			player_views.append(player_view)
		return dealer_view, None, player_views

	def start_gameplay_loop(self):
		# take player bets
		# dealer card
		# deal hands to each player
		# take player actions
		# get rest of dealer hand
		# take or give out money
		pass

