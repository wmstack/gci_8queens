import random
import argparse

#can be adapted to any size
BOARD_SIZE = 20

#for drawing the image after putqueen generates solutions
from PIL import Image
import numpy as np

def putqueen(board, queens_placed, desired_queens=BOARD_SIZE):
    if queens_placed>=desired_queens:
        return True

    #choices for the index of the queen, shuffled
    queen_choices = [*range(len(board))]
    random.shuffle(queen_choices)
    
    #added for optimization, and it does optimize faster
    bad_queen_locs = []

    for queen_index in queen_choices:
        #pick queen location
        queen = board[queen_index]

        #remove positions from board when the queen can attack them
        new_board = [
            pos for pos in board if

            #pos is not horizontal to queen
            pos[0] != queen[0] and
            #pos is not vertical to queen
            pos[1] != queen[1] and

            #pos is not diagonal, i.e. the horizontal difference does not have the same
            #magnitude as the vertical difference
            abs(pos[0] - queen[0]) != abs(pos[1] - queen[1]) and
            
            #if it were a possible position it would've succeded in a
            #previous iteration, put_queen only outputs false
            #if not possible
            not pos in bad_queen_locs
        ]
        res = putqueen(new_board, queens_placed + 1, desired_queens)
        if res:
            if type(res) == bool: 
                return [queen]
            
            res.append(queen)
            return res
        bad_queen_locs.append(queen)
    else:
        return False

def draw_board(queens, board_size=BOARD_SIZE):

    #draw the board
    board = np.full((64*board_size, 64*board_size,3),0, dtype=np.uint8)
    wb = np.full((64,64,3), 255, dtype=np.uint8)
    

    #draw alternating white and black
    for i in range(board_size):
        for j in range(board_size):
            if (i+j) % 2 == 0:
                board[j*64:j*64+64, i*64:i*64+64] = wb
    
    #draw queens
    queen_img = Image.open('45px-Chess_qlt45.svg.png').convert('RGB')
    queen_img_arr = np.asarray(queen_img)

    for queen in queen_locations:
        #12 is padding for the queen image
        xpos = queen[0]*64 + 12
        ypos = queen[1]*64 + 12
        #draw the queen in the block
        board[ypos:ypos+45, xpos:xpos+45] = queen_img_arr

    #numpy to image
    board_img = Image.fromarray(board, 'RGB')
    
    #save image to out.png and show
    board_img.save('out.png')
    board_img.show()

def parse_args():
    parser = argparse.ArgumentParser(description='Program to compute a random 20 queens solution.')

def main():
    #get the initial board
    initial_board = [(i,j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]

    #get the queen locations
    queen_locations = putqueen(board=initial_board, queens_placed=0)

    #print the locations
    print(queen_locations)

    #draw board with queens and display them
    draw_board(queen_locations)