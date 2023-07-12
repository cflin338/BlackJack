

"""
Created on Thu Jun 22 17:28:47 2023
 
@author: Chris Lin
"""
 
counter = {'A': 0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, 
           '8':0, '9':0, '10':0, 'J':0, 'Q':0, 'K':0}
 
class deck():
    def __init__(self, deck_count=1,total_hands=5):
        
        self.total_hands = total_hands
        
        self.counter = {'A': [0, deck_count*4], '2':[0, deck_count*4], '3':[0, deck_count*4], 
                   '4':[0, deck_count*4], '5':[0, deck_count*4], '6':[0, deck_count*4], 
                   '7':[0, deck_count*4], '8':[0, deck_count*4], '9':[0, deck_count*4], 
                   '10':[0, deck_count*4], 'J':[0, deck_count*4], 'Q':[0, deck_count*4], 
                   'K':[0, deck_count*4]}
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
    
    def calc_dealer_bust(self):
        #bag of coins question
        #assume dealer does not have an ace
        card = self.dealer['card']
        if card in ['K', 'Q','J']:
            diff = 21 - 10
        else:
            diff = 21 - int(card)
            
        diff = self.dealer['card']
        
        
        
        #bust in 1 draw
        #bust in 2 draws
        #bust in 3 draws
        
        return
        
    def update_total(self, card, hand_number):
        #update totals
        #10's for J/Q/K
        #for A, first index is if A represents 1, second if A represents 11
        current_total = self.hand_totals[hand_number]
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
                for i in range(list(self.counter.keys()).index(str(leeway)),len(self.counter)):
                   bust_card_count+=self.counter[list(self.counter.keys())[i]][1]
                
                rate = bust_card_count/self.remaining_cards
            bust_rates.append(rate)
        self.calc_dealer_bust()
        self.bust_chance = bust_rates
                  
        
    def card_drawn(self, card, hand_number, debug=False):
        #check if cards left
        if self.counter[card][1]==0:
            print('ERROR, NO MORE OF {} TO DRAW'.format(card))
            return
        #update hands
        self.hands[hand_number].append(card)
        #update card counts
        self.counter[card][0]+=1
        self.counter[card][1]-=1
        self.remaining_cards-=1
        #update hand totals
        self.update_total(card,hand_number)
        #update bust rate for every hand
        self.update_bust_rate()
        if debug:
            print(self.hands)
            print(self.bust_chance)
            print(self.counter)
        
    def reset(self):
        self.counter = {'A': [0, self.deck_count*4], '2':[0, self.deck_count*4], '3':[0, self.deck_count*4], 
                        '4':[0, self.deck_count*4], '5':[0, self.deck_count*4], '6':[0, self.deck_count*4], 
                        '7':[0, self.deck_count*4], '8':[0, self.deck_count*4], '9':[0, self.deck_count*4], 
                        '10':[0, self.deck_count*4], 'J':[0, self.deck_count*4], 'Q':[0, self.deck_count*4], 
                        'K':[0, self.deck_count*4]}
        self.remaining_cards = 52*self.deck_count
        self.bust_chance = [0]*self.total_hands
        
        self.hand_totals = [0]*self.total_hands
        self.hands = [[] for i in range(self.total_hands)]
        
d = deck()
d.card_drawn('5',0, debug=True)
d.card_drawn('5',0, debug=True)
d.card_drawn('2',0, debug=True)
d.reset()
 
d.card_drawn('K',3,debug=True)
d.card_drawn('6',3,debug=True)
 
#print(d.hands)
#print(d.bust_chance)
