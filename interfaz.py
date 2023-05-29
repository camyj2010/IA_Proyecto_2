import pygame, sys
from button import Button
import tkinter as tk
from tkinter import filedialog, messagebox
from dropdown import DropDown

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

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if PLAY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    if DROPDOWN_LEVEL.main == "Beginner" and count==0:
                        print("Beginner")
                    if DROPDOWN_LEVEL.main == "Amateur" and count==0:
                        print("Amateur")
                    if DROPDOWN_LEVEL.main == "Expert" and count==0:
                        print("Expert")


        # DIBUJO DEL TABLERO
        NUMBERS = [(2,3), (1,4), (7,5), (5,6), (1,3), (4,5), (6,4)]
        POS_W = (0,0)
        POS_B = (7,2)
        
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                POS_I = i*CELL_WIDTH
                POS_J = j*CELL_HEIGHT
                rect = pygame.Rect(POS_I+340, POS_J+60, CELL_WIDTH, CELL_HEIGHT)
                if (i+j)%2 == 0:
                    pygame.draw.rect(SCREEN, (240, 210, 185), rect) # Dibuja el cuadro blanco
                else:
                    pygame.draw.rect(SCREEN, (65, 60, 55), rect) # Dibuja el cuadro negro
                
                if (i,j) == POS_W:
                    SCREEN.blit(knight_W, (POS_I+345, POS_J+65))
                elif (i,j) == POS_B:
                    SCREEN.blit(knight_B, (POS_I+345, POS_J+65))
                
                pygame.draw.rect(SCREEN, (0, 0, 0), rect, 1) # Dibuja el borde negro

        for i in range(len(NUMBERS)):
            POS_I = NUMBERS[i][0] * CELL_WIDTH
            POS_J = NUMBERS[i][1] * CELL_HEIGHT
            draw_text(POS_I+377, POS_J+97, str(i+1), "Black", 30, SCREEN)


        # Actualizar el dropdown del tipo de algoritmo 
        selected_alg = DROPDOWN_LEVEL.update(event_list)
        if selected_alg >= 0:
            count=0
            DROPDOWN_LEVEL.main = DROPDOWN_LEVEL.options[selected_alg]
        event_list = pygame.event.get()

        pygame.display.update()
    
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