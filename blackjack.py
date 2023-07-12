

"""
Created on Thu Jun 22 17:28:47 2023
 
@author: Chris Lin
"""
 
counter = {'A': 0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, 
           '8':0, '9':0, '10':0, 'J':0, 'Q':0, 'K':0}
 
class deck():
    def __init__(self, deck_count=1,total_hands=5):
        
        self.total_hands = total_hands
        
        #self.counter = {'A': [0, deck_count*4], '2':[0, deck_count*4], '3':[0, deck_count*4], 
        #           '4':[0, deck_count*4], '5':[0, deck_count*4], '6':[0, deck_count*4], 
        #           '7':[0, deck_count*4], '8':[0, deck_count*4], '9':[0, deck_count*4], 
        #           '10':[0, deck_count*4], 'J':[0, deck_count*4], 'Q':[0, deck_count*4], 
        #           'K':[0, deck_count*4]}
        self.deck = {i:4*deck_count for i in range(2,11)}
        self.deck['J'] = 4*deck_count
        self.deck['Q'] = 4*deck_count
        self.deck['K'] = 4*deck_count
        self.deck['A'] = 4*deck_count
        
        self.max_deck = self.deck.copy()
        
        
        self.deck_count = deck_count
        self.remaining_cards = 52*deck_count
        self.bust_chance = [0]*total_hands
        
        self.hand_totals = [0]*total_hands
        self.hands = [[] for i in range(total_hands)]
        self.split = [] #will hold both hand and bust chance
        #dealer will contain a single card, with bust %
        #will need to update this
        self.dealer = {'card':'', 'bust%': 0, }
    
    def deal_dealer(self, card):
        self.dealer['card'] = card
        self.dealer['bust%'] = self.calc_dealer_bust()
    
    def calc_dealer_bust(self, max_draws = 2,):
        face = ['K', 'Q', 'J']
                
        #combinations_found = {}
            
        def bust(current_count, deck,drawn, ace_count, all_drawn,cache=False, debug = False):
            if ace_count>0 and current_count>21:
                current_count-=10
                ace_count-=1
                
            if drawn>max_draws:
                #means previously, less than 21 and drew max allowed
                #only increase to valid combination count
                return 0, 1
            
            elif current_count>21:
                #previous draw resulted in a bust
                #add to bust count, combination count
                return 1, 1
            elif current_count>=17:
                #more than 17 and less than max card limit
                return 0, 1
            
            bust_count = 0
            safe_count = 0
            for card in deck:
        
                if deck[card]>0:
                    deck[card]-=1
                    
                    #if cache:
                    #    all_drawn.append(str(card))
                    #    tmp = all_drawn.copy()
                    #    tmp.sort()
                    #    all_drawn_string = ''.join(tmp)
                    #    if all_drawn_string in combinations_found:
                    #        bust_count+=combinations_found[all_drawn_string][0]
                    #        safe_count+=combinations_found[all_drawn_string][1]
                    if card=='A':
                        #do this
                        if current_count+11<=21:
                            b = bust(current_count+11, deck, drawn+1, ace_count+1, all_drawn, cache = cache, debug = debug)
                            bust_count+=b[0]
                            safe_count+=b[1]
                        b = bust(current_count+1, deck, drawn+1, ace_count, all_drawn, cache = cache, debug = debug)
                        bust_count+=b[0]
                        safe_count+=b[1]
                    elif card in face:
                        b=bust(current_count+10, deck, drawn+1, ace_count, all_drawn, cache = cache, debug = debug)
                        bust_count+=b[0]
                        safe_count+=b[1]
                    else:
                        b = bust(current_count+card, deck, drawn+1, ace_count, all_drawn, cache = cache, debug = debug)
                        bust_count+=b[0]
                        safe_count+=b[1]
                    deck[card]+=1
                    #if cache:
                    #    combinations_found[all_drawn_string] = [bust_count, safe_count]
                    #    all_drawn.pop()
                    
            return bust_count, safe_count
            
            bust_draws = bust(current_count = self.dealer['card'], 
                              deck = self.deck, 
                              drawn = 0, 
                              ace_count = ace_count, 
                              all_drawn = [],
                              debug=False)
            #print('dealer card', dealer_card, bust_draws)
            #bustdraws = [number of bust draws, total possible draws]
            return bust_draws
    
        
    def update_total(self, card, hand_number):
        #update totals
        #10's for J/Q/K
        #for A, first index is if A represents 1, second if A represents 11
        #current_total = self.hand_totals[hand_number]
        if card in ['J','Q','K']:
            self.hand_totals[hand_number]+=10
            
        elif card=='A':
            self.hand_totals[hand_number]+=1
            
        else:
            self.hand_totals[hand_number]+=int(card)
            
    def update_bust_rate(self):
        #update bust rate
        bust_rates = []
        for totals in self.hand_totals:
            if totals<12:
                rate = 0
            else:
                leeway = 22-totals
                bust_card_count = 0
                #count frome leeway up till 10
                #count J Q K
                bust_card_count = 0
                for i in range(leeway, 11):
                    bust_card_count+=self.deck[i]
                for face in ['J','Q','K']:
                    bust_card_count+=self.deck[face]
                
                rate = bust_card_count/self.remaining_cards
            bust_rates.append(rate)
            
        self.bust_chance = bust_rates
        if self.dealer['card']:
            self.dealer['bust%'] = self.calc_dealer_bust()
                  
        
    def card_drawn(self, card, hand_number, debug=False):
        #check if cards left
        if self.deck[card]==0:
            print('ERROR, NO MORE OF {} TO DRAW'.format(card))
            return
        #update hands
        self.hands[hand_number].append(card)
        #update card counts
        self.deck[card]-=1
        self.remaining_cards-=1
        #update hand totals
        self.update_total(card,hand_number)
        #update bust rate for every hand
        self.update_bust_rate()
        if debug:
            print(self.hands)
            print(self.bust_chance)
            print(self.deck)
        
    def reset(self):
        self.deck = {i:4*self.deck_count for i in range(2,11)}
        self.deck['J'] = 4*self.deck_count
        self.deck['Q'] = 4*self.deck_count
        self.deck['K'] = 4*self.deck_count
        self.deck['A'] = 4*self.deck_count
        
        self.remaining_cards = 52*self.deck_count
        self.bust_chance = [0]*self.total_hands
        
        self.hand_totals = [0]*self.total_hands
        self.hands = [[] for i in range(self.total_hands)]
        
d = deck(total_hands = 1)
d.card_drawn(card = 5,hand_number = 0, debug=True)
d.card_drawn(card = 5,hand_number = 0, debug=True)
d.deal_dealer(card = 'K')
#d.card_drawn(card = 5,hand_number = 1, debug=True)
#d.card_drawn(card = 5,hand_number = 1, debug=True)
#d.card_drawn(card = 4,hand_number = 2, debug=True)
#d.card_drawn(card = 4,hand_number = 2, debug=True)
#d.card_drawn(card = 4,hand_number = 3, debug=True)
#d.card_drawn(card = 4,hand_number = 3, debug=True)
#d.card_drawn(card = 3,hand_number = 4, debug=True)
#d.card_drawn(card = 3,hand_number = 4, debug=True)
d.reset()
 
d.card_drawn('K',0,debug=True)
d.card_drawn(6,0,debug=True)
 
#print(d.hands)
#print(d.bust_chance)
