# Contains fucntions to draw buttons, check which mouse button is clicked and setup the menu screen

import pygame
from mouse import Mouse

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

    def check_click(self, new_press, args): #check if a button was clicked
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
            #Mouse.write_mouse_pos(args, mouse_pos) #??? new_press = False #reset to True in loop when mouse button is released
            return True
        else:
            return False
    
# Function defines the labels and buttons for the Main Menu screen
def menu_setup(args, screen, ex_img, subID_text_input, condition_text_input, subID_rect, condition_rect):
    # creates the labels and buttons for the menu
    font = pygame.font.Font(args.font_type, args.font_size)
    # Draw rectangle and empty text for sub_ID
    pygame.draw.rect(screen, 'white', subID_rect, 0, 5) #draw white filled rect to screen. 4th parameter is 0 to fill or 1 for outline in specified color. 5th parameter is rounding of corners.
    pygame.draw.rect(screen, 'black', subID_rect, 1, 5) #draw black border around rect.
    subID_text = font.render(subID_text_input, True, 'black') #draw text on new surface with specified text color. True is for antialiasing, meaning characters have smooth edges.
    screen.blit(subID_text, (subID_rect.x + 20, subID_rect.y + 10)) #copy text surface object to screen at this location

    # Draw rectangle and empty text for Condition
    pygame.draw.rect(screen, 'white', condition_rect, 0, 5)
    pygame.draw.rect(screen, 'black', condition_rect, 1, 5)
    condition_text = font.render(condition_text_input, True, 'black')
    screen.blit(condition_text, (condition_rect.x + 20, condition_rect.y + 10))

    # Label for user input boxes
    subID_label = font.render('Subject ID', True, 'black')
    screen.blit(subID_label, (28, 88))
    condition_label = font.render('Condition', True, 'black')
    screen.blit(condition_label, (360, 88))

    # Training Button
    training_button = Button(screen, 'Training', 28, 200) #??? these should be args
    
    # Start Button
    start_button = Button(screen, 'Start', 28, 400)

    #Examples of target objects image
    screen.blit(ex_img, (680, 160))

    return training_button, start_button