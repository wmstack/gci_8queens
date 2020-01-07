#! /usr/bin/env python3

#random to pick queen positions randomly
import random
import argparse

#Image saving, loading, manipulation etc...
from PIL import Image

#for drawing the board
import numpy as np

def putqueen(board, queens_placed=0, desired_queens=20):
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

def draw_board(queens, board_size=20, display=True, out='out.png'):

    #draw the board
    black = [0,0,0,255]
    white = [255,255,255,255]

    board = np.full((64*board_size, 64*board_size, 4),black , dtype=np.uint8)
    
    wb = np.full((64,64,4), white, dtype=np.uint8)
    
    #draw alternating white and black
    for i in range(board_size):
        for j in range(board_size):
            if (i+j) % 2 == 0:
                board[j*64:j*64+64, i*64:i*64+64] = wb
    
    #numpy to image
    board_img = Image.fromarray(board, 'RGBA')

    #draw queens
    queen_img = Image.open('45px-Chess_qlt45.svg.png').convert('RGBA')

    for queen in queens:
        #10 is padding for the queen image
        xpos = queen[0]*64 + 10
        ypos = queen[1]*64 + 10
        offset = (xpos, ypos)
        #draw the queen in the block, and donot draw alpha
        board_img.paste(queen_img, offset, queen_img)
    
    #save image to out.png and show
    board_img.save(out,mode='PNG')
    if display:
        board_img.show()

def parse_args():
    parser = argparse.ArgumentParser(description='Program to compute a random N queens solution.')
    parser.add_argument('size',type=int, nargs='?',default=20, help='Board size and number of queens, default is 20')
    parser.add_argument('-n','--no-display',action='store_true', help='Donot display, just save')
    parser.add_argument('-o','--output', help='Output image name, default out.png', default='out.png')
    return parser.parse_args()

def main():
    result = parse_args()
    #get the initial board
    initial_board = [(i,j) for i in range(result.size) for j in range(result.size)]

    #get the queen locations
    queen_locations = putqueen(board=initial_board, desired_queens=result.size)

    #print the locations
    print(queen_locations)

    #draw board with queens and display them
    draw_board(queen_locations, board_size=result.size, out= result.output,  display= not result.no_display)

if __name__ == "__main__":
    main()