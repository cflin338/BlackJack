# BlackJack
Live update of chance of busting based on cards drawn

#7/11/2023
blackjack.py contains deck class 

inputs:
	deck_count = number of decks played
	total_hands = total hands being played
initialization:
	create counter dictionary counting how many of a certain card drawn, cards remaining
	total remaining cards
	empty hands	
functions:
	calculate/update chance of dealer busting: uses Dealer.py file; note, this includes drawing more than one card
	update total: update possible totals for a specific hand given a card drawn
	update bust rate: update bust chance for each hand if 1 more card is drawn
	card_drawn: update deck class assuming a card is drawn for a certain hand
	reset: resets everything assuming same number of decks, total hands

Dealer.py
	calculating odds of dealer busting given the current cards drawn from the deck
	currently designed to only allow a certain number of cards to be drawn
	work in progress...