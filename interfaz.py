import pygame, sys
import time
from button import Button
import tkinter as tk
from tkinter import filedialog, messagebox
from dropdown import DropDown

# Minimax
from minimax import *
from utils import *

pygame.init()

# Constantes de juego
BOARD_SIZE = 8
knight_N=2
CELL_WIDTH = 75
CELL_HEIGHT = 75

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.transform.scale(pygame.image.load("images/chees.jpg"),(int(1280), int(720)))
knight_W=pygame.transform.scale(pygame.image.load("images/strategy_white.png"), (int(CELL_WIDTH-10), int(CELL_HEIGHT-10)))
knight_B=pygame.transform.scale(pygame.image.load("images/strategy_black.png"), (int(CELL_WIDTH-10), int(CELL_HEIGHT-10)))




# Funcion que dibuja un texto
def draw_text(x, y, string, col, size, window, number=1):
    font = get_font(size)
    text = font.render(string, True, col)
    textbox = text.get_rect(center=(x,y))
    window.blit(text, textbox)
    
# Funcion que devuelve una fuente de texto
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("fonts/Montserrat-Bold.ttf", size)

# Menu de juego
def play():
     # Colores de los Dropdown
    COLOR_INACTIVE = (85, 85, 85)
    COLOR_ACTIVE = (149, 149, 149)
    COLOR_LIST_INACTIVE = (85, 85, 85)
    COLOR_LIST_ACTIVE = (149, 149, 149)
    # Dropdown de seleccion de tipo de busqueda (informada o no informada)
    DROPDOWN_LEVEL= DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        150, 300, 170, 50, 
        pygame.font.SysFont(None, 30), 
        "Select level", ["Beginner", "Amateur","Expert"])
    
   
    PLAYER1_POS, PLAYER2_POS, BOARD = init_game()
    #print(PLAYER1_POS)
    #print(PLAYER1_POS[1])
    PLAYER1_SCORE = 0
    PLAYER2_SCORE = 0

    turn = 1

    # Para verificar si el jugador hace click en el caballo
    clicked = False
    
    count = -1
    countp1=1
    depth=0
    oldposition=PLAYER1_POS

    while True:
        
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BG= pygame.transform.scale(pygame.image.load("images/background.jpg"),(int(1280), int(720)))
        SCREEN.blit(PLAY_BG, (0, 0)) 


        PLAY_BACK = Button(image=pygame.transform.scale(pygame.image.load("images/Play_rect.png"),(int(250), int(125))), pos=(1100, 600), 
                            text_input="BACK", font=get_font(40), base_color="#FFFFFF", hovering_color="#87CEEB")

        PLAY_BACK.changeColor( PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("images/Play_rect3.png"),(int(200), int(70))), pos=(150, 450), 
                            text_input="PLAY", font=get_font(30), base_color="#FFFFFF", hovering_color="#555555")

        PLAY_BUTTON.changeColor( PLAY_MOUSE_POS)
        PLAY_BUTTON.update(SCREEN)
        RESTART_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("images/Play_rect3.png"),(int(200), int(70))), pos=(150, 520), 
                            text_input="RESTART", font=get_font(30), base_color="#FFFFFF", hovering_color="#555555")

        RESTART_BUTTON.changeColor( PLAY_MOUSE_POS)
        RESTART_BUTTON.update(SCREEN)
        DROPDOWN_LEVEL.draw(SCREEN)

        # Tarjeta del jugador 1
        rect1 = pygame.Rect(20, 60, 300, 200)
        pygame.draw.rect(SCREEN, (65, 60, 55), rect1, 0, 25, 25)
        # Imagen
        SCREEN.blit(knight_W, (40, 80))
        draw_text(200, 115, "Player 1", "White", 30, SCREEN) # Texto

        # Tarjeta del jugador 2
        rect2 = pygame.Rect(960, 60, 300, 200)
        pygame.draw.rect(SCREEN, (65, 60, 55), rect2, 0, 25, 25)
        # Imagen
        SCREEN.blit(knight_B, (980, 80))
        draw_text(1140, 115, "Player 2", "White", 30, SCREEN) # Texto

        #Textos
        draw_text(115, 200, "Points:", "White", 30, SCREEN)
        draw_text(80, 320, "Level:", "White", 30, SCREEN)
        draw_text(1065, 200, "Points:", "White", 30, SCREEN)

        #Puntajes
        draw_text(215, 200, str(PLAYER1_SCORE), "White", 30, SCREEN)
        draw_text(1165, 200, str(PLAYER2_SCORE), "White", 30, SCREEN)
        

        # PINTA EL TABLERO
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                POS_I = i*CELL_WIDTH
                POS_J = j*CELL_HEIGHT
                rect = pygame.Rect(POS_I+340, POS_J+60, CELL_WIDTH, CELL_HEIGHT)
                if (i+j)%2 == 0:
                    pygame.draw.rect(SCREEN, (240, 210, 185), rect) # Dibuja el cuadro blanco
                else:
                    pygame.draw.rect(SCREEN, (65, 60, 55), rect) # Dibuja el cuadro negro
                
                if (i,j) == PLAYER1_POS:
                    SCREEN.blit(knight_W, (POS_I+345, POS_J+65))
                elif (i,j) == PLAYER2_POS:
                    SCREEN.blit(knight_B, (POS_I+345, POS_J+65))
                
                pygame.draw.rect(SCREEN, (0, 0, 0), rect, 1) # Dibuja el borde negro


        # PINTA LOS NUMEROS
        for i, pos in enumerate(BOARD):
            if pos != 0:
                POS_I = BOARD[i][0] * CELL_WIDTH
                POS_J = BOARD[i][1] * CELL_HEIGHT
                draw_text(POS_I+375, POS_J+95, str(i+1), "Black", 30, SCREEN)
                draw_text(POS_I+375, POS_J+99, str(i+1), "Black", 30, SCREEN)
                draw_text(POS_I+379, POS_J+95, str(i+1), "Black", 30, SCREEN)
                draw_text(POS_I+379, POS_J+99, str(i+1), "Black", 30, SCREEN)
                draw_text(POS_I+377, POS_J+97, str(i+1), "White", 30, SCREEN)

        if count==0 and depth!=0:
            gameminimax=Game(PLAYER1_POS,PLAYER2_POS,BOARD)
            PLAYER1_POS=minimax(gameminimax,depth)
            index = check_move(BOARD, PLAYER1_POS)
            if index != None:
                        PLAYER1_SCORE += index+1
                        BOARD[index] = 0

            #oldposition=PLAYER2_POS
            count = 1

         # Todos los movimientos posibles para el J2
        if count == 1:    
            moves = get_all_moves(PLAYER2_POS, PLAYER1_POS)
            # PINTA EL RECUADRO VERDE DE LOS POSIBLES MOVIMIENTOS
            if clicked:
                for move in moves:
                    POS_I = move[0]*CELL_WIDTH
                    POS_J = move[1]*CELL_HEIGHT
                    rect = pygame.Rect(POS_I+340, POS_J+60, CELL_WIDTH, CELL_HEIGHT)
                    pygame.draw.rect(SCREEN, (0, 255, 0), rect, 5)

                countp1=0

            

        # EVENTOS
        event_list = pygame.event.get()
        x, y = pygame.mouse.get_pos()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if PLAY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                
                    if DROPDOWN_LEVEL.main == "Beginner" :
                        print("Beginner")
                        depth=2

                    if DROPDOWN_LEVEL.main == "Amateur" :
                        print("Amateur")
                        depth=4
                    if DROPDOWN_LEVEL.main == "Expert" :
                        print("Expert")
                        depth=6
                    count=0

                # Si el jugador hace click en el caballo
                if PLAYER2_POS[0]*CELL_WIDTH+340 <= x <= PLAYER2_POS[0]*CELL_WIDTH+340+CELL_WIDTH and \
                PLAYER2_POS[1]*CELL_HEIGHT+60 <= y <= PLAYER2_POS[1]*CELL_HEIGHT+60+CELL_HEIGHT:
                    clicked = clicked ^ True

                # Si el jugador hace click en una casilla verde
                if clicked and countp1==0:
                
                    for move in moves:
                        if move != 0:
                            POS_I = move[0]*CELL_WIDTH+340
                            POS_J = move[1]*CELL_HEIGHT+60

                            print(PLAYER2_POS)
                            print(PLAYER1_POS)
                            if POS_I <= x <= POS_I+CELL_WIDTH and POS_J <= y <= POS_J+CELL_HEIGHT :
                                # Se verifica si el movimiento da puntos
                                index = check_move(BOARD, move)


                                # ESTO TOCA CAMBIARLO LUEGO
                                # ES SOLO DE PRUEBA
                                if index != None:
                                    PLAYER2_SCORE += index+1
                                    BOARD[index] = 0

                                PLAYER2_POS = move
                                print(BOARD)
                                print (PLAYER2_POS)
                                clicked = False
                                
                                turn = 1
                                # time.sleep(10)

                                
                                break
                    
                    countp1=1
                    if countp1==1 and depth!=0:
                        countp1=2
                        count = 2

        


        selected_alg = DROPDOWN_LEVEL.update(event_list)
        if selected_alg >= 0:
            count=0
            DROPDOWN_LEVEL.main = DROPDOWN_LEVEL.options[selected_alg]
        event_list = pygame.event.get()


        pygame.display.update()
        
        if countp1==2 and depth!=0:
            countp1=1
            count = 0
    
#Funcion de la pestaña de creditos
def credits():
    # sound.stop()
    # sound.play()
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0)) 

        draw_text(642, 118, "CREDITS", "White", 120, SCREEN)
        draw_text(642, 122, "CREDITS", "White", 120, SCREEN)
        draw_text(638, 118, "CREDITS", "White", 120, SCREEN)
        draw_text(638, 122, "CREDITS", "White", 120, SCREEN)
        draw_text(640, 120, "CREDITS", "Black", 120, SCREEN)

        draw_text(642, 298, "Valery Molina Burgos", "White", 40, SCREEN)
        draw_text(642, 302, "Valery Molina Burgos", "White", 40, SCREEN)
        draw_text(638, 298, "Valery Molina Burgos", "White", 40, SCREEN)
        draw_text(638, 302, "Valery Molina Burgos", "White", 40, SCREEN)
        draw_text(640, 300, "Valery Molina Burgos", "Black", 40, SCREEN)

        draw_text(642, 378, "Maria Camila Jaramilo Andrade", "White",40, SCREEN)
        draw_text(642, 382, "Maria Camila Jaramilo Andrade", "White", 40, SCREEN)
        draw_text(638, 378, "Maria Camila Jaramilo Andrade", "White", 40, SCREEN)
        draw_text(638, 382, "Maria Camila Jaramilo Andrade", "White", 40, SCREEN)
        draw_text(640, 380, "Maria Camila Jaramilo Andrade", "Black", 40, SCREEN)

        draw_text(642, 458, "Juan Esteban Betancourt Narvaez", "White", 40, SCREEN)
        draw_text(642, 462, "Juan Esteban Betancourt Narvaez", "White", 40, SCREEN)
        draw_text(638, 462, "Juan Esteban Betancourt Narvaez", "White", 40, SCREEN)
        draw_text(638, 458, "Juan Esteban Betancourt Narvaez", "White", 40, SCREEN)
        draw_text(640, 460, "Juan Esteban Betancourt Narvaez", "Black", 40, SCREEN)


        OPTIONS_BACK = Button(image=pygame.transform.scale(pygame.image.load("images/Play_rect.png"),(int(250), int(125))), pos=(900, 600), 
                            text_input="BACK", font=get_font(40), base_color="#FFFFFF", hovering_color="#87CEEB")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()



        
def main_menu():
     
     while True:
        
        SCREEN.blit(BG, (0, 0)) 
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        draw_text(648, 122, "Smart Horses", "White", 150, SCREEN)
        draw_text(648, 118, "Smart Horses", "White", 150, SCREEN)
        draw_text(652, 118, "Smart Horses", "White", 150, SCREEN)
        draw_text(652, 122, "Smart Horses", "White", 150, SCREEN)
        draw_text(650, 120, "Smart Horses", "Black", 150, SCREEN)

        
        #Botones de las pantallas 
        
        PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("images/Play_rect.png"),(int(250), int(125))), pos=(400, 600), 
                            text_input="PLAY", font=get_font(40), base_color="#FFFFFF", hovering_color="#87CEEB")
        
        CREDIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("images/Play_rect.png"),(int(250), int(125))), pos=(900, 600), 
                            text_input="CREDITS", font=get_font(40), base_color="#FFFFFF", hovering_color="#87CEEB")
        
        
    
        
        for button in [PLAY_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for button in [CREDIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if CREDIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    credits()
               

        pygame.display.update()
 


main_menu()