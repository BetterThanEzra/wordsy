#!/usr/bin/env python3

import random
import csv

import sys
sys.setrecursionlimit(600)


bonus_letters = {
    "F" : 1,
    "H" : 1,
    "J" : 2,
    "K" : 1,
    "Q" : 2,
    "V" : 1,
    "W" : 1,
    "X" : 2,
    "Y" : 1,
    "Z" : 2
}

location_points = {
   1 : 5,
   2 : 5,
   3 : 4,
   4 : 4,
   5 : 3,
   6 : 3,
   7 : 2,
   8 : 2
}

game_letters = None

threshold = 65

###### FILE HANDLING ############################################################################################################
def read_files():
    words = list_from_file('filtered_words.csv', 'word')
    letters = list_from_file("wordsey-letters.txt", 'char')
    return letters, words

def list_from_file(file_name, list_of):
    f = open(file_name, "r")
    contents = ''
    if f.mode == 'r':
        contents = f.read()
    if list_of == 'char':
        contents = list(contents)
    if list_of == 'word':
        contents = contents.split()
    contents = remove_values_from_list(contents, '\n')
    contents = remove_values_from_list(contents, ' ')
    return contents


def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]


def store_to_file(data, mode, filename):
    # mode: a|append  w|write
    file = open(filename, mode)
    file.write(','.join(data))
    file.write('\n')
    file.close()  


###### GAME COMPONENTS ############################################################################################################
def simulate_game(letters):
    random.shuffle(letters)
    global game_letters
    game_letters = letters
    game_rounds = [[] for i in range(7)]
    game_rounds[0] = create_first_board()
    for i in range(1,7):
         game_rounds[i] = update_board(game_rounds[i-1])
    return game_rounds


def get_letter():
    global game_letters
    letter = game_letters[0]
    game_letters = game_letters[1:]
    return letter


def valid_letter(board,rec):
    new_letter = get_letter()
    bonus_letters_list = [ k for k in bonus_letters ]
    bc = board.count(new_letter)
    bbc = sum(el in bonus_letters_list for el in board) + bonus_letters_list.count(new_letter)
    if bc < 2 and bbc <= 2:
        return new_letter
    else:
        return valid_letter(board, rec+1)


def create_first_board():
    board = []
    board_size = 8
    for i in range(board_size):
        new_letter = valid_letter(board,0)
        board.insert(0, new_letter)
    return board


def update_board(previous_round):
    board = previous_round[:4]
    for i in range(4):
        new_letter = valid_letter(board,0)
        board.insert(0, new_letter)
    return board


###### SCORING ############################################################################################################


def score_word(word, game):
    total_score = 0
    for game_round in game:
        total_score = total_score + score_round(word,game_round)
    return total_score

    
def score_round(word,game_round):
    this_round = game_round.copy()
    word_letters = list(word.upper())
    scoring_letters = {}
    ## scoring_letters = []
    for c in word_letters:
        if c in this_round:
            scoring_letters[c] = this_round.index(c)+1
            ## scoring_letters.append(c)
            this_round.remove(c)
    return score_letters(scoring_letters)


def score_letters(scoring_letters):
    global bonus_letters
    global location_points
    score = 0
    for l in scoring_letters:
        score = score + bonus_letters.get(l, 0 ) + location_points[scoring_letters[l]]
    return score


###### MAIN ############################################################################################################

def main():
    letters, words = read_files()
    store_to_file(["---"], 'w', "filtered_word_averages.csv")
    print("starting")
    for word in words:
        running_word_score = 0
        for i in range(1,100000):
            game = simulate_game(letters)
            running_word_score = running_word_score + score_word(word, game)
            avg = running_word_score/i
            rnd_avg = avg/7
            print("Running simulation:","{:10f}".format(i)," word:", word," averge:","{:10.4f}".format(avg), "round average:", "{:10.4f}".format(rnd_avg) , end='\r')
        data = [ word, str(round(avg, 5)) , str(round(rnd_avg,5)) ]
        store_to_file(data, 'a', "filtered_word_averages.csv")
    print("\ndone")
    

if __name__ == "__main__":
    main()