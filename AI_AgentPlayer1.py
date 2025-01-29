import copy
import random
import time
from main import make_move, set_banners, make_companion_move, remove_unusable_companion_cards, house_card_count

# this version has only jon playing in minimax
def find_varys(cards):
    '''
    This function finds the location of Varys on the board.

    Parameters:
        cards (list): list of Card objects

    Returns:
        varys_location (int): location of Varys
    '''

    varys = [card for card in cards if card.get_name() == 'Varys']

    varys_location = varys[0].get_location()

    return varys_location

def get_valid_moves(cards):
    '''
    This function gets the possible moves for the player.

    Parameters:
        cards (list): list of Card objects

    Returns:
        moves (list): list of possible moves
    '''

    # Get the location of Varys
    varys_location = find_varys(cards)

    varys_row, varys_col = varys_location // 6, varys_location % 6

    moves = []

    for card in cards:
        if card.get_name() == 'Varys':
            continue

        row, col = card.get_location() // 6, card.get_location() % 6

        if row == varys_row or col == varys_col:
            moves.append(card.get_location())

    return moves

def get_valid_ramsay(cards):
    '''
    This function gets the possible moves for Ramsay.

    Parameters:
        cards (list): list of Card objects
    
    Returns:
        moves (list): list of possible moves
    '''

    moves=[]

    for card in cards:
        moves.append(card.get_location())
    
    return moves

def get_valid_jon_sandor_jaqan(cards):
    '''
    This function gets the possible moves for Jon Snow, Sandor Clegane, and Jaqen H'ghar.

    Parameters:
        cards (list): list of Card objects
    
    Returns:
        moves (list): list of possible moves
    '''

    moves=[]

    for card in cards:
        if card.get_name() != 'Varys':
            moves.append(card.get_location())
    
    return moves

def get_move(cards, player1, player2, companion_cards, choose_companion):
    '''
    This function gets the move of the player.

    Parameters:
        cards (list): list of Card objects
        player1 (Player): the player
        player2 (Player): the opponent
        companion_cards (dict): dictionary of companion cards
        choose_companion (bool): flag to choose a companion card

    Returns:
        move (int/list): the move of the player
    '''

    if 1 == 3:
        pass

    else:
        # Normal move, choose from valid moves
        moves = get_valid_moves(cards)

        cards_copy = copy.deepcopy(cards)
        player1_copy = copy.deepcopy(player1)
        player2_copy = copy.deepcopy(player2)
        companion_cards_copy = copy.deepcopy(companion_cards)
        choose_companion_copy = copy.deepcopy(choose_companion)

        depth = 2
        best_score, best_move = minimax(cards_copy, True, -float("inf"), float("inf"), player1_copy, player2_copy, time.time(), depth, companion_cards_copy, choose_companion_copy)
        # if(best_move == 'Jon'):
        #     print("returning best_move in get_move()")
        #     if(len(best_move) == 1):
        #         print("right error!!!!!!")


        return best_move





def evaluate_board(cards, player1, player2, companion_cards=[], choose_companion= False):
    score = 0

    # Retrieve banners from both players
    player1_banners = player1.get_banners()
    player2_banners = player2.get_banners()

    # Calculate the scores of the players
    player1_score = sum(player1_banners.values())
    player2_score = sum(player2_banners.values())

    # Add the score difference to the total score, scaled by a weight
    score += (player1_score - player2_score) * 100

    # Deduct the number of valid moves from the score
    valid_moves = get_valid_moves(cards)
    score -= len(valid_moves)

    # Define weights for different houses
    house_weights = {
        'Stark': 8,
        'Greyjoy': 7,
        'Lannister': 6,
        'Targaryen': 5,
        'Baratheon': 4,
        'Tyrell': 3,
        'Tully': 2
    }

    # Adjust the score based on card counts for each house
    for house, weight in house_weights.items():
        if len(player1.cards[house]) > weight / 2:
            score += 100
        elif len(player2.cards[house]) > weight / 2:
            score -= 100
        elif len(player1.cards[house]) == len(player2.cards[house]) == weight / 2:
            score -= 100 * (player2_banners[house] - player1_banners[house])

    return score


def minimax(cards, maxplayer, alpha, beta, player1, player2, start_time, depth, companion_cards =[], choose_companion=False):
    """
    Minimax algorithm with alpha-beta pruning and move sorting for better pruning.
    returns best_score, best_move
    """


    if choose_companion:
        # Choose a random companion card if available

        # if(maxplayer):
        #     best_val = -float("-inf")
        #
        #     if companion_cards:
        #
        #         # for comp_card in companion_cards:
        #
        #             comp_card = "Jon"
        #
        #             move = [comp_card]
        #             choices = companion_cards[comp_card]['Choice']
        #
        #             if(comp_card == 'Jon'):
        #                 valids = get_valid_jon_sandor_jaqan(cards)
        #                 for valid in valids:
        #
        #                     cards_copy = copy.deepcopy(cards)
        #                     player1_copy = copy.deepcopy(player1)
        #                     player2_copy = copy.deepcopy(player2)
        #                     companion_cards_copy = copy.deepcopy(companion_cards)
        #                     move_copy = copy.deepcopy(move)
        #
        #                     del companion_cards_copy[move_copy[0]]
        #                     is_house = make_companion_move(cards_copy, companion_cards_copy, move_copy, player1_copy)
        #                     print("****************************************************")
        #                     remove_unusable_companion_cards(cards_copy, companion_cards_copy)
        #                     player1_copy, player2_copy = set_banners(player1_copy, player2_copy, is_house, 1)
        #                     move_copy.append(valid)
        #
        #                     val, _ = minimax(cards_copy, False, alpha, beta, player1_copy, player2_copy, start_time, depth - 1, companion_cards_copy)
        #                     if val > best_val:
        #                         best_val = val
        #                         best_move = move
        #                     alpha = max(alpha, best_val)
        #                     if beta <= alpha:  # Alpha-Beta Pruning
        #                         break
        #                 return best_val, best_move


                    # elif(comp_card == 'Gendry'):
                    #     pass
                    # elif(comp_card == 'Ramsay'):
                    #     pass
                    # elif(comp_card == 'Sandor'):
                    #     pass
                    # elif(comp_card == 'Jaqen'):
                    #     pass
                    # elif(comp_card == 'Melisandre'):
                    #     pass
                    # else:
                    #     print("ERORRRRRRRRRRRRRR")


            flag = False
            for c in companion_cards:
                if c == "Jon":
                    flag = True

            if(flag):
                if (maxplayer):
                    best_val = -float("-inf")

                    if companion_cards:

                        # for comp_card in companion_cards:

                        comp_card = "Jon"

                        move = [comp_card]
                        del companion_cards[move[0]]
                        print("tekrariiiiiiiiiiiiiiiii")


                        if (comp_card == 'Jon'):
                            valids = get_valid_jon_sandor_jaqan(cards)
                            for valid in valids:
                                cards_copy = copy.deepcopy(cards)
                                player1_copy = copy.deepcopy(player1)
                                player2_copy = copy.deepcopy(player2)
                                companion_cards_copy = copy.deepcopy(companion_cards)
                                move_copy = copy.deepcopy(move)

                                move_copy.append(valid)

                                is_house = make_companion_move(cards_copy, companion_cards_copy, move_copy, player1_copy)
                                print("it is jonnnnnnnnnnnnnnnnnn")
                                remove_unusable_companion_cards(cards_copy, companion_cards_copy)
                                # player1_copy, player2_copy = set_banners(player1_copy, player2_copy, is_house, 1)
                                set_banners(player1_copy, player2_copy, is_house, 1)



                                print("33333333333333333333333333333333333333")
                                choose_companion = False
                                val, _ = minimax(cards_copy, False, alpha, beta, player1_copy, player2_copy, start_time, depth - 1, companion_cards_copy, False)
                                if val > best_val:
                                    best_val = val
                                alpha = max(alpha, best_val)
                                if beta <= alpha:  # Alpha-Beta Pruning
                                    break
                            return best_val, move_copy




            else:
                print("not jonnnnnnnnnnn")
                if(not companion_cards) : return 0, []
                selected_companion = random.choice(list(companion_cards.keys()))  # Randomly select a companion card

                move = [selected_companion]  # Add the companion card to the move list
                choices = companion_cards[selected_companion]['Choice']  # Get the number of choices required by the companion card

                if choices == 1:  # For cards like Jon Snow
                    move.append(random.choice(get_valid_jon_sandor_jaqan(cards)))

                elif choices == 2:  # For cards like Ramsay
                    valid_moves = get_valid_ramsay(cards)

                    if len(valid_moves) >= 2:
                        move.extend(random.sample(valid_moves, 2))

                    else:
                        move.extend(valid_moves)  # If not enough moves, just use what's available


                elif choices == 3:  # Special case for Jaqen with an additional companion card selection
                    valid_moves = get_valid_jon_sandor_jaqan(cards)

                    if len(valid_moves) >= 2 and len(companion_cards) > 0:
                        move.extend(random.sample(valid_moves, 2))
                        move.append(random.choice(list(companion_cards.keys())))

                    else:
                        # If there aren't enough moves or companion cards, just return what's possible
                        move.extend(valid_moves)
                        move.append(random.choice(list(companion_cards.keys())) if companion_cards else None)

                return 0, move








    else:
        next_move = get_valid_moves(cards)
        if time.time() - start_time > 9.91 or not next_move or depth == 0:
            return evaluate_board(cards, player1, player2), None

        best_move = None
        if maxplayer:
            best_val = -float("inf")
            for move in next_move:
                cards_copy = copy.deepcopy(cards)
                player1_copy = copy.deepcopy(player1)
                player2_copy = copy.deepcopy(player2)
                companion_cards_copy = copy.deepcopy(companion_cards)

                selected_house = make_move(cards_copy, move, player1_copy)
                set_banners(player1_copy, player2_copy, selected_house, 1)

                choose_companion = False
                # if house_card_count(cards_copy, selected_house) == 0 and len(companion_cards) != 0:
                #     choose_companion = True

                # print("maxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                val, _ = minimax(cards_copy, False, alpha, beta, player1_copy, player2_copy, start_time, depth - 1, companion_cards_copy, choose_companion)
                if val > best_val:
                    best_val = val
                    best_move = move
                alpha = max(alpha, best_val)
                if beta <= alpha:  # Alpha-Beta Pruning
                    break
            return best_val, best_move
        else:
            best_val = float("inf")
            for move in next_move:
                cards_copy = copy.deepcopy(cards)
                player1_copy = copy.deepcopy(player1)
                player2_copy = copy.deepcopy(player2)
                companion_cards_copy = copy.deepcopy(companion_cards)

                selected_house = make_move(cards_copy, move, player2_copy)
                set_banners(player1_copy, player2_copy, selected_house, 2)

                choose_companion = False
                # if house_card_count(cards_copy, selected_house) == 0 and len(companion_cards) != 0:
                #     choose_companion = True


                # print("minnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
                val, _ = minimax(cards_copy, True, alpha, beta, player1_copy, player2_copy, start_time, depth - 1, companion_cards_copy, choose_companion)
                if val < best_val:
                    best_val = val
                    best_move = move
                beta = min(beta, best_val)
                if beta <= alpha:  # Alpha-Beta Pruning
                    break
            return best_val, best_move


