# Contains functions which setup the screen display for the Training and Real Quiz game sessions.

import pygame
from utils import Button


class Game_Disp_Setup:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def add_buttons(args, screen):
        # Buttons for '+' (text, x_pos, y_pos)
        add_button1 = Button(screen, '+', args.add_pos_x, args.start_ypos)
        add_button2 = Button(screen, '+', args.add_pos_x, args.start_ypos + args.delta)
        add_button3 = Button(screen, '+', args.add_pos_x, args.start_ypos + 2*args.delta)
        add_button4 = Button(screen, '+', args.add_pos_x, args.start_ypos + 3*args.delta)
        add_button5 = Button(screen, '+', args.add_pos_x, args.start_ypos + 4*args.delta)

        add_button_list = [add_button1, add_button2, add_button3, add_button4, add_button5]

        return add_button_list
    
    @staticmethod
    def subtract_buttons(args, screen):
        # Buttons for '-' (text, x_pos, y_pos)
        sub_button1 = Button(screen, '-', args.sub_pos_x, args.start_ypos)
        sub_button2 = Button(screen, '-', args.sub_pos_x, args.start_ypos + args.delta)
        sub_button3 = Button(screen, '-', args.sub_pos_x, args.start_ypos + 2*args.delta)
        sub_button4 = Button(screen, '-', args.sub_pos_x, args.start_ypos + 3*args.delta)
        sub_button5 = Button(screen, '-', args.sub_pos_x, args.start_ypos + 4*args.delta)

        sub_button_list = [sub_button1, sub_button2, sub_button3, sub_button4, sub_button5]

        return sub_button_list

    @staticmethod
    def count_object_labels(args, screen, obj_scores):
         
        # Rectangles for count of each object type. These will not be clicked on so no need to store Button class object
        Button(screen, str(obj_scores[0]), args.label_xpos, args.label_start_ypos)
        Button(screen, str(obj_scores[1]), args.label_xpos, args.label_start_ypos + args.delta)
        Button(screen, str(obj_scores[2]), args.label_xpos, args.label_start_ypos + 2*args.delta)
        Button(screen, str(obj_scores[3]), args.label_xpos, args.label_start_ypos + 3*args.delta)
        Button(screen, str(obj_scores[4]), args.label_xpos, args.label_start_ypos + 4*args.delta)
    
    @staticmethod
    #creates all text labels for target objects and score
    def labels(args, screen, score):
        # Font size and type for target object labels
        font = pygame.font.SysFont(args.font_type, 40)
        # Label for Object Names
        people_label = font.render('People', True, 'black')
        screen.blit(people_label, (996, 80))
        vehicles_label = font.render('Vehicles', True, 'black')
        screen.blit(vehicles_label, (983, 200))
        bags_label = font.render('Bags', True, 'black')
        screen.blit(bags_label, (1007, 320))
        barrels_label = font.render('Barrels', True, 'black')
        screen.blit(barrels_label, (992, 440))
        antennas_label = font.render('Antennas', True, 'black')
        screen.blit(antennas_label, (971, 560))
        
        # Label for 'Score'
        font = pygame.font.SysFont(args.font_type, 100)
        score_label = font.render('Score: ', True, 'dark green')
        screen.blit(score_label, (40, 40))

        #text for Score value
        score_text = font.render(str(score), True, 'dark green')
        screen.blit(score_text, (260, 40))

        return
