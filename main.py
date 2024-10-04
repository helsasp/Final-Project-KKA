import sys

import pygame

from Game_Board import *

game = Game()
ai = game.ai
user = -1
alg = 1

while True:

    # Mendapatkan event dari user
    for event in pygame.event.get():

    #Quit Game jika diclose
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: #periksa tombol

           #Jika pencet g, mode game akan berganti 
            if event.key == pygame.K_g:
                game.change_gamemode()
                print(f'game mode changed to {game.gamemode}')

            # Jika pencet r,  game akan restart
            if event.key == pygame.K_r:
                game.reset()
                board = game.board
                ai = game.ai
                screen.fill(background_color)
                print('game restarted')

    # Masuk ke fungsi home game di awal
    if game.player == -1:
        game.home_page()
        alg = ai.algorithm

    #Game distart, masuk ke show lines
    else:
        game.show_lines()

        # Mode AI vs Player

        #Periksa giliran player
        if game.player == game.turn and game.running and game.gamemode == 'ai':
           
           #Pemain click kotak yang ada dan mendapatkan posisi
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                pos = pygame.mouse.get_pos()
                row = pos[1] // square_size
                col = pos[0] // square_size

                #Periksa kotak empty, jika empty akan diisi
                if game.board.empty_sqr(row, col):
                    game.make_move(row, col)
        else:
            # Giliran AI
            if game.running:
                # update screen
                pygame.display.update()

            #Menentukan langkah dengan algoritma yg ada
                row, col = ai.eval(game.board, game.turn, game.gamemode, alg)
                game.make_move(row, col)
                time.sleep(0.5)

        # Jika game over, ada tombol untuk play again
        if game.isover():
            game.running = False
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            game.set_button(againButton, 'Play Again')

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1: # Game akan direset ke awal
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    # RESET
                    game.player = -1
                    game.reset()
                    game.gamemode = 'ai'
                    ai = game.ai

    pygame.display.update()
    #diupdate
