import pygame
import pandas as pd

class Button:
    def __init__(self, screen, text, x_pos, y_pos):
        self.text = text #the text to display over the button
        self.x_pos = x_pos #the x pos of the upper left corner of the button
        self.y_pos = y_pos #the y pos of the upper left corner of the button
        self.screen = screen
        self.draw() #function to draw the button and add text
    
    def draw(self):
        # For + and - buttons
        if self.text == '+' or self.text == '-':
            # Font type and Size
            font = pygame.font.SysFont('Arial MS', 80)
            button_text = font.render(self.text, True, 'black') #draw text on new surface with specified text color. True is for antialiasing, meaning characters have smooth edges.
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (75, 75)) #create rect object
            pygame.draw.rect(self.screen, 'sky blue', button_rect, 0, 5) #draw color filled rect to screen. 4th parameter is 0 to fill or 1 for outline in specified color. 5th parameter is rounding of corners.
            
            # Switch Condition for + or - label
            if self.text == '+':
                self.screen.blit(button_text, (self.x_pos + 22, self.y_pos + 8)) #copy text surface object to screen at this location
            elif self.text == '-':
                self.screen.blit(button_text, (self.x_pos + 29, self.y_pos + 12))
        
        # For Next button
        elif self.text == 'Next':
            # Font type and Size
            font = pygame.font.SysFont('Arial MS', 60)
            button_text = font.render(self.text, True, 'black')
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (155, 60))
            pygame.draw.rect(self.screen, 'gray', button_rect, 0, 5)
            pygame.draw.rect(self.screen, 'black', button_rect, 1, 5)
            self.screen.blit(button_text, (self.x_pos + 33, self.y_pos + 13))
        
        # For Training button
        elif self.text == 'Training':
            # Font type and Size
            font = pygame.font.SysFont('Arial MS', 80)
            button_text = font.render(self.text, True, 'black')
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (575, 100))
            pygame.draw.rect(self.screen, 'white', button_rect, 0, 5)
            pygame.draw.rect(self.screen, 'black', button_rect, 1, 5)
            self.screen.blit(button_text, (self.x_pos + 180, self.y_pos + 30))
        
        # For Start button
        elif self.text == 'Start':
            # Font type and size
            font = pygame.font.SysFont('Arial MS', 100)
            button_text = font.render(self.text, True, 'black')
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (575, 100))
            pygame.draw.rect(self.screen, 'green', button_rect, 0, 5)
            pygame.draw.rect(self.screen, 'black', button_rect, 2, 5)
            self.screen.blit(button_text, (self.x_pos + 220, self.y_pos + 20))
        

        # For object type rectangles to hold count values
        else:
            # Font type and Size
            font = pygame.font.SysFont('Arial MS', 60)
            button_text = font.render(self.text, True, 'black') #this is the count of the object type
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (85, 45))
            pygame.draw.rect(self.screen, 'white', button_rect, 0, 5)
            pygame.draw.rect(self.screen, 'black', button_rect, 1, 5)
            self.screen.blit(button_text, (self.x_pos + 32, self.y_pos + 5))

    def check_click(self): #check if a button was clicked
        global new_press
        mouse_pos = pygame.mouse.get_pos() #get (x,y) mouse cursor position relative to top-left screen corner
        left_click = pygame.mouse.get_pressed()[0] #gets boolean of left mouse button being clicked

        if self.text == 'Training' or self.text == 'Start':
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (575, 100)) #rect object the same size as the training or start buttons
        elif self.text == '+' or self.text == '-':
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (75, 75)) #rect object the same size as the - or + buttons
        else: #Next button
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (155, 60)) #rect object the same size as the next button
        
        if left_click and button_rect.collidepoint(mouse_pos) and new_press:
            #the mouse was clicked over a button and it is a new button press
            new_press = False #reset to True in loop when mouse button is released
            return True
        else:
            return False
    
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
    
# Function defines the labels and buttons for the Main Menu screen
def menu_setup(args, screen, subID_text_input, conditionNo_text_input, subID_rect, conditionNo_rect):
    # creates the labels and buttons for the menu
    font = pygame.font.Font(args.font_type, args.font_size)
    # Draw rectangle and empty text for sub_ID
    pygame.draw.rect(screen, 'white', subID_rect, 0, 5) #draw white filled rect to screen. 4th parameter is 0 to fill or 1 for outline in specified color. 5th parameter is rounding of corners.
    pygame.draw.rect(screen, 'black', subID_rect, 1, 5) #draw black border around rect.
    subID_text = font.render(subID_text_input, True, 'black') #draw text on new surface with specified text color. True is for antialiasing, meaning characters have smooth edges.
    screen.blit(subID_text, (subID_rect.x + 20, subID_rect.y + 10)) #copy text surface object to screen at this location

    # Draw rectangle and empty text for Condition No.
    pygame.draw.rect(screen, 'white', conditionNo_rect, 0, 5)
    pygame.draw.rect(screen, 'black', conditionNo_rect, 1, 5)
    conditionNo_text = font.render(conditionNo_text_input, True, 'black')
    screen.blit(conditionNo_text, (conditionNo_rect.x + 20, conditionNo_rect.y + 10))

    # Label for user input boxes
    subID_label = args.font_type.render('Subject ID', True, 'black')
    screen.blit(subID_label, (28, 88))
    conditionNo_label = font.render('Condition No', True, 'black')
    screen.blit(conditionNo_label, (390, 88))

    # Training Button
    training_button = Button('Training', 28, 200)
    
    #Start Button
    start_button = Button('Start', 28, 400)

    return training_button, start_button