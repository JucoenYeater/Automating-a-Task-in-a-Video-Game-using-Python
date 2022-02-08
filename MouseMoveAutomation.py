# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 04:11:55 2021

@author: jucoe
"""



"""
******NOTE: IMPORTANT INFORMATION******

Characters must be chosen in page location order or scipt won't work
For Example:
    If there is a character on page 2 slot 3 and another character on
    page 2 slot 5 then the page 2 slot 3 character needs to be chosen
    first. This is because of the way characters are listed in the
    character select screen. The characters are listed in order by
    most recently played


Location information (Note the locations are for windowed mode and 1920x1080)
    Character Slots
        Position 1: 1550, 195
        Subsequent Postions 1550, +70 per slot for 6 slots total per page
    Character Page Change Location
        Page Right: 1885, 663
        Page Left: 1525, 663
    Character Select Play Button
        "Play" button location: 1870, 840
"""

from numpy import arange, zeros, empty
from tkinter import Label, ttk, Tk, Button, messagebox
import time, pyautogui, sched


pyautogui.FAILSAFE = True  



        
#Variables
char = float(input("Input the amount of characters you intend to farm with (note: must be 30 or less): "))
rotations = float(input("Input the amount of rotations you intend to farm: "))
char_play = input("Will you be playing a non-farming character during the farm? ('y' or 'n'): ")

rewardclickrotation = 8
rewardclickperrotation = 5
charslotsperpage = 6


#Arrays
number_words = ("first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth",
                "ninth", "tenth", "eleventh", "twelvth", "thirteenth", "fourteenth",
                "fifteenth", "sixteenth", "seventeenth", "eighteenth", "nineteenth", "twentyith")



#Button Locations
#Character Selection Screen
y_dis = 70
char_slot_loc_x = 1550
char_slot_loc_y = (195, 195+(y_dis*1), 195+(y_dis*2), 195+(y_dis*3), 195+(y_dis*4), 195+(y_dis*5))
pageright_loc_x = 1885
pageright_loc_y = 663
pageleft_loc = (1525, 663)
#Crew Skills Window
crew_skill_y_distance = 70
crew_skill_loc_x = (150, 190, 230)
crew_skill_loc_y = (475, 475+(crew_skill_y_distance*1), 475+(crew_skill_y_distance*2), 475+(crew_skill_y_distance*3),
                    475, 475+(crew_skill_y_distance*1), 475+(crew_skill_y_distance*2), 475+(crew_skill_y_distance*3))
#Crew Missions Window
crew_mission_win_top = (500, 375)
crew_mission_win_bottom = (500, 625)
crew_mission_win_exit = (760,295)
#Legacy Bank right click Location
lb_rclick_loc = (1400, 600)
#Guild Bank close location
gb_close_loc = (655, 40)
#Legacy Bank button locations
lb_close_loc = (650, 75)
lb_slot_size = 41 #Length = Width
lb_slot_row1_col = (260,140)
lb_bay1_loc = (267,495)
lb_bay_tab_dis = 55
lb_slots_per_row = 10
#Legacy Bank Mission Locations (Ensure bank window is in top left corner of ui)
arc_miss_start_coords = (lb_slot_row1_col[0], lb_slot_row1_col[1])
bio_miss_start_coords = (lb_slot_row1_col[0], lb_slot_row1_col[1])
dip_miss_start_coords = (lb_slot_row1_col[0], lb_slot_row1_col[1]+(lb_slot_size*2))
inv_miss_start_coords = (lb_slot_row1_col[0], lb_slot_row1_col[1]+(lb_slot_size*2))
sca_miss_start_coords = (lb_slot_row1_col[0], lb_slot_row1_col[1]+(lb_slot_size*4))
sli_miss_start_coords = (lb_slot_row1_col[0], lb_slot_row1_col[1]+(lb_slot_size*6))
tre_miss_start_coords = (lb_slot_row1_col[0], lb_slot_row1_col[1]+(lb_slot_size*4))
und_miss_start_coords = (lb_slot_row1_col[0], lb_slot_row1_col[1]+(lb_slot_size*6))
#Increment tracking across characters and rotations for purp missions
inc_start = 0
arc_inc = inc_start
bio_inc = inc_start
dip_inc = inc_start
inv_inc = inc_start
sca_inc = inc_start
sli_inc = inc_start
tre_inc = inc_start
und_inc = inc_start
#Inventory Coordinates for purp mission
inv_slot_size = 41
inv_slot_row1_col1 = (1500,505)
inv_coords_skill1 = (inv_slot_row1_col1[0]+(inv_slot_size*7), inv_slot_row1_col1[1]+(inv_slot_size*4))
inv_coords_skill2 = (inv_slot_row1_col1[0]+(inv_slot_size*8), inv_slot_row1_col1[1]+(inv_slot_size*4))
inv_coords_skill3 = (inv_slot_row1_col1[0]+(inv_slot_size*9), inv_slot_row1_col1[1]+(inv_slot_size*4))




#Empty arrys for character page and slot numbers
char_page = arange(char)
char_slot = arange(char)
comp_amount = arange(char)
char_skills = arange(char)
char_time = arange(char)

char_crew_skill1_amount = arange(char)
char_crew_skill2_amount = arange(char)
char_crew_skill3_amount = arange(char)

purp_miss_skill1 = empty(int(char), dtype = str)
purp_miss_skill2 = empty(int(char), dtype = str)
purp_miss_skill3 = empty(int(char), dtype = str)
purp_skill1_amount = zeros(int(char))
purp_skill2_amount = zeros(int(char))
purp_skill3_amount = zeros(int(char))

skill1 = empty(int(char), dtype = "<U3")
skill2 = empty(int(char), dtype = "<U3")
skill3 = empty(int(char), dtype = "<U3")


#Takes user input for location of characters
for i in range(int(char)):
    char_page[i] = float(input("Input {} character's current page number: ".format(number_words[i])))
    char_slot[i] = float(input("Input {} character's current slot number (should be from 1 to 6): ".format(number_words[i])))
    char_crew_skill1_amount[i] = float(input("How many missions for 1st crew skill on {} character: ".format(number_words[i])))
    if char_crew_skill1_amount[i] != 0:
        purp_miss_skill1[i] = input("Will one of them be a purple mission from guild bank? (type Y or N for answer):  ")
        if purp_miss_skill1[i] == 'Y' or purp_miss_skill1[i] == 'y':
            skill1[i] = input("What is crew skill 1? (Use first three letters only): ")
            purp_skill1_amount[i] = float(input("How many rotations will 1st crew skill have a purple mission for the {} character".format(number_words[i])))
    char_crew_skill2_amount[i] = float(input("How many missions for 2nd crew skill on {} character: ".format(number_words[i])))
    if char_crew_skill2_amount[i] != 0:
        purp_miss_skill2[i] = input("Will one of them be a purple mission from guild bank? (type Y or N for answer):  ")
        if purp_miss_skill2[i] == 'Y' or purp_miss_skill2[i] == 'y':
            skill2[i] = input("What is crew skill 2? (Use first three letters only): ")
            purp_skill2_amount[i] = float(input("How many rotations will 2nd crew skill have a purple mission for the {} character".format(number_words[i])))
    char_crew_skill3_amount[i] =float(input("How many missions for 3rd crew skill on {} character: ".format(number_words[i])))
    if char_crew_skill3_amount[i] != 0:
        purp_miss_skill3[i] = input("Will one of them be a purple mission from guild bank? (type Y or N for answer):  ")
        if purp_miss_skill3[i] == 'Y' or purp_miss_skill3[i] == 'y':
            skill3[i] = input("What is crew skill 3? (Use first three letters only): ")
            purp_skill3_amount[i] = float(input("How many rotations will 3rd crew skill have a purple mission for the {} character".format(number_words[i])))
    
comp_amount = char_crew_skill1_amount + char_crew_skill2_amount + char_crew_skill3_amount




def crewskills_loc_x(x, y, z):
    locx = arange(x+y+z)
    for i in range(x+y+z):
        if x > 0 and i < x:
            locx[i] = crew_skill_loc_x[0]
        elif y > 0 and i >= x and i < (x+y):
            locx[i] = crew_skill_loc_x[1]
        elif z > 0 and i >= (x+y):
            locx[i] = crew_skill_loc_x[2]
    return locx


def show_msg():
    global char_play
    char_play = 'y'
    messagebox.showinfo("Log out scrub!")



s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    global n1,arc_inc,bio_inc,dip_inc,inv_inc,sca_inc,sli_inc,tre_inc,und_inc,coords,char_play
    print("Doing stuff...")
    for n in range(int(char)):
        time1 = time.time()
        clickx = crewskills_loc_x(int(char_crew_skill1_amount[n]),int(char_crew_skill2_amount[n]),int(char_crew_skill3_amount[n]))
        clicky = crew_skill_loc_y
        if char_page[n] > 1:
            for m in range(int(char_page[n])-1):
                pyautogui.click(pageright_loc_x, pageright_loc_y)
                time.sleep(0.5)
        pyautogui.click(char_slot_loc_x, char_slot_loc_y[int(char_slot[n]-1)], clicks=2)
        if char_play == 'y' or char_play == 'Y':
            char_slot[n] = (char+1) % charslotsperpage
            if (char+1) <= 6:
                char_page[n] = 1
            elif 7 <= (char+1) <= 12:
                char_page[n] = 2
            elif 12 <= (char+1) <= 18:
                char_page[n] = 3
            elif 19 <= (char+1) <= 24:
                char_page[n] = 4
            elif 25 <= (char+1) <= 30:
                char_page[n] = 5
        else:
            char_slot[n] = char % charslotsperpage
            if char <= 6:
                char_page[n] = 1
            elif 7 <= char <= 12:
                char_page[n] = 2
            elif 12 <= char <= 18:
                char_page[n] = 3
            elif 19 <= char <= 24:
                char_page[n] = 4
            elif 25 <= char <= 30:
                char_page[n] = 5
        
        time.sleep(20)
        pyautogui.press('space', presses=2, interval=2)
        time.sleep(8)
        pyautogui.hotkey('b')
        for m in range(rewardclickrotation+2):
            pyautogui.click(1850,320)
            pyautogui.click(1850,350)
            pyautogui.click(1850,380)
            pyautogui.click(1850,405)
            pyautogui.click(1850,430)
            pyautogui.click(1850,460)
            pyautogui.click(1850,490)
        pyautogui.click(1380, 225)
        time.sleep(0.5)
            
#Block to check for and place in inventory from legacy bank tab 1 and 2
#Each Gathering/Mission skill takes up two rows
        if purp_miss_skill1[n] == 'y' or purp_miss_skill2[n] == 'y' or purp_miss_skill3[n] == 'y':
            pyautogui.rightClick(lb_rclick_loc[0], lb_rclick_loc[1], duration=1)
            time.sleep(4)
        if n1 <= purp_skill1_amount[n]:
            if skill1[n] == 'arc':
                pyautogui.click(lb_bay1_loc[0]+(lb_bay_tab_dis),lb_bay1_loc[1])
                time.sleep(0.5)
                if arc_inc <= 9:
                    coords = (arc_miss_start_coords[0]+(lb_slot_size*arc_inc), arc_miss_start_coords[1])
                else:
                    coords = (arc_miss_start_coords[0]+(lb_slot_size*(arc_inc-lb_slots_per_row)), arc_miss_start_coords[1]+lb_slot_size)
                arc_inc += 1
            elif skill1[n] == 'bio':
                pyautogui.click(lb_bay1_loc[0],lb_bay1_loc[1])
                time.sleep(0.5)
                if bio_inc <= 9:
                    coords = (bio_miss_start_coords[0]+(lb_slot_size*bio_inc), bio_miss_start_coords[1])
                else:
                    coords = (bio_miss_start_coords[0]+(lb_slot_size*(bio_inc-lb_slots_per_row)), bio_miss_start_coords[1]+lb_slot_size)
                bio_inc += 1
            elif skill1[n] == 'dip':
                pyautogui.click(lb_bay1_loc[0],lb_bay1_loc[1])
                time.sleep(0.5)
                if dip_inc <= 9:
                    coords = (dip_miss_start_coords[0]+(lb_slot_size*dip_inc), dip_miss_start_coords[1])
                else:
                    coords = (dip_miss_start_coords[0]+(lb_slot_size*(dip_inc-lb_slots_per_row)), dip_miss_start_coords[1]+lb_slot_size)
                dip_inc += 1
            elif skill1[n] == 'inv':
                pyautogui.click(lb_bay1_loc[0]+(lb_bay_tab_dis),lb_bay1_loc[1])
                time.sleep(0.5)
                if inv_inc <= 9:
                    coords = (inv_miss_start_coords[0]+(lb_slot_size*inv_inc), inv_miss_start_coords[1])
                else:
                    coords = (inv_miss_start_coords[0]+(lb_slot_size*(inv_inc-lb_slots_per_row)), inv_miss_start_coords[1]+lb_slot_size)
                inv_inc += 1
            elif skill1[n] == 'sca':
                pyautogui.click(lb_bay1_loc[0],lb_bay1_loc[1])
                time.sleep(0.5)
                if sca_inc <= 9:
                    coords = (sca_miss_start_coords[0]+(lb_slot_size*sca_inc), sca_miss_start_coords[1])
                else:
                    coords = (sca_miss_start_coords[0]+(lb_slot_size*(sca_inc-lb_slots_per_row)), sca_miss_start_coords[1]+lb_slot_size)
                sca_inc += 1
            elif skill1[n] == 'sli':
                pyautogui.click(lb_bay1_loc[0],lb_bay1_loc[1])
                time.sleep(0.5)
                if sli_inc <= 9:
                    coords = (sli_miss_start_coords[0]+(lb_slot_size*sli_inc), sli_miss_start_coords[1])
                else:
                    coords = (sli_miss_start_coords[0]+(lb_slot_size*(sli_inc-lb_slots_per_row)), sli_miss_start_coords[1]+lb_slot_size)
                sli_inc += 1
            elif skill1[n] == 'tre':
                pyautogui.click(lb_bay1_loc[0]+(lb_bay_tab_dis),lb_bay1_loc[1])
                time.sleep(0.5)
                if tre_inc <= 9:
                    coords = (tre_miss_start_coords[0]+(lb_slot_size*tre_inc), tre_miss_start_coords[1])
                else:
                    coords = (tre_miss_start_coords[0]+(lb_slot_size*(tre_inc-lb_slots_per_row)), tre_miss_start_coords[1]+lb_slot_size)
                tre_inc += 1
            elif skill1[n] == 'und':
                pyautogui.click(lb_bay1_loc[0]+(lb_bay_tab_dis),lb_bay1_loc[1])
                time.sleep(0.5)
                if und_inc <= 9:
                    coords = (und_miss_start_coords[0]+(lb_slot_size*und_inc), und_miss_start_coords[1])
                else:
                    coords = (und_miss_start_coords[0]+(lb_slot_size*(und_inc-lb_slots_per_row)), und_miss_start_coords[1]+lb_slot_size)
                und_inc += 1
            time.sleep(0.5)
            pyautogui.click(coords[0], coords[1], button='left')
            time.sleep(0.5)
            pyautogui.click(inv_coords_skill1[0], inv_coords_skill1[1], button='left')
            time.sleep(0.5)
        if n1 <= purp_skill2_amount[n]:
            if skill2[n] == 'arc':
                pyautogui.click(lb_bay1_loc[0]+(lb_bay_tab_dis),lb_bay1_loc[1])
                time.sleep(0.5)
                if arc_inc <= 9:
                    coords = (arc_miss_start_coords[0]+(lb_slot_size*arc_inc), arc_miss_start_coords[1])
                else:
                    coords = (arc_miss_start_coords[0]+(lb_slot_size*(arc_inc-lb_slots_per_row)), arc_miss_start_coords[1]+lb_slot_size)
                arc_inc += 1
            elif skill2[n] == 'bio':
                pyautogui.click(lb_bay1_loc[0],lb_bay1_loc[1])
                time.sleep(0.5)
                if bio_inc <= 9:
                    coords = (bio_miss_start_coords[0]+(lb_slot_size*bio_inc), bio_miss_start_coords[1])
                else:
                    coords = (bio_miss_start_coords[0]+(lb_slot_size*(bio_inc-lb_slots_per_row)), bio_miss_start_coords[1]+lb_slot_size)
                bio_inc += 1
            elif skill2[n] == 'dip':
                pyautogui.click(lb_bay1_loc[0],lb_bay1_loc[1])
                time.sleep(0.5)
                if dip_inc <= 9:
                    coords = (dip_miss_start_coords[0]+(lb_slot_size*dip_inc), dip_miss_start_coords[1])
                else:
                    coords = (dip_miss_start_coords[0]+(lb_slot_size*(dip_inc-lb_slots_per_row)), dip_miss_start_coords[1]+lb_slot_size)
                dip_inc += 1
            elif skill2[n] == 'inv':
                pyautogui.click(lb_bay1_loc[0]+(lb_bay_tab_dis),lb_bay1_loc[1])
                time.sleep(0.5)
                if inv_inc <= 9:
                    coords = (inv_miss_start_coords[0]+(lb_slot_size*inv_inc), inv_miss_start_coords[1])
                else:
                    coords = (inv_miss_start_coords[0]+(lb_slot_size*(inv_inc-lb_slots_per_row)), inv_miss_start_coords[1]+lb_slot_size)
                inv_inc += 1
            elif skill2[n] == 'sca':
                pyautogui.click(lb_bay1_loc[0],lb_bay1_loc[1])
                time.sleep(0.5)
                if sca_inc <= 9:
                    coords = (sca_miss_start_coords[0]+(lb_slot_size*sca_inc), sca_miss_start_coords[1])
                else:
                    coords = (sca_miss_start_coords[0]+(lb_slot_size*(sca_inc-lb_slots_per_row)), sca_miss_start_coords[1]+lb_slot_size)
                sca_inc += 1
            elif skill2[n] == 'sli':
                pyautogui.click(lb_bay1_loc[0],lb_bay1_loc[1])
                time.sleep(0.5)
                if sli_inc <= 9:
                    coords = (sli_miss_start_coords[0]+(lb_slot_size*sli_inc), sli_miss_start_coords[1])
                else:
                    coords = (sli_miss_start_coords[0]+(lb_slot_size*(sli_inc-lb_slots_per_row)), sli_miss_start_coords[1]+lb_slot_size)
                sli_inc += 1
            elif skill2[n] == 'tre':
                pyautogui.click(lb_bay1_loc[0]+(lb_bay_tab_dis),lb_bay1_loc[1])
                time.sleep(0.5)
                if tre_inc <= 9:
                    coords = (tre_miss_start_coords[0]+(lb_slot_size*tre_inc), tre_miss_start_coords[1])
                else:
                    coords = (tre_miss_start_coords[0]+(lb_slot_size*(tre_inc-lb_slots_per_row)), tre_miss_start_coords[1]+lb_slot_size)
                tre_inc += 1
            elif skill2[n] == 'und':
                pyautogui.click(lb_bay1_loc[0]+(lb_bay_tab_dis),lb_bay1_loc[1])
                time.sleep(0.5)
                if und_inc <= 9:
                    coords = (und_miss_start_coords[0]+(lb_slot_size*und_inc), und_miss_start_coords[1])
                else:
                    coords = (und_miss_start_coords[0]+(lb_slot_size*(und_inc-lb_slots_per_row)), und_miss_start_coords[1]+lb_slot_size)
                und_inc += 1
            time.sleep(0.5)
            pyautogui.click(coords[0], coords[1], button='left')  
            time.sleep(0.5)
            pyautogui.click(inv_coords_skill2[0], inv_coords_skill2[1], button='left')
            time.sleep(0.5)
        if n1 <= purp_skill3_amount[n]:
            if skill3[n] == 'arc':
                pyautogui.click(lb_bay1_loc[0]+(lb_bay_tab_dis),lb_bay1_loc[1])
                time.sleep(0.5)
                if arc_inc <= 9:
                    coords = (arc_miss_start_coords[0]+(lb_slot_size*arc_inc), arc_miss_start_coords[1])
                else:
                    coords = (arc_miss_start_coords[0]+(lb_slot_size*(arc_inc-lb_slots_per_row)), arc_miss_start_coords[1]+lb_slot_size)
                arc_inc += 1
            elif skill3[n] == 'bio':
                pyautogui.click(lb_bay1_loc[0],lb_bay1_loc[1])
                time.sleep(0.5)
                if bio_inc <= 9:
                    coords = (bio_miss_start_coords[0]+(lb_slot_size*bio_inc), bio_miss_start_coords[1])
                else:
                    coords = (bio_miss_start_coords[0]+(lb_slot_size*(bio_inc-lb_slots_per_row)), bio_miss_start_coords[1]+lb_slot_size)
                bio_inc += 1
            elif skill3[n] == 'dip':
                pyautogui.click(lb_bay1_loc[0],lb_bay1_loc[1])
                time.sleep(0.5)
                if dip_inc <= 9:
                    coords = (dip_miss_start_coords[0]+(lb_slot_size*dip_inc), dip_miss_start_coords[1])
                else:
                    coords = (dip_miss_start_coords[0]+(lb_slot_size*(dip_inc-lb_slots_per_row)), dip_miss_start_coords[1]+lb_slot_size)
                dip_inc += 1
            elif skill3[n] == 'inv':
                pyautogui.click(lb_bay1_loc[0]+(lb_bay_tab_dis),lb_bay1_loc[1])
                time.sleep(0.5)
                if inv_inc <= 9:
                    coords = (inv_miss_start_coords[0]+(lb_slot_size*inv_inc), inv_miss_start_coords[1])
                else:
                    coords = (inv_miss_start_coords[0]+(lb_slot_size*(inv_inc-lb_slots_per_row)), inv_miss_start_coords[1]+lb_slot_size)
                inv_inc += 1
            elif skill3[n] == 'sca':
                pyautogui.click(lb_bay1_loc[0],lb_bay1_loc[1])
                time.sleep(0.5)
                if sca_inc <= 9:
                    coords = (sca_miss_start_coords[0]+(lb_slot_size*sca_inc), sca_miss_start_coords[1])
                else:
                    coords = (sca_miss_start_coords[0]+(lb_slot_size*(sca_inc-lb_slots_per_row)), sca_miss_start_coords[1]+lb_slot_size)
                sca_inc += 1
            elif skill3[n] == 'sli':
                pyautogui.click(lb_bay1_loc[0],lb_bay1_loc[1])
                time.sleep(0.5)
                if sli_inc <= 9:
                    coords = (sli_miss_start_coords[0]+(lb_slot_size*sli_inc), sli_miss_start_coords[1])
                else:
                    coords = (sli_miss_start_coords[0]+(lb_slot_size*(sli_inc-lb_slots_per_row)), sli_miss_start_coords[1]+lb_slot_size)
                sli_inc += 1
            elif skill3[n] == 'tre':
                pyautogui.click(lb_bay1_loc[0]+(lb_bay_tab_dis),lb_bay1_loc[1])
                time.sleep(0.5)
                if tre_inc <= 9:
                    coords = (tre_miss_start_coords[0]+(lb_slot_size*tre_inc), tre_miss_start_coords[1])
                else:
                    coords = (tre_miss_start_coords[0]+(lb_slot_size*(tre_inc-lb_slots_per_row)), tre_miss_start_coords[1]+lb_slot_size)
                tre_inc += 1
            elif skill3[n] == 'und':
                pyautogui.click(lb_bay1_loc[0]+(lb_bay_tab_dis),lb_bay1_loc[1])
                time.sleep(0.5)
                if und_inc <= 9:
                    coords = (und_miss_start_coords[0]+(lb_slot_size*und_inc), und_miss_start_coords[1])
                else:
                    coords = (und_miss_start_coords[0]+(lb_slot_size*(und_inc-lb_slots_per_row)), und_miss_start_coords[1]+lb_slot_size)
                und_inc += 1  
            time.sleep(0.5)
            pyautogui.click(coords[0], coords[1], button='left')   
            time.sleep(0.5)
            pyautogui.click(inv_coords_skill3[0], inv_coords_skill3[1], button='left')
            time.sleep(0.5)
        if purp_miss_skill1[n] == 'y' or purp_miss_skill2[n] == 'y' or purp_miss_skill3[n] == 'y':
            pyautogui.click(lb_close_loc[0], lb_close_loc[1])
            time.sleep(1)
            pyautogui.hotkey('i')
            time.sleep(1)
            
            
#Block executes appropriate purple missions in inventory
        if n1 <= purp_skill1_amount[n]:
            pyautogui.rightClick(inv_coords_skill1[0], inv_coords_skill1[1])
            time.sleep(purp_miss_cast_speed)
        if n1 <= purp_skill2_amount[n]:
            pyautogui.rightClick(inv_coords_skill2[0], inv_coords_skill2[1])
            time.sleep(purp_miss_cast_speed)
        if n1 <= purp_skill3_amount[n]:
            pyautogui.rightClick(inv_coords_skill3[0], inv_coords_skill3[1])
            time.sleep(purp_miss_cast_speed)
            
        
        
 #Block sends companions out on approrpriate crew skills       
        for m in range(int(comp_amount[n])):
            if m == 4:
                pyautogui.moveTo(clickx[m], clicky[m])
                pyautogui.scroll(-500)
            pyautogui.click(clickx[m], clicky[m])
            if clickx[m] > clickx[m-1]:
                time.sleep(0.5)
                pyautogui.click(crew_mission_win_exit[0], crew_mission_win_exit[1])
                pyautogui.click(clickx[m], clicky[m])
            if n1 <= purp_skill1_amount[n] and m == 0:
                time.sleep(0.5)
                pyautogui.moveTo(crew_mission_win_bottom[0], crew_mission_win_bottom[1])
                pyautogui.scroll(-15000)
                pyautogui.scroll(-15000)
                pyautogui.click(crew_mission_win_bottom[0], crew_mission_win_bottom[1], clicks=2)
                time.sleep(0.5)
            elif n1 <= purp_skill2_amount[n] and m == char_crew_skill1_amount[n]:
                time.sleep(0.5)
                pyautogui.moveTo(crew_mission_win_bottom[0], crew_mission_win_bottom[1])
                pyautogui.scroll(-15000)
                pyautogui.scroll(-15000)
                pyautogui.click(crew_mission_win_bottom[0], crew_mission_win_bottom[1], clicks=2)
                time.sleep(0.5)
            elif n1 <= purp_skill3_amount[n] and m == (char_crew_skill2_amount[n]+char_crew_skill1_amount[n]):
                time.sleep(0.5)
                pyautogui.moveTo(crew_mission_win_bottom[0], crew_mission_win_bottom[1])
                pyautogui.scroll(-15000)
                pyautogui.scroll(-15000)
                pyautogui.click(crew_mission_win_bottom[0], crew_mission_win_bottom[1], clicks=2)
                time.sleep(0.5)
            else:   
                time.sleep(0.5)
                pyautogui.click(crew_mission_win_top[0], crew_mission_win_top[1], clicks=2)
                time.sleep(0.5)      
        pyautogui.click(990, 30)
        pyautogui.click(990, 150)
        pyautogui.click(920, 555)
        pyautogui.click(900, 570)
        time.sleep(20)
        char_time[n] = time.time()-time1
        print("Character",n+1,"took",int(char_time[n]),"seconds")
    if n1 < rotations:
        #char_play must be set to 'n' just in case the player is afk which
        #will result in the characters being placed correctly for the following
        #rotation
        #If either of the if/else statements are ran then char_play will be
        #set back to 'y' via the msg_box definition if the button is clicked
        #and you can keep playing a currently non-farming character
        char_play = 'n'
        n1 += 1
        if any(i >= n1 for i in purp_skill1_amount) or any(i >= n1 for i in purp_skill2_amount) or any(i >= n1 for i in purp_skill3_amount):
            print("This is purple run time")
            print("Time until next rotation begins: ", rotation_time_yes_purp-sum(char_time))
            s.enter(rotation_time_yes_purp-sum(char_time), 1, do_something, (sc,))
            time.sleep(rotation_time_yes_purp-sum(char_time)-60)
            #Create an instance of tkinter frame
            win = Tk()

            #Set the geometry of tkinter frame
            win.geometry("750x270")

            #Initialize a Label widget
            Label(win, text = "60 seconds until next rotation starts!!!",
                  font = ('Helvetica 20 bold')).pack(pady = 20)
            Button(win, text="Click if still playing while farming", command = show_msg).pack(pady=20)
            #Automatically close the window after 3 seconds
            win.after(50000, lambda: win.destroy())

            win.mainloop()
            
            
        else:
            print("This is non-purple run time")
            print("Time until next rotation begins: ", rotation_time_no_purp-sum(char_time))
            s.enter(rotation_time_no_purp-sum(char_time), 1, do_something, (sc,))
            time.sleep(rotation_time_no_purp-sum(char_time)-60)
            #Create an instance of tkinter frame
            win = Tk()

            #Set the geometry of tkinter frame
            win.geometry("750x270")

            #Initialize a Label widget
            Label(win, text = "60 seconds until next rotation starts!!!",
                  font = ('Helvetica 20 bold')).pack(pady = 20)
            Button(win, text="Click if still playing while farming, then log out", command = show_msg).pack(pady=20)
            #Automatically close the window after 50 seconds
            win.after(50000, lambda: win.destroy())

            win.mainloop()
        if char_play == 'n':
            pyautogui.click(990, 30)
            pyautogui.click(990, 150)
            pyautogui.click(920, 555)
            pyautogui.click(900, 570)
            pyautogui.click(960,575)
            time.sleep(1)
            pyautogui.click(600,410, clicks=2)
            


#Ensures start on first page of character select
#for z in range((int(char)-1)//charslotsperpage):
pyautogui.click(pageleft_loc[0], pageleft_loc[1], clicks=5, interval=0.2)
#Block of code that calls the above definition to run the scheduled loop
n1 = 1 #Increments until == rotations then kills the loop
char_time_no_purp = 65 #seconds-No longer used (replaced by char_time)
char_time_yes_purp = 75 #seconds-No longer used (replaced by char_time)
rotation_time_no_purp = 1260 #Time per rotation
rotation_time_yes_purp = 2520 #Time per rotation
purp_miss_cast_speed = 4.2
s.enter(0, 1, do_something, (s,))
s.run()








'''
def do_something1():
  global n1  
  if n1 == rotations: # (Optional condition)
    print("* do_something1() is done *"); return
  for i in range(int(rotations)):
      for n in range(int(char)):      
          clickx = crewskills_loc_x(int(char_crew_skill1_amount[n]),int(char_crew_skill2_amount[n]),int(char_crew_skill3_amount[n]))
          clicky = crew_skill_loc_y
          if char_page[n] > 1:
              for m in range(int(char_page[n])-1):
                  pyautogui.click(pageright_loc_x, pageright_loc_y)
                  time.sleep(0.5)
          pyautogui.click(char_slot_loc_x, char_slot_loc_y[int(char_slot[n]-1)], clicks=2)
          char_slot[n] = char % charslotsperpage
          if char <= 6:
              char_page[n] = 1
          elif 7 <= char <= 12:
              char_page[n] = 2
          elif 12 <= char <= 18:
              char_page[n] = 3
          elif 19 <= char <= 24:
              char_page[n] = 4
          elif 25 <= char <= 30:
              char_page[n] = 5
          time.sleep(30)
          pyautogui.hotkey('b')
          for m in range(rewardclickrotation+2):
              pyautogui.moveTo(1850,320)
              pyautogui.click(1850,380)
              pyautogui.click(1850,405)
              pyautogui.click(1850, 430)
              
          for m in range(int(comp_amount[n])):
              if m == 4:
                  pyautogui.moveTo(clickx[m], clicky[m])
                  pyautogui.scroll(-500)
                  time.sleep(0.5)
              pyautogui.click(clickx[m], clicky[m])
              time.sleep(0.5)
              pyautogui.click(500, 375, clicks=2)
              time.sleep(0.5)      
          pyautogui.click(990, 30)
          pyautogui.click(990, 150)
          pyautogui.click(920, 555)
          pyautogui.click(900, 570)
          time.sleep(20)
  n1 += 1
  print("do_something1() "+str(n1))
  tk.after(180000, do_something1)


tk = Tkinter.Tk(); 
n1 = 0
do_something1()
tk.mainloop()
'''             
         
      


'''
for i in range(int(rotations)):
    for n in range(int(char)):      
        clickx = crewskills_loc_x(int(char_crew_skill1_amount[n]),int(char_crew_skill2_amount[n]),int(char_crew_skill3_amount[n]))
        clicky = crew_skill_loc_y
        if char_page[n] > 1:
            for m in range(int(char_page[n])-1):
                pyautogui.click(pageright_loc_x, pageright_loc_y)
                time.sleep(0.5)
        pyautogui.click(char_slot_loc_x, char_slot_loc_y[int(char_slot[n]-1)], clicks=2)
        char_slot[n] = char % charslotsperpage
        if char <= 6:
            char_page[n] = 1
        elif 7 <= char <= 12:
            char_page[n] = 2
        elif 12 <= char <= 18:
            char_page[n] = 3
        elif 19 <= char <= 24:
            char_page[n] = 4
        elif 25 <= char <= 30:
            char_page[n] = 5
        time.sleep(30)
        pyautogui.hotkey('b')
        for m in range(rewardclickrotation):
            pyautogui.click(1850,380)
            time.sleep(0.5)
            pyautogui.click(1850, 430)
            time.sleep(0.5)
            
            
        if purp_miss_skill1[n] == 'Y' or purp_miss_skills1[n] = 'y':
            pyautogui.rightClick(guild_bank_loc_x, guild_bank_loc_y)
            
            
        for m in range(int(comp_amount[n])):
            if m == 4:
                pyautogui.moveTo(clickx[m], clicky[m])
                pyautogui.scroll(-500)
                time.sleep(0.5)
            pyautogui.click(clickx[m], clicky[m])
            time.sleep(0.5)
            pyautogui.click(500, 375, clicks=2)
            time.sleep(0.5)      
        pyautogui.click(990, 30)
        pyautogui.click(990, 150)
        pyautogui.click(920, 555)
        time.sleep(20)
'''            
            


            
        
            
            
            
            
            
            