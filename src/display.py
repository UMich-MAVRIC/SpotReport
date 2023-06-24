import pygame

# Contains fucntions to draw buttons and check whether a button has been clicked
class Button:
    def __init__(self, args, screen, text, x_pos, y_pos):
        self.text = text #the text to display over the button
        self.x_pos = x_pos #the x pos of the upper left corner of the button
        self.y_pos = y_pos #the y pos of the upper left corner of the button
        self.screen = screen
        self.draw(args) #function to draw the button and add text
    
    def draw(self, args):
        # For + and - buttons
        if self.text == '+' or self.text == '-':
            # Font type and Size
            font = pygame.font.SysFont(args.font_type, 80)
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
            font = pygame.font.SysFont(args.font_type, 60)
            button_text = font.render(self.text, True, 'black')
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (155, 60))
            pygame.draw.rect(self.screen, 'gray', button_rect, 0, 5)
            pygame.draw.rect(self.screen, 'black', button_rect, 1, 5)
            self.screen.blit(button_text, (self.x_pos + 33, self.y_pos + 13))
        
        # For Training button
        elif self.text == 'Training':
            # Font type and Size
            font = pygame.font.SysFont(args.font_type, 80)
            button_text = font.render(self.text, True, 'black')
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (575, 100))
            pygame.draw.rect(self.screen, 'white', button_rect, 0, 5)
            pygame.draw.rect(self.screen, 'black', button_rect, 1, 5)
            self.screen.blit(button_text, (self.x_pos + 180, self.y_pos + 30))
        
        # For Start button
        elif self.text == 'Start':
            # Font type and size
            font = pygame.font.SysFont(args.font_type, 100)
            button_text = font.render(self.text, True, 'black')
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (575, 100))
            pygame.draw.rect(self.screen, 'green', button_rect, 0, 5)
            pygame.draw.rect(self.screen, 'black', button_rect, 2, 5)
            self.screen.blit(button_text, (self.x_pos + 220, self.y_pos + 20))
        
        # For object type rectangles to hold count values
        else:
            # Font type and Size
            font = pygame.font.SysFont(args.font_type, 60)
            button_text = font.render(self.text, True, 'black') #this is the count of the object type
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (85, 45))
            pygame.draw.rect(self.screen, 'white', button_rect, 0, 5)
            pygame.draw.rect(self.screen, 'black', button_rect, 1, 5)
            self.screen.blit(button_text, (self.x_pos + 32, self.y_pos + 5))

    def check_click(self, new_press): #check if a button was clicked
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
            return True
        else:
            return False
    

# Function defines the labels and buttons for the Menu screen
def menu_setup(args, screen, ex_img, subID_text_input, condition_text_input, subID_rect, condition_rect):
    # creates the labels and buttons for the menu
    font = pygame.font.SysFont(args.font_type, 30)
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
    training_button = Button(args, screen, 'Training', 28, 200)
    
    # Start Button
    start_button = Button(args, screen, 'Start', 28, 400)

    #Examples of target objects image
    screen.blit(ex_img, (680, 160))

    return training_button, start_button


# Contains functions which setup the screen display for the training and task spot report
class Disp_Setup:
    def __init__(self) -> None:
        pass
    
    @staticmethod #function that belongs to a class but doesn't access any properties of that class
    def add_buttons(args, screen):
        # Buttons for '+' (text, x_pos, y_pos)
        add_button1 = Button(args, screen, '+', args.add_xpos, args.add_sub_ypos)
        add_button2 = Button(args, screen, '+', args.add_xpos, args.add_sub_ypos + args.delta)
        add_button3 = Button(args, screen, '+', args.add_xpos, args.add_sub_ypos + 2*args.delta)
        add_button4 = Button(args, screen, '+', args.add_xpos, args.add_sub_ypos + 3*args.delta)
        add_button5 = Button(args, screen, '+', args.add_xpos, args.add_sub_ypos + 4*args.delta)

        add_button_list = [add_button1, add_button2, add_button3, add_button4, add_button5]

        return add_button_list
    
    @staticmethod
    def subtract_buttons(args, screen):
        # Buttons for '-' (text, x_pos, y_pos)
        sub_button1 = Button(args, screen, '-', args.sub_xpos, args.add_sub_ypos)
        sub_button2 = Button(args, screen, '-', args.sub_xpos, args.add_sub_ypos + args.delta)
        sub_button3 = Button(args, screen, '-', args.sub_xpos, args.add_sub_ypos + 2*args.delta)
        sub_button4 = Button(args, screen, '-', args.sub_xpos, args.add_sub_ypos + 3*args.delta)
        sub_button5 = Button(args, screen, '-', args.sub_xpos, args.add_sub_ypos + 4*args.delta)

        sub_button_list = [sub_button1, sub_button2, sub_button3, sub_button4, sub_button5]

        return sub_button_list

    @staticmethod
    def count_object_labels(args, screen, obj_vals):
        # Rectangles for count of each object type. These will not be clicked on so no need to store Button class object
        Button(args, screen, str(obj_vals[0]), args.label_xpos, args.label_ypos) # user count for people
        Button(args, screen, str(obj_vals[1]), args.label_xpos, args.label_ypos + args.delta) # user count for vehicles
        Button(args, screen, str(obj_vals[2]), args.label_xpos, args.label_ypos + 2*args.delta) # user count for bags
        Button(args, screen, str(obj_vals[3]), args.label_xpos, args.label_ypos + 3*args.delta) # user count for barrels
        Button(args, screen, str(obj_vals[4]), args.label_xpos, args.label_ypos + 4*args.delta) # user count for antennas
    
        return
    
    @staticmethod
    def labels(args, screen, score):
        #creates all text labels for target objects and score
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