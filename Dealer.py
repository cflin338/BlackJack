
"""
Created on Thu Jun 29 20:38:18 2023

@author: clin4
"""

for dealer_card in range(5,9):
    deck_count = 1
    deck = {i:4*deck_count for i in range(2,11)}
    deck['J'] = 4*deck_count
    deck['Q'] = 4*deck_count
    deck['K'] = 4*deck_count
    deck['A'] = 4*deck_count
    
    #set faceup dealer card
    max_deck = deck.copy()
    #dealer_card = 5
    dealer_count = 0
    
    #adjust deck
    face = ['K', 'Q', 'J']
    
    if dealer_card in face:
        deck[10]-=1
        dealer_count = 10
        ace_count = 0
    elif dealer_card =='A':
        deck['A']-=1
        dealer_count = 11
        ace_count = 1
    else:
        deck[dealer_card]-=1
        dealer_count = dealer_card
        ace_count=0
    

max_draws = 2    
    
combinations_found = {}
    
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
        output = []
        for card in deck:
            if max_deck[card]-deck[card]>0:
                output.append((card,max_deck[card]-deck[card]))
        if debug:
            print(current_count, output)
        
        return 1, 1
    elif current_count>=17:
        #more than 17 and less than max card limit
        return 0, 1
    
    bust_count = 0
    safe_count = 0
    for card in deck:

        if deck[card]>0:
            deck[card]-=1
            
            if cache:
                all_drawn.append(str(card))
                tmp = all_drawn.copy()
                tmp.sort()
                #heapq.heappush(all_drawn, str(card))
                #all_drawn.sort()
                all_drawn_string = ''.join(tmp)
                if all_drawn_string in combinations_found:
                    bust_count+=combinations_found[all_drawn_string][0]
                    safe_count+=combinations_found[all_drawn_string][1]
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
            if cache:
                combinations_found[all_drawn_string] = [bust_count, safe_count]
                all_drawn.pop()
            
    return bust_count, safe_count
    
    bust_draws = bust(current_count = dealer_card, 
                      deck = deck, 
                      drawn = 0, 
                      ace_count = ace_count, 
                      all_drawn = [],
                      debug=False)
    print('dealer card', dealer_card, bust_draws)
    
    
    

        
    