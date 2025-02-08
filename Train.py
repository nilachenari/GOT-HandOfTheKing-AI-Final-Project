import json
import random
import copy
import time

import numpy as np

from main import main,parser,make_board

Board = make_board()

def evaluate_fitness(chromosome,count):
    global Board
    board = copy.deepcopy(Board)
    fe = []
    winner, cards, player1, player2 = main(parser.parse_args(),board,chromosome)

    if winner == 1:
        # count = 0
        if chromosome[1] >= 10:
            print("New Board")
            Board = make_board()
        else:
            chromosome[0] = min(2*chromosome[1],10)
    else:
        # if count == 10:
        #     for i in range(len(chromosome)):
        #         chromosome[i] /= 10
        # count+=1
        chromosome[1] = max(chromosome[1]-1,1)




    score = 0
    banner_weight = 100
    house_weights_ = {
        'Stark': chromosome[2],
        'Greyjoy': chromosome[3],
        'Lannister': chromosome[4],
        'Targaryen': chromosome[5],
        'Baratheon': chromosome[6],
        'Tyrell': chromosome[7],
        'Tully': chromosome[8],
    }

    # Retrieve banners from both players
    player1_banners = player1.get_banners()
    player2_banners = player2.get_banners()


    fe.extend(list(player1_banners.values()))
    fe.extend(list(player2_banners.values()))
    # Calculate the scores of the players
    player1_score = sum(player1_banners.values())
    player2_score = sum(player2_banners.values())

    # Add the score difference to the total score, scaled by a weight
    score += (player1_score - player2_score) * banner_weight

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
    p1 = []
    p2 = []
    # Adjust the score based on card counts for each house
    for house, weight in house_weights.items():
        if len(player1.cards[house]) > weight / 2:
            score +=  house_weights_[house]
            if winner == 2:
                chromosome[10 - weight] -= 1
        elif len(player2.cards[house]) > weight / 2:
            score -=  house_weights_[house]
            if winner == 2:
                chromosome[10-weight] += 10
        elif len(player1.cards[house]) == len(player2.cards[house]) == weight / 2:
            point = (player2_banners[house] - player1_banners[house])
            score -=  point * house_weights_[house]
            if winner == 2:
                if point < 0:
                    chromosome[10-weight] -=1
                else:
                    chromosome[10-weight] += 10
        p1.append(len(player1.cards[house]))
        p2.append(len(player2.cards[house]))
    fe.extend(p1)
    fe.extend(p2)
    fe.extend(chromosome)
    fe.append(winner)
    fe.append(score)
    # File path to save the array
    file_path = 'training_logs.csv'

    # Writing the 2D array to a text file
    with open(file_path, 'a') as file:
        file.write(','.join(map(str, fe)) + '\n')
    print("Writed")


    return chromosome,count

def generate_random_weights():
    # Generate random weights for the evaluation function
    w = [random.randint(0, 100) for _ in range(9)]
    w[0] = sum(w[2:])//7
    w[1] = 1
    return w

if __name__ == "__main__":

    weight = generate_random_weights()
    count = 0
    for i in range(100):
       weight,count = evaluate_fitness(weight,count)

    print(weight)

