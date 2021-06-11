import tkinter
import pygame
import numpy as np
import os
from tkinter import *
from tkinter import messagebox

pygame.font.init()

dict_blocks = {
    0: pygame.image.load(os.path.join('Images', '0block.png')),
    1: pygame.image.load(os.path.join('Images', '1block.png')),
    2: pygame.image.load(os.path.join('Images', '2block.png')),
    3: pygame.image.load(os.path.join('Images', '3block.png')),
    4: pygame.image.load(os.path.join('Images', '4block.png')),
    5: pygame.image.load(os.path.join('Images', '5block.png'))
}

dict_level_select = {
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_4: 4,
    pygame.K_5: 5
}

dict_moves = {
    pygame.K_1: 0,
    pygame.K_2: 1,
    pygame.K_3: 2
}

WHITE = (255, 255, 255)
CYAN = (52, 152, 235)
FONT = pygame.font.SysFont('ComicSans', 40)

WIDTH = 850
HEIGHT = 230
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hanoi Tower')
pygame.display.set_icon(pygame.image.load(os.path.join('Images', 'icon.jpg')))


def show_starter_text():
    WIN.fill(CYAN)
    level_text_1 = FONT.render('Enter the number of blocks', True, WHITE)
    WIN.blit(level_text_1, (247, 80))
    level_text_2 = FONT.render('Press R anytime during the game to restart', True, WHITE)
    WIN.blit(level_text_2, (150, 130))


def msg_box(count):
    Tk().wm_withdraw()
    response = tkinter.messagebox.askyesno('YOU WON',
                                           f'You completed the tower in {count} turns.\nDo you want to play again?')
    return response


def show_invalid_move():
    invalid_text = FONT.render('INVALID MOVE', True, WHITE)
    WIN.blit(invalid_text, (330, 190))


class Puzzle:
    def __init__(self, size):
        self.size = size
        self.blocks = []
        self.coordinates = []
        self.start_index = None
        self.end_index = None

        self.blocks = [[0] * 5 for _ in range(3)]
        self.coordinates = [[(0, 0)] * 5 for _ in range(3)]
        for i in range(self.size):
            self.blocks[0][i] = self.size - i

        for i in range(3):
            for j in range(5):
                x = 275 * i + 25
                y = 25 * (5 - j)
                self.coordinates[i][j] = (x, y)

    def show_blocks(self):
        WIN.fill(CYAN)

        for i in range(3):
            for j in range(5):
                WIN.blit(dict_blocks[self.blocks[i][j]], self.coordinates[i][j])

        title_1 = FONT.render('1', True, WHITE)
        WIN.blit(title_1, (142, 1))
        title_2 = FONT.render('2', True, WHITE)
        WIN.blit(title_2, (417, 1))
        title_3 = FONT.render('3', True, WHITE)
        WIN.blit(title_3, (693, 1))

    def show_start_move(self, start):
        self.start_index = start
        start_text = FONT.render(f'Move block from {self.start_index + 1}', True, WHITE)
        WIN.blit(start_text, (268, 160))

    def set_end_index(self, end):
        self.end_index = end

    def show_end_move(self):
        end_text = FONT.render(f'Move block from {self.start_index + 1} to {self.end_index + 1}', True, WHITE)
        WIN.blit(end_text, (268, 160))

    def move_block(self):
        index = np.max(np.nonzero(self.blocks[self.start_index]))

        if self.blocks[self.end_index][0] == 0:
            self.blocks[self.end_index][0] = self.blocks[self.start_index][index]
        else:  # move block to other stack at the index of the first zero
            self.blocks[self.end_index][self.blocks[self.end_index].index(0)] = self.blocks[self.start_index][index]

        self.blocks[self.start_index][index] = 0

    def valid_move(self):
        if self.blocks[self.start_index][0] != 0:  # check if the stack you're moving FROM has a block in it
            smaller = self.blocks[self.start_index][np.max(np.nonzero(self.blocks[self.start_index]))]
        else:
            return False

        if self.blocks[self.end_index][0] == 0:
            return True
        else:
            larger = self.blocks[self.end_index][np.max(np.nonzero(self.blocks[self.end_index]))]

        if smaller > larger:  # check if you're allowed to move your blocks as per the rules
            return False

        if self.start_index == self.end_index:
            return False
        return True

    def puzzle_complete(self):
        for i in range(1, 3):
            count = 0
            for j in range(self.size):
                if self.blocks[i][j] == self.size - j:
                    count += 1
            if count == self.size:
                return True
        return False


def main():
    run = True
    state = 'starterText'
    turns = 0
    show_starter_text()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = 'starterText'
                    turns = 0
                    show_starter_text()
            if event.type == pygame.KEYDOWN:
                if state == 'starterText':
                    if event.key in dict_level_select:
                        size = dict_level_select[event.key]
                        hanoi = Puzzle(size)
                        state = 'pickStart'
                        hanoi.show_blocks()
                else:
                    hanoi.show_blocks()
                    if state == 'pickStart':
                        if event.key in dict_moves:
                            start = dict_moves[event.key]
                            state = 'pickEnd'
                            hanoi.show_start_move(start)
                    elif state == 'pickEnd':
                        if event.key in dict_moves:
                            end = dict_moves[event.key]
                            hanoi.set_end_index(end)
                            state = 'pickStart'
                            if hanoi.valid_move() is True:
                                hanoi.move_block()
                                hanoi.show_blocks()
                                turns += 1
                            else:
                                show_invalid_move()
                            hanoi.show_end_move()
                            if hanoi.puzzle_complete() is True:
                                pygame.display.update()
                                if msg_box(turns) is True:
                                    state = 'starterText'
                                    turns = 0
                                    show_starter_text()
                                else:
                                    run = False
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
