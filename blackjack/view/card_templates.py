from ..model.cards import Suit

rank_placeholder = 'XX'
card_height = 7
card_width = 9
card_templates = {
	Suit.Hearts: 	' _______ \n' +  
			'|XX     |\n' +  
			'|  _ _  |\n' +  
			'| ( v ) |\n' +  
			'|  \\ /  |\n'+ 
			'|   .   |\n' +  
			'|_____XX|\n',

	Suit.Clubs: 	' _______ \n' +  
			'|XX     |\n' +  
			'|   _   |\n' +  
			'|  ( )  |\n' +  
			'| (_\'_) |\n' +  
			'|   |   |\n' +  
			'|_____XX|\n',

	Suit.Spades: 	' _______ \n' +  
			'|XX     |\n' +  
			'|   .   |\n' +  
			'|  /.\\  |\n'+ 
			'| (_._) |\n' +  
			'|   |   |\n' +  
			'|_____XX|\n',

	Suit.Diamonds: 	' _______ \n' +  
			'|XX     |\n' +  
			'|   ^   |\n' +  
			'|  / \\  |\n'+ 
			'|  \\ /  |\n'+ 
			'|   v   |\n' +  
			'|_____XX|\n' 
}
