import copy
import random
import time
from main import make_move, set_banners, make_companion_move, remove_unusable_companion_cards, house_card_count, \
    find_card


def select(selected_companion, companion_cards, cards):
    move = [selected_companion]  # Add the companion card to the move list
    choices = companion_cards[selected_companion]['Choice']  # Get the number of choices required by the companion card

    if choices == 1:  # For cards like Jon Snow
        S = get_valid_jon_sandor_jaqan(cards)
        if len(S) != 0:
            move.append(random.choice(S))

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

    return move


def apply(move, companion_cards, turn, player1, player2, cards):
    choose_companion = True  # Reset the flag
    if move[0] in companion_cards.keys():
        # Remove the companion card from the list
        del companion_cards[move[0]]

        # Make the companion move
        is_house = make_companion_move(cards, companion_cards, move, player1 if turn == 1 else player2)

        # Remove the companion cards that cannot be used
        remove_unusable_companion_cards(cards, companion_cards)

        # Set the banners for the players
        set_banners(player1, player2, is_house, turn)

        # Melisandre gives the player another turn
        if move[0] != 'Melisandre':
            # Change the turn
            turn = 2 if turn == 1 else 1

        choose_companion = False  # Reset the flag
    if turn == 1:
        return choose_companion, True, player1, player2
    else:
        return choose_companion, False, player1, player2

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

    moves = []

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

    moves = []

    for card in cards:
        if card.get_name() != 'Varys':
            moves.append(card.get_location())
    return moves


def get_move(cards, player1, player2, companion_cards, choose_companion,weight=None):
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
    weight = [240,10,297,165,282,172,316,127,356]
    if choose_companion:
        depth = 4
        best_score, best_move = minimax_right(cards, True, -float("inf"), float("inf"), player1, player2, time.time(),
                                              depth, companion_cards, False,weight)
    else:
        depth = 7
        best_score, best_move = minimax(cards, True, -float("inf"), float("inf"), player1, player2, time.time(), depth,
                                        companion_cards, False,weight)

    return best_move


def evaluate_board(cards, player1, player2, companion_cards, choose_companion,weight):
    score = 0
    if choose_companion:
        score += weight[0]
    # Retrieve banners from both players
    player1_banners = player1.get_banners()
    player2_banners = player2.get_banners()

    # Calculate the scores of the players
    player1_score = sum(player1_banners.values())
    player2_score = sum(player2_banners.values())

    # Add the score difference to the total score, scaled by a weight
    score += (player1_score - player2_score) * weight[0]

    # Deduct the number of valid moves from the score
    valid_moves = get_valid_moves(cards)
    score -= len(valid_moves) * weight[1]

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
    house_weights_ = {
        'Stark': weight[2],
        'Greyjoy': weight[3],
        'Lannister': weight[4],
        'Targaryen': weight[5],
        'Baratheon': weight[6],
        'Tyrell': weight[7],
        'Tully': weight[8]
    }

    # Adjust the score based on card counts for each house
    for house, weight in house_weights.items():
        if len(player1.cards[house]) > weight / 2:
            score += house_weights_[house]
        elif len(player2.cards[house]) > weight / 2:
            score -= house_weights_[house]
        elif len(player1.cards[house]) == len(player2.cards[house]) == weight / 2:
            score -=  (player2_banners[house] - player1_banners[house])*house_weights_[house]

    return score


def minimax(cards, maxplayer, alpha, beta, player1, player2, start_time, depth, companion_cards, choose_companion,weight):
    """
    Minimax algorithm with alpha-beta pruning and move sorting for better pruning.
    returns best_score, best_move
    """
    next_move = get_valid_moves(cards)
    if time.time() - start_time > 9.91 or not next_move or depth == 0 or choose_companion:
        return evaluate_board(cards, player1, player2, companion_cards, choose_companion,weight), None

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
            test = house_card_count(cards_copy, selected_house)
            if test == 0 and len(companion_cards) != 0:
                choose_companion = True

            val, _ = minimax(cards_copy, False, alpha, beta, player1_copy, player2_copy, start_time, depth - 1,
                             companion_cards_copy, choose_companion,weight)
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
            if house_card_count(cards_copy, selected_house) == 0 and len(companion_cards) != 0:
                choose_companion = True

            val, _ = minimax(cards_copy, True, alpha, beta, player1_copy, player2_copy, start_time, depth - 1,
                             companion_cards_copy, choose_companion,weight)
            if val < best_val:
                best_val = val
                best_move = move
            beta = min(beta, best_val)
            if beta <= alpha:  # Alpha-Beta Pruning
                break
        return best_val, best_move


def minimax_right(cards, maxplayer, alpha, beta, player1, player2, start_time, depth, companion_cards,choose_companion,weight):
    print("********************************")
    next_move = list(companion_cards.keys())
    if time.time() - start_time > 9.91 or not next_move or depth == 0 or choose_companion:
        return evaluate_board(cards, player1, player2, companion_cards, choose_companion,weight), None

    best_move = None
    if maxplayer:
        best_val = -float("inf")
        best_move = None
        for move in next_move:

            if move == 'Jon' or move == 'Sandor':
                print("111111111111111")
                # Stark: 3 Greyjoy: 2 Lannister: 1 Targaryen: 0 Baratheon: 0 Tyrell: 0 Tully: 0
                done = [False, False, False, False, False, False, False, False]
                # print(f"{move} is controlling")
                S = get_valid_jon_sandor_jaqan(cards)
                if (len(S) == 0):
                    continue

                for choice in S:
                    if move == 'Jon':
                        chosen_card_house = find_card(cards, choice).get_house()

                        if chosen_card_house == 'Stark':
                            if done[0]:
                                continue
                            else:
                                done[0] = True
                        if chosen_card_house == 'Greyjoy':
                            if done[1]:
                                continue
                            else:
                                done[1] = True
                        if chosen_card_house == 'Lannister':
                            if done[2]:
                                continue
                            else:
                                done[2] = True
                        if chosen_card_house == 'Targaryen':
                            if done[3]:
                                continue
                            else:
                                done[3] = True
                        if chosen_card_house == 'Baratheon':
                            if done[4]:
                                continue
                            else:
                                done[4] = True
                        if chosen_card_house == 'Tyrell':
                            if done[5]:
                                continue
                            else:
                                done[5] = True
                        if chosen_card_house == 'Tully':
                            if done[6]:
                                continue
                            else:
                                done[6] = True



                    cards_copy = copy.deepcopy(cards)
                    player1_copy = copy.deepcopy(player1)
                    player2_copy = copy.deepcopy(player2)
                    companion_cards_copy = copy.deepcopy(companion_cards)
                    new_move = [move, choice]
                    choose_companion, Maxplayer, player1_copy, player2_copy = apply(new_move, companion_cards_copy, 1, player1_copy, player2_copy, cards_copy)

                    val, _ = minimax(cards_copy, Maxplayer, alpha, beta, player1_copy, player2_copy, start_time, depth - 1, companion_cards_copy, choose_companion,weight)
                    if val > best_val:
                        best_val = val
                        best_move = new_move

            elif move == 'Gendry':
                # print("Gendry is controlling")
                print("22222222222222222")
                cards_copy = copy.deepcopy(cards)
                player1_copy = copy.deepcopy(player1)
                player2_copy = copy.deepcopy(player2)
                companion_cards_copy = copy.deepcopy(companion_cards)
                new_move = ["Gendry"]
                choose_companion, Maxplayer, player1_copy, player2_copy = apply(new_move, companion_cards_copy, 1, player1_copy, player2_copy, cards_copy)
                val, _ = minimax(cards_copy, Maxplayer, alpha, beta, player1_copy, player2_copy, start_time, depth - 1, companion_cards_copy, choose_companion,weight)
                if val > best_val:
                    best_val = val
                    best_move = new_move
                alpha = max(alpha, best_val)
                if beta <= alpha:  # Alpha-Beta Pruning
                    break


            elif move == 'Ramsay':
                print("33333333333333333")
                # print("Ramsay is controlling")
                cards1 = copy.deepcopy(get_valid_ramsay(cards))
                for c1 in cards1:
                    for c2 in cards1:
                        if c1 == c2:
                            continue
                        new_move = ['Ramsay', c1, c2]
                        cards_copy = copy.deepcopy(cards)
                        player1_copy = copy.deepcopy(player1)
                        player2_copy = copy.deepcopy(player2)
                        companion_cards_copy = copy.deepcopy(companion_cards)
                        choose_companion, Maxplayer, player1_copy, player2_copy = apply(new_move, companion_cards_copy, 1, player1_copy, player2_copy, cards_copy)

                        val, _ = minimax(cards_copy, Maxplayer, alpha, beta, player1_copy, player2_copy, start_time, depth - 1, companion_cards_copy, choose_companion,weight)
                        if val > best_val:
                            best_val = val
                            best_move = new_move


            elif move == 'Melisandre':
                print("444444444444444")
                # print("Melisandre is controlling")
                cards_copy = copy.deepcopy(cards)
                player1_copy = copy.deepcopy(player1)
                player2_copy = copy.deepcopy(player2)
                companion_cards_copy = copy.deepcopy(companion_cards)
                new_move = [move]
                choose_companion, Maxplayer, player1_copy, player2_copy = apply(new_move, companion_cards_copy, 1, player1_copy, player2_copy,cards_copy)

                val, _ = minimax(cards_copy, Maxplayer, alpha, beta, player1_copy, player2_copy, start_time, depth - 1,companion_cards_copy, choose_companion,weight)
                if val > best_val:
                    best_val = val
                    best_move = new_move

            else:

                valid_moves = get_valid_jon_sandor_jaqan(cards)

                for i in valid_moves:
                    for j in valid_moves:
                        if i == j:
                            continue
                        cards_copy = copy.deepcopy(cards)
                        player1_copy = copy.deepcopy(player1)
                        player2_copy = copy.deepcopy(player2)
                        companion_cards_copy = copy.deepcopy(companion_cards)
                        k = random.choice(list(companion_cards_copy.keys()))
                        while k == 'Jaqen':
                            k = random.choice(list(companion_cards_copy.keys()))
                        _, _, player1_copy, player2_copy = apply(['Jaqen', i, j, k], companion_cards_copy,1,player1_copy, player2_copy, cards_copy)
                        score = evaluate_board(cards_copy, player1_copy, player2_copy, companion_cards_copy, False,weight)
                        if score > best_val:
                            best_val = score
                            best_move = ['Jaqen', i, j, k]

        return best_val, best_move



    else:
        best_val = float("inf")

        for move in next_move:



            if move == 'Jon' or move == 'Sandor':
                # Stark: 3 Greyjoy: 2 Lannister: 1 Targaryen: 0 Baratheon: 0 Tyrell: 0 Tully: 0
                done = [False, False, False, False, False, False, False, False]
                print(f"{move} is controlling")
                S = get_valid_jon_sandor_jaqan(cards)
                if (len(S) == 0):
                    continue

                for choice in S:
                    chosen_card_house = find_card(cards, choice).get_house()
                    if move == 'Jon':
                        if chosen_card_house == 'Stark':
                            if done[0]:
                                continue
                            else:
                                done[0] = True
                        if chosen_card_house == 'Greyjoy':
                            if done[1]:
                                continue
                            else:
                                done[1] = True
                        if chosen_card_house == 'Lannister':
                            if done[2]:
                                continue
                            else:
                                done[2] = True
                        if chosen_card_house == 'Targaryen':
                            if done[3]:
                                continue
                            else:
                                done[3] = True
                        if chosen_card_house == 'Baratheon':
                            if done[4]:
                                continue
                            else:
                                done[4] = True
                        if chosen_card_house == 'Tyrell':
                            if done[5]:
                                continue
                            else:
                                done[5] = True
                        if chosen_card_house == 'Tully':
                            if done[6]:
                                continue
                            else:
                                done[6] = True

                    cards_copy = copy.deepcopy(cards)
                    player1_copy = copy.deepcopy(player1)
                    player2_copy = copy.deepcopy(player2)
                    companion_cards_copy = copy.deepcopy(companion_cards)
                    new_move = [move, choice]
                    choose_companion, Maxplayer, player1_copy, player2_copy = apply(new_move, companion_cards_copy, 2, player1_copy, player2_copy,
                                                        cards_copy)

                    val, _ = minimax(cards_copy, Maxplayer, alpha, beta, player1_copy, player2_copy, start_time, depth - 1, companion_cards_copy, choose_companion,weight)

                    if val < best_val:
                        best_val = val
                        best_move = new_move

            elif move == 'Gendry':
                print("Gendry is controlling")

                cards_copy = copy.deepcopy(cards)
                player1_copy = copy.deepcopy(player1)
                player2_copy = copy.deepcopy(player2)
                companion_cards_copy = copy.deepcopy(companion_cards)
                new_move = ["Gendry"]
                choose_companion, Maxplayer, player1_copy, player2_copy = apply(new_move, companion_cards_copy, 2, player1_copy, player2_copy, cards_copy)
                val, _ = minimax(cards_copy, Maxplayer, alpha, beta, player1_copy, player2_copy, start_time, depth - 1, companion_cards_copy, choose_companion,weight)

                if val < best_val:
                    best_val = val
                    best_move = new_move

            elif move == 'Ramsay':
                print("Ramsay is controlling")
                cards1 = copy.deepcopy(get_valid_ramsay(cards))
                for c1 in cards1:
                    for c2 in cards1:
                        if c1 == c2:
                            continue
                        new_move = ['Ramsay', c1, c2]
                        cards_copy = copy.deepcopy(cards)
                        player1_copy = copy.deepcopy(player1)
                        player2_copy = copy.deepcopy(player2)
                        companion_cards_copy = copy.deepcopy(companion_cards)
                        choose_companion, Maxplayer, player1_copy, player2_copy = apply(new_move, companion_cards_copy, 2, player1_copy, player2_copy, cards_copy)

                        val, _ = minimax(cards_copy, Maxplayer, alpha, beta, player1_copy, player2_copy, start_time, depth - 1, companion_cards_copy, choose_companion,weight)
                        if val < best_val:
                            best_val = val
                            best_move = new_move

            elif move == 'Melisandre':
                print("Melisandre is controlling")
                cards_copy = copy.deepcopy(cards)
                player1_copy = copy.deepcopy(player1)
                player2_copy = copy.deepcopy(player2)
                companion_cards_copy = copy.deepcopy(companion_cards)
                new_move = [move]
                choose_companion, Maxplayer, player1_copy, player2_copy = apply(new_move, companion_cards_copy, 2, player1_copy, player2_copy,cards_copy)

                val, _ = minimax(cards_copy, Maxplayer, alpha, beta, player1_copy, player2_copy, start_time, depth - 1,companion_cards_copy, choose_companion,weight)
                if val < best_val:
                    best_val = val
                    best_move = new_move


            else:
                valid_moves = get_valid_jon_sandor_jaqan(cards)

                for i in valid_moves:
                    for j in valid_moves:
                        if i == j:
                            continue
                        cards_copy = copy.deepcopy(cards)
                        player1_copy = copy.deepcopy(player1)
                        player2_copy = copy.deepcopy(player2)
                        companion_cards_copy = copy.deepcopy(companion_cards)
                        k = random.choice(list(companion_cards_copy.keys()))
                        while k == 'Jaqen':
                            k = random.choice(list(companion_cards_copy.keys()))
                        _, _, player1_copy, player2_copy = apply(['Jaqen', i, j, k], companion_cards_copy,2,player1_copy, player2_copy, cards_copy)
                        score = evaluate_board(cards_copy, player1_copy, player2_copy, companion_cards_copy, False,weight)
                        if score > best_val:
                            best_val = score
                            best_move = ['Jaqen', i, j, k]
        return best_val, best_move
