import pygame
from utils import Button, labels
from score import calculate_score


def game_display_setup(args, timer, screen, fps, score, img_ID, mode, ans_dict = None, imgs = None):
        
        pygame.font.init()

        people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0

        screen.fill('white')
        timer.tick(fps)
        
        # Buttons for '+' (text, x_pos, y_pos)
        add_button1 = Button('+', args.add_pos_x, args.start_ypos)
        add_button2 = Button('+', args.add_pos_x, args.start_ypos + args.delta)
        add_button3 = Button('+', args.add_pos_x, args.start_ypos + 2*args.delta)
        add_button4 = Button('+', args.add_pos_x, args.start_ypos + 3*args.delta)
        add_button5 = Button('+', args.add_pos_x, args.start_ypos + 4*args.delta)
            
        #+ buttons only increase counts up to 5
        if add_button1.check_click():
            if people_val < 5:
                people_val += 1
        elif add_button2.check_click():
            if vehicle_val < 5:
                vehicle_val += 1
        elif add_button3.check_click():
            if bags_val < 5:
                bags_val += 1
        elif add_button4.check_click():
            if barrels_val < 5:
                barrels_val += 1
        elif add_button5.check_click():
            if antennas_val < 5:
                antennas_val += 1     
            
        # Buttons for '-' (text, x_pos, y_pos)
        sub_button1 = Button('-', args.sub_pos_x, args.start_ypos)
        sub_button2 = Button('-', args.sub_pos_x, args.start_ypos + args.delta)
        sub_button3 = Button('-', args.sub_pos_x, args.start_ypos + 2*args.delta)
        sub_button4 = Button('-', args.sub_pos_x, args.start_ypos + 3*args.delta)
        sub_button5 = Button('-', args.sub_pos_x, args.start_ypos + 4*args.delta)

        #- buttons only decrease counts down to 0
        if sub_button1.check_click():
            if people_val > 0:
                people_val -= 1
        elif sub_button2.check_click():
            if vehicle_val > 0:
                vehicle_val -= 1
        elif sub_button3.check_click():
            if bags_val > 0:
                bags_val -= 1
        elif sub_button4.check_click():
            if barrels_val > 0:
                barrels_val -= 1
        elif sub_button5.check_click():
            if antennas_val > 0:
                antennas_val -= 1

        # Rectangles for count of each object type. These will not be clicked on so no need to store Button class object
        Button(str(people_val), args.label_xpos, args.label_start_ypos)
        Button(str(vehicle_val), args.label_xpos, args.label_start_ypos + args.delta)
        Button(str(bags_val), args.label_xpos, args.label_start_ypos + 2*args.delta)
        Button(str(barrels_val), args.label_xpos, args.label_start_ypos + 3*args.delta)
        Button(str(antennas_val), args.label_xpos, args.label_start_ypos + 4*args.delta)

        # Button for Next
        x_pos = args.label_xpos     # Store the x position for the Next button 
        y_pos = args.label_start_ypos + 4*args.delta    # Store the y position for the Next button
        next_button = Button('Next', x_pos + 80, y_pos + 100)   # The values 80 & 100 are the deltas for x & y position respectively, change if reuqired
            
        #labels for target object types, 'score' and score value
        labels(args, screen, score)

        screen.blit(imgs[img_ID], (args.img_pos_x, args.img_pos_y)) # display the current real image

                #when Next button is clicked, update the score and show next image
        if next_button.check_click():
            new_points = calculate_score(img_ID, people_val, vehicle_val, bags_val, barrels_val, antennas_val, mode, score, ans_dict)
            score += new_points
                
            img_ID += 1 #incrememnt the img_ID
            #if last real image, reset img_ID back to 0 to loop through images again
            if img_ID >= len(imgs):
                img_ID = 0
                screen.blit(imgs[img_ID], (args.img_pos_x, args.img_pos_y))
            else:
                screen.blit(imgs[img_ID], (args.img_pos_x, args.img_pos_y)) # display the next image

        return