# Brennan Lu
# 24 May 2016 (?)
# Submitted to ICS3U1-03, Mr. Cope

# main.py
#     This python file is the main executable for the ManaSwap game. It references from the manaLib.py library located in the same folder.
# This python file is composed of several functions that handle the creation of game menus. Each function contains one and only one
# game loop, which is active when the function is called and ends when the function collapses. A "main" while loop at the very bottom
# of this file determines which menu is opened. No more than one menu is active at any time.

#     Each menu function is typically composed of three parts: graphics initialization, game loop, and data return. The graphics initialization defines
# graphics, images, and text. The main game loop takes the graphics defined by the first part and implements them. As well, the main game loop
# is takes player input and changes the game's variables accordingly. The data return stage typically returns some menu choice, although it also
# may return the player's score or the Treasures they have unlocked.
#     Each menu functions' return value is rarely used by another function menu, this is because it is usually unnecessary. The few instances where
# a function uses another function's return value includes normal_game_over_menu() taking the player score from play_normal_game(), and
# "treasuresDict" and "treasuresList" being passed around the menus: play_excavation_game(), treasures_menu(), and excavation_game_over()_menu
# and play_excavation_tutorial()

# READING TIP: To navigate through this file quickly, press "Ctrl-F" and type in "def (function_name)" to go to the function you want to look at.
# The menu functions that have been defined in this file are:
#        play_normal_game()
#        play_excavation_game()
#        play_basic_tutorial()
#        play_excavation_tutorial()
#        main_menu()
#        gametype_selection_menu()
#        normal_game_over_menu()
#        excavation_game_over_menu()
#        score_menu()
#        tutorial_type_selection_menu()
#        treasures_menu()

import pygame
from pygame.locals import *
import manaLib
pygame.init()

def play_normal_game(gameBoard, bg_color, text_color):
   # Parametres:     a multidimensional array, "gameBoard"; two tuples, "bg_color" and "text_color";
   # Returns:        an integer value, "playerScore"
   # Description:    this function handles the creation of the gameplay menu, where the actual gameplay takes place.
   #                 Player inputs will change "gameBoard" and increase the integer, "playerScore" according to the changes made
   #                 on the board. The function returns the player's score after their game is finished.
   #                 This gamemode is called "Normal", players are given 20 moves. The objective is to get as many mana points,
   #                 also called the player score, as possible before running out of moves. 
   
   # INITIALIZE GRAPHICS
   pygame.display.set_caption("MANASWAP release version: 2.65")
   screen_dimensions = (480, 640)
   screen = pygame.display.set_mode(screen_dimensions)
      
   red_gem = pygame.image.load("assets\images\\redgem.png")
   green_gem = pygame.image.load("assets\images\\greengem.png")
   blue_gem = pygame.image.load("assets\images\\bluegem.png")
   yellow_gem = pygame.image.load("assets\images\\yellowgem.png")

   background = pygame.Surface(screen_dimensions).convert()
   background.fill(bg_color)
   
   score_font = pygame.font.Font("assets/fonts//vani.ttf", 20)
   score_display = score_font.render("0", False, text_color)
   moves_display = score_font.render("Moves left: 20", False, text_color)
   
   button_font = pygame.font.Font("assets/fonts//vani.ttf", 24)
   exit_display = button_font.render("exit", False, text_color)
   button_selected = pygame.Surface((60, 30)).convert() # surface used to highlight button
   button_selected.fill((210, 180, 179))
   
   # INITIALIZE GAMEBOARD 
   gameBoard = manaLib.refreshBoard_noGraphics(gameBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)[0]

   # MAIN GAME LOOP
   clock = pygame.time.Clock()
   keep_going = True
   playerScore = 0
   tile1 = None
   tile2 = None
   mouseOver_exit = False # if True, we highlight the exit button
   moves_left = 20

   while keep_going:
      clock.tick(30)

      for ev in pygame.event.get():
            mousePos = pygame.mouse.get_pos()
            
            # CHECK FOR MOUSEOVER
            if 350 < mousePos[0] < 450 and 560 < mousePos[1] < 600:
               mouseOver_exit = True
            else:
               mouseOver_exit = False

            # CHECK FOR LEFT-CLICK
            if pygame.mouse.get_pressed()[0] == True: 
               if 350 < mousePos[0] < 450 and 560 < mousePos[1] < 600:  # exit button
                  keep_going = False

               elif 60 <= mousePos[0] <= 420 and 60 <= mousePos[1] <= 420: # clicked on tile
                  if tile1 == None:
                     tile1 = (mousePos[1] // 60 - 1, mousePos[0] // 60 - 1) # tile1 graphical coordinates convert to indice-form
                  elif tile2 == None:
                     tile2 = (mousePos[1] // 60 - 1, mousePos[0] // 60 - 1) # tile2 graphical coordinates convert to indice-form

               if tile1 != None and tile2 != None:# check if selected tiles are valid
                  is_adjacent = abs(tile1[0] - tile2[0]) <= 1 and abs(tile1[1] - tile2[1]) <= 1 # True if two tiles are next to each other
                  is_diagonal = abs(tile1[0] - tile2[0]) == 1 and abs(tile1[1] - tile2[1]) == 1 # True if tiles are diagonals to each other
                  if not(is_adjacent) or is_diagonal:
                     # two selected tiles are invalid if they are not adjacent to each other
                     # or if they are diagonal to each other;
                     tile1 = None
                     tile2 = None

      if tile1 != None and tile2 != None: # two tiles have been selected
         manaLib.swap_animation(tile1, tile2, gameBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)
         gameBoard = manaLib.swapTile(tile1, tile2, gameBoard)

         # there are three return values in findMatches(); [0] is indices of tiles matched, [1] is length of matching row, [2] is length of matching column
         # [3] and [4] are not need for a Normal game
         # [0] can be an empty list;
         matchData_tile1 = manaLib.findMatches(tile1, gameBoard) 
         matchData_tile2 = manaLib.findMatches(tile2, gameBoard)                                                                     

         if len(matchData_tile1[0]) != 0 or len(matchData_tile2[0]) != 0: # if a matching group was formed by tile1 or tile2 swapping
            moves_left -= 1
            moves_display = score_font.render("Moves left: " + str(moves_left), False, text_color)
            if moves_left <= 0:
               keep_going = False
                                             
            matches_list = manaLib.eliminateDuplicates(matchData_tile1[0] + matchData_tile2[0]) # matches by both tile1 and tile2 may overlap, remove duplicates
            manaLib.show_matches(matches_list, gameBoard, [], screen, red_gem, green_gem, blue_gem, yellow_gem)

            matchingRow_lengths = [matchData_tile1[1], matchData_tile2[1]]      # scoring system works by awarding bonus points for longer rows or columns
            matchingColumn_lengths = [matchData_tile1[2], matchData_tile2[2]] # collect length of all rows and columns formed
            manaLib.blit_praise_matchLength(matchingRow_lengths, matchingColumn_lengths, text_color, screen) 
            playerScore += manaLib.calculateScore(matchingRow_lengths, matchingColumn_lengths,  False)
            
            manaLib.tile_destroyed_animation(matches_list, screen)
            manaLib.play_gem_break_sound()
            gameBoard = manaLib.removeTiles(matches_list, gameBoard)
               
         else: # no matches were formed by tile1 and tile2 swapping
            manaLib.swap_animation(tile1, tile2, gameBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)
            gameBoard = manaLib.swapTile(tile1, tile2, gameBoard)

         new_state = manaLib.refreshBoard(gameBoard, [], screen, red_gem, green_gem, blue_gem, yellow_gem, score_font, text_color)
         # refreshBoard() fills in any gaps with newtiles, deletes any prexisting matches, awards points for those matches, and updates and refreshes the graphics
         gameBoard = new_state[0]            # new_state[0] is the gameBoard after being updated by refreshBoard()
         playerScore += new_state[1]         # new_state[1] is the score awarded by pre-existing matches formed

         tile1 = None # reset tile1 and tile2 when a swap was attempted
         tile2 = None
   

      screen.blit(background, (0, 0))
      
      score_display = score_font.render(str(playerScore), False, text_color)
      screen.blit(score_display, (manaLib.get_xcenter(screen_dimensions, score_display.get_rect()), 450))
      screen.blit(moves_display, (60, 550))
      
      if mouseOver_exit:
         screen.blit(button_selected, (345, 560)) # highlight text in exit_display
      screen.blit(exit_display, (350, 560))
      
      if tile1 != None: # a tile has been selected 
         manaLib.blit_tile_highlight(manaLib.indice_to_coordinate(tile1),  screen) # show which tile has been selected
         
      manaLib.blit_gameBoard(gameBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)
      
      pygame.display.flip()

   manaLib.play_gem_break_sound() # play sound to let player know he is leaving this menu
   pygame.time.wait(300)
   return playerScore


def play_excavation_game(gameBoard, runeBoard, bg_color, text_color):
   # Parametres:        a multidimensional array, "gameBoard"; two tuples, "bg_color" and "text_color";
   # Returns:           an integer value, "playerScore"; a list, "rune_list"
   # Description:       this function handles the creation of the gameplay menu, where the actual gameplay takes place.
   #                 Player inputs will change "gameBoard" and increase the integer, "playerScore" according to the changes made
   #                 on the board. The function returns the player's score after their game is finished.
   #                 This gamemode is called "Excavation", players have unlimited moves and the gems on this board have "runes"
   #                 inscribed on them. Creating a matching group deletes all the runes inscribed ontop of it. The runes are stored
   #                 in a multidimensional array similar to "gameBoard", called "runeBoard"
   
   # INITIALIZE GRAPHICS
   pygame.display.set_caption("MANASWAP release version: 2.65")
   screen_dimensions = (480, 640)
   screen = pygame.display.set_mode(screen_dimensions)
      
   red_gem = pygame.image.load("assets\images\\redgem.png")
   green_gem = pygame.image.load("assets\images\\greengem.png")
   blue_gem = pygame.image.load("assets\images\\bluegem.png")
   yellow_gem = pygame.image.load("assets\images\\yellowgem.png")

   background = pygame.Surface(screen_dimensions).convert()
   background.fill(bg_color)
   
   score_font = pygame.font.Font("assets/fonts//vani.ttf", 20)
   score_display = score_font.render("0", False, text_color)
   
   button_font = pygame.font.Font("assets/fonts//vani.ttf", 24)
   exit_display = button_font.render("exit", False, text_color)
   button_selected = pygame.Surface((60, 30)).convert() # surface used to highlight button
   button_selected.fill((210, 180, 179))
   
   # INITIALIZE GAMEBOARD
   gameBoard = manaLib.refreshBoard_noGraphics(gameBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)[0]

   # MAIN GAME LOOP
   clock = pygame.time.Clock()
   keep_going = True
   playerScore = 0
   tile1 = None
   tile2 = None
   mouseOver_exit = False # if True, we highlight the exit button
   rune_list = [] # all of the runes collected the player, returned at end of function

   while keep_going:
      clock.tick(30)

      for ev in pygame.event.get():
            mousePos = pygame.mouse.get_pos()
                     
            # CHECK FOR MOUSEOVER
            if 350 < mousePos[0] < 450 and 560 < mousePos[1] < 600:
               mouseOver_exit = True
            else:
               mouseOver_exit = False

            # CHECK FOR LEFT-CLICK
            if pygame.mouse.get_pressed()[0] == True:
               
               if 350 < mousePos[0] < 450 and 560 < mousePos[1] < 600: # exit button
                  keep_going = False
               
               elif 60 <= mousePos[0] <= 420 and 60 <= mousePos[1] <= 420: # clicked on tile
                  if tile1 == None:
                     tile1 = (mousePos[1] // 60 - 1, mousePos[0] // 60 - 1) # tile1 graphical coordinates convert to indice-form
                  elif tile2 == None:
                     tile2 = (mousePos[1] // 60 - 1, mousePos[0] // 60 - 1) # tile2 graphical coordinates convert to indice-form

               # check if selected tiles are valid
               if tile1 != None and tile2 != None:
                  is_adjacent = abs(tile1[0] - tile2[0]) <= 1 and abs(tile1[1] - tile2[1]) <= 1 # True if two tiles are next to each other
                  is_diagonal = abs(tile1[0] - tile2[0]) == 1 and abs(tile1[1] - tile2[1]) == 1 # True if tiles are diagonals to each other
                  if not(is_adjacent) or is_diagonal:
                     # two selected tiles are invalid if they are not adjacent to each other
                     # or if they are diagonal to each other;
                     tile1 = None
                     tile2 = None

      if tile1 != None and tile2 != None: # two tiles have been selected
         manaLib.swap_animation(tile1, tile2, gameBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)
         gameBoard = manaLib.swapTile(tile1, tile2, gameBoard)

         # findMatches has three return values; [0] is indices of all tiles in a matching group, [1] is length of matching row, [2] is length of matching column
         # [3] is the tile indices of a matching row formed by the tile, [4] is the tile indices of any matching column formed by the tile
         # [0] can be an empty list;
         matchData_tile1 = manaLib.findMatches(tile1, gameBoard) 
         matchData_tile2 = manaLib.findMatches(tile2, gameBoard)                                                                     

         if len(matchData_tile1[0]) != 0 or len(matchData_tile2[0]) != 0: # if there were matches formed by tile1 and/or tile2
            # TILE CALCULATIONS
            # these are identical to the tile calculations in play_normal_game()
            matches_list = manaLib.eliminateDuplicates(matchData_tile1[0] + matchData_tile2[0])
            manaLib.show_matches(matches_list, gameBoard, runeBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)

            matchingRow_lengths = [matchData_tile1[1], matchData_tile2[1]]
            matchingColumn_lengths = [matchData_tile1[2], matchData_tile2[2]]
            manaLib.blit_praise_matchLength(matchingRow_lengths, matchingColumn_lengths, text_color, screen)
            playerScore += manaLib.calculateScore(matchingRow_lengths, matchingColumn_lengths,  False)
            
            manaLib.tile_destroyed_animation(matches_list, screen)
            manaLib.play_gem_break_sound()
            gameBoard = manaLib.removeTiles(matches_list, gameBoard)

            # RUNE CALCULATIONS
            runeData = [matchData_tile1[3], matchData_tile1[4], matchData_tile2[3], matchData_tile2[4]] # collect all the matching groups into a list ##################################################################
            for permutation in runeData:
               new_state = manaLib.identifyRunes(runeBoard, permutation)
               if len(new_state[0]) >= 3: # if 3 or more runes were part of a matching group
                  rune_list.append(new_state[0])
                  runeBoard = manaLib.removeTiles(new_state[1], runeBoard)
               
         else: # no matches were formed by tile1 and tile2 swapping
            manaLib.swap_animation(tile1, tile2, gameBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)
            gameBoard = manaLib.swapTile(tile1, tile2, gameBoard)

         new_state = manaLib.refreshBoard(gameBoard, runeBoard, screen, red_gem, green_gem, blue_gem, yellow_gem, score_font, text_color)
         # refreshBoard() updates the gameBoard
         gameBoard = new_state[0]            # new_state[0] is the gameBoard after pre-existing matched 3's are removed
         playerScore += new_state[1]         # new_state[1] is the score generated by the pre-existing matched 3's

         tile1 = None # reset tile1 and tile2 when a swap has been done
         tile2 = None
   

      screen.blit(background, (0, 0))
      
      score_display = score_font.render(str(playerScore), False, text_color)
      screen.blit(score_display, (manaLib.get_xcenter(screen_dimensions, score_display.get_rect()), 450))
      
      if mouseOver_exit:
         screen.blit(button_selected, (345, 560)) # highlight text in exit_display
      screen.blit(exit_display, (350, 560))
      
      if tile1 != None:
         manaLib.blit_tile_highlight(manaLib.indice_to_coordinate(tile1),  screen) # show which tile has been selected
         
      manaLib.blit_gameBoard(gameBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)
      manaLib.blit_runes(runeBoard, screen) 
      
      pygame.display.flip()

   manaLib.play_gem_break_sound() # play sound to let player know he is leaving this menu
   pygame.time.wait(300)
   return playerScore, rune_list


def play_basic_tutorial(bg_color, text_color):
    # Parameters:       two tuples, "bg_color" and "text_color"
    # Returns:          None
    # Description:      this essentially the same as play_normal_game(), however, this function does not
    #                take in any "grid" as input since the board for this tutorial is pre-generated; furthermore, the
    #                function does not return any playerScore; finally, functions that would otherwise be present are
    #                replaced by hard-coded code, addTiles(), for example, randomly adds tiles; so addTiles()
    #                is represented by a series of gameBoard[x][y] = new_tile statements; 

    #                in this tutorial level, the player should only swap the tile at gameBoard[3][2] and gameBoard[3][3];
    #                which are red and blue gems respectively; 

   # INITIALIZE GRAPHICS
   pygame.display.set_caption("MANASWAP release version: 2.65")
   screen_dimensions = (480, 640)
   screen = pygame.display.set_mode(screen_dimensions)

   red_gem = pygame.image.load("assets\images\\redgem.png")
   green_gem = pygame.image.load("assets\images\\greengem.png")
   blue_gem = pygame.image.load("assets\images\\bluegem.png")
   yellow_gem = pygame.image.load("assets\images\\yellowgem.png")

   background = pygame.Surface(screen_dimensions).convert()
   background.fill(bg_color)

   score_font = pygame.font.Font("assets/fonts//vani.ttf", 30)
   score_display = score_font.render("0", False, text_color)
   moves_display = score_font.render("Moves left: 1", False, text_color)
   
   button_font = pygame.font.Font("assets/fonts//vani.ttf", 24)
   exit_display = button_font.render("exit", False, text_color)

   tutorial_font = pygame.font.Font("assets/fonts//vani.ttf", 12)
   tutorial_lines = open("assets/dialogue//basic_tutorial_messages.txt", "r+").readlines()
   tutorial_box = pygame.Surface((240, 90)).convert() # this is a box that encloses the tutorial messages
   tutorial_box.fill((63, 59, 85))

   # below are various highlights to guide the reader's eye to important information
   tutorial_highlight_tile = pygame.Surface((60, 60)).convert()
   tutorial_highlight_tile.fill((200, 100, 100))
   tutorial_exit_highlight = pygame.Surface((50, 30)).convert()
   tutorial_exit_highlight.fill((210, 180, 179))
   tutorial_score_highlight = pygame.Surface((60, 30)).convert()
   tutorial_score_highlight.fill((210, 180, 179))
   tutorial_moves_highlight = pygame.Surface((30, 30)).convert()
   tutorial_moves_highlight.fill((210, 180, 179))

   # MAIN GAME LOOP
   # A gameboard has been hand-made for the purpose of this tutorial
   gameBoard = [["green", "yellow", "blue", "green", "green", "blue"],
                          ["red", "green", "blue", "blue", "yellow", "red"],
                          ["blue", "yellow", "green", "red", "green", "red"],
                          ["red", "green", "red", "blue", "yellow", "blue"],
                          ["yellow", "blue", "yellow", "red", "green", "green"],
                          ["green", "red", "green", "blue", "yellow", "blue"]] 
   clock = pygame.time.Clock()
   keep_going = True
   playerScore = 0
   tile1 = None
   tile2 = None
   mouseOver_exit = False
   moves_left = 1
   tutorial_stage = 1 # there are 10 stages in the tutorial, each with one text-box that tells the player what to do;
                              # here are all of the stages and what sorts of inputs is taken from the player;
                              # the tutorial instructions are stored in "basic_tutorial_messages.txt"
                              # tutorial_stage = 1          -       left-mouseclick anywhere to continue
                              # tutorial_stage = 2          -       left-mouseclick anywhere to continue
                              # tutorial_stage = 3          -       left-mouseclick at 180 <= x <= 240 and 240 <= y <= 300 to continue
                              # tutorial_stage = 4          -       left-mouseclick at 240 <= x <= 300 and 240 <= y <= 300 to continue
                              # tutorial_stage = 5          -       left-mouseclick anywhere to continue          
                              # tutorial_stage = 6          -       left-mouseclick anywhere to continue
                              # tutorial_stage = 8          -       left-mouseclick anywhere to continue
                              # tutorial_stage = 9          -       left-mouseclick anywhere to continue                              
                              # tutorial_stage = 10          -       left-mouseclick anywhere to continue
                              # tutorial_stage = 11       -       left-click 350 < x < 450 and 560 < y < 600 to continue      

   while keep_going:
      clock.tick(30)
                
      for ev in pygame.event.get():
            mousePos = pygame.mouse.get_pos()
               
            if pygame.mouse.get_pressed()[0] == True:
               
              if tutorial_stage == 3: # the player must select the red tile at this stage
                  if 180 <= mousePos[0] <= 240 and 240 <= mousePos[1] <= 300:
                     tutorial_stage += 1
                     tile1 = (3, 2)
                     
              elif tutorial_stage == 4: # the player must select the blue tile at this stage
                  if 240 <= mousePos[0] <= 300 and 240 <= mousePos[1] <= 300:
                     tutorial_stage += 1
                     tile2 = (3, 3)
                     
              elif tutorial_stage == 11: # the player can only select the exit tile at this stage
                  if 350 < mousePos[0] < 450 and 560 < mousePos[1] < 600:
                     keep_going = False
                     
              else: # in all other stages, mouse left-click continues with the next tutorial message
                  tutorial_stage += 1

      if tile1 != None and tile2 != None:
         # img_cover below is a band-aid solution for a graphical bug; "tutorial_highlight_tile", defined in the
         # graphical section of this function above needs to be erased when tile2 is selected; 
         img_cover = pygame.Surface((60, 60)).convert()
         img_cover.fill(bg_color)
         screen.blit(img_cover, (240, 240))
         pygame.display.flip()
         
         manaLib.swap_animation(tile1, tile2, gameBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)
         gameBoard = manaLib.swapTile(tile1, tile2, gameBoard)
         
         moves_left -= 1
         moves_display = score_font.render("Moves left: " + str(moves_left), False, (255, 255, 255))
                                          
         matches_list = [[3,3],[2,3],[4,3]] # the tiles that will be matched were pre-determined, so just write the list instead of calling findMatches()
         manaLib.show_matches(matches_list, gameBoard, [], screen, red_gem, green_gem, blue_gem, yellow_gem)
         
         playerScore += manaLib.calculateScore([3],[], False) # there is a matching row of length 3, no matching column, and turn bug_correction off
         
         manaLib.tile_destroyed_animation(matches_list, screen)
         manaLib.play_gem_break_sound()
         gameBoard = manaLib.removeTiles(matches_list, gameBoard)
         
         tile_kinematic_data = manaLib.get_tile_kinematics(gameBoard, red_gem, green_gem, blue_gem, yellow_gem)
         manaLib.tile_shift_animation(gameBoard, screen, tile_kinematic_data)
         gameBoard = manaLib.shiftTiles(gameBoard)
         manaLib.play_thump()

         # manually replace the matched tiles
         gameBoard[0][3] = "blue"
         gameBoard[1][3] = "red"
         gameBoard[2][3] = "red"

         # reset tile1 and tile2
         tile1 = None
         tile2 = None

      screen.blit(background, (0, 0))

      # print all the tutorial descriptions here
      screen.blit(tutorial_box, (40, 430))
      line_pos = (50, 440) # start from the top of the text box
      for line in tutorial_lines[(tutorial_stage - 1) * 4: tutorial_stage * 4]: # if stage == 1, show lines 0 to 3; if stage == 2, show lines 4 to 7, etc
         current_line = tutorial_font.render(line[:-1], False, text_color) # line[:-1] removes the \n char at end when reading from file
         screen.blit(current_line, line_pos) 
         line_pos = (line_pos[0], line_pos[1] + 20) # move to the next line in text box

      if tutorial_stage == 3:
         # in this stage, the player must click on the red gem; highlight it for the user
         screen.blit(tutorial_highlight_tile, (180, 240))
      elif tutorial_stage == 4:
         # in this stage, the player must click on the blue gem; highlight it for the user
         screen.blit(tutorial_highlight_tile, (240, 240))
      elif tutorial_stage == 5 or tutorial_stage == 6:
         screen.blit(tutorial_score_highlight, (300, 455))
      elif tutorial_stage == 8:
         screen.blit(tutorial_moves_highlight, (210, 555))
      elif tutorial_stage == 10 or tutorial_stage == 11:
         screen.blit(tutorial_exit_highlight, (345, 560))
         
      score_display = score_font.render(str(playerScore), False, text_color)
      screen.blit(score_display, (300, 450))
      screen.blit(moves_display, (60, 550))
      screen.blit(exit_display, (350, 560))
      
      if tile1 != None: # tile1 was selected
         manaLib.blit_tile_highlight(manaLib.indice_to_coordinate(tile1),  screen) # highlight tile1
         
      manaLib.blit_gameBoard(gameBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)
      pygame.display.flip()

   manaLib.play_gem_break_sound() # play a sound when the player leaves this menu
   pygame.time.wait(300)


def play_excavation_tutorial(treasuresDict, bg_color, text_color):
   # Parametres:     a dictionary "treasuresDict" ; two tuples, "bg_color" and "text_color";
   # Returns:        a dictionary, "treasuresDict"
   # Description:    this function handles the creation of the Excavation tutorial menu. This function does not
   #              take a grid array as input because it generates its own gameBoard and runeBoard. This function
   #              resembles play_excavation_game(), however, not all of the manaLib functions are used and
   #              updates to the gameBoard and runeBoard are hardcoded
   
   # INITIALIZE GRAPHICS
   pygame.display.set_caption("MANASWAP release version: 2.65")
   screen_dimensions = (480, 640)
   screen = pygame.display.set_mode(screen_dimensions)
      
   red_gem = pygame.image.load("assets\images\\redgem.png")
   green_gem = pygame.image.load("assets\images\\greengem.png")
   blue_gem = pygame.image.load("assets\images\\bluegem.png")
   yellow_gem = pygame.image.load("assets\images\\yellowgem.png")

   background = pygame.Surface(screen_dimensions).convert()
   background.fill(bg_color)
   
   score_font = pygame.font.Font("assets/fonts//vani.ttf", 30)
   score_display = score_font.render("0", False, text_color)
   
   button_font = pygame.font.Font("assets/fonts//vani.ttf", 24)
   exit_display = button_font.render("exit", False, text_color)
   button_selected = pygame.Surface((60, 30)).convert() # surface used to highlight button
   button_selected.fill((210, 180, 179))

   # INITIALIZE TUTORIAL GRAPHICS
   tutorial_font = pygame.font.Font("assets/fonts//vani.ttf", 12)
   tutorial_lines = open("assets/dialogue//excavation_tutorial_messages.txt", "r+").readlines()
   tutorial_box = pygame.Surface((245, 90)).convert() # this is a box that encloses the tutorial messages
   tutorial_box.fill((63, 59, 85))

   # below are various highlights to guide the reader's eye to important information
   tutorial_highlight_tile = pygame.Surface((60, 60)).convert()
   tutorial_highlight_tile.fill((200, 100, 100))
   tutorial_exit_highlight = pygame.Surface((40, 25)).convert()
   tutorial_exit_highlight.fill((210, 180, 179))
   tutorial_score_highlight = pygame.Surface((60, 30)).convert()
   tutorial_score_highlight.fill((210, 180, 179))
   
   # INITIALIZE GAMEBOARD AND RUNEBOARD
   gameBoard = [["blue", "red", "green", "red", "green", "blue"],
                          ["green", "yellow", "green", "red", "red", "yellow"],
                          ["blue", "yellow", "red", "blue", "blue", "red"],
                          ["yellow", "green", "yellow", "yellow", "blue", "red"],
                          ["yellow", "blue", "red", "green", "yellow", "green"],
                          ["red", "blue", "blue", "green", "red", "yellow"] ]
   runeBoard =  [["a", "u", "u", "a", "t", "a"],
                         ["u", "a", "t", "t", "a", "u"],
                         ["t", "t", "a", "p", "t", "u"],
                         ["a", "t", "u", "p", "u", "u"],
                         ["a", "p", "p", "t", "t", "p"],
                         ["p", "a", "a", "a", "u", "u"]]
   
   # MAIN GAME LOOP
   clock = pygame.time.Clock()
   keep_going = True
   playerScore = 0
   tile1 = None
   tile2 = None
   mouseOver_exit = False # if True, we highlight the exit button
   rune_list = [] # this will be returned
   tutorial_stage = 1 # there are 21 stages in this tutorial

   while keep_going:
      clock.tick(30)

      for ev in pygame.event.get():
            mousePos = pygame.mouse.get_pos()
            
            if pygame.mouse.get_pressed()[0] == True: # left-click
              if tutorial_stage == 8: # the player must select the red tile at this stage
                  if 180 <= mousePos[0] <= 240 and 180 <= mousePos[1] <= 240:
                     tutorial_stage += 1
                     tile1 = (2, 2)
              elif tutorial_stage == 9: # the player must select the blue tile at this stage
                  if 240 <= mousePos[0] <= 300 and 180 <= mousePos[1] <= 240:
                     tutorial_stage += 1
                     tile2 = (2, 3)
              elif tutorial_stage == 21: # the player can only select the exit tile at this stage
                  if 350 < mousePos[0] < 450 and 560 < mousePos[1] < 600:
                     keep_going = False
              else: # in all other stages, mouse left-click continues with the next tutorial message
                  tutorial_stage += 1

      if tile1 != None and tile2 != None:
         manaLib.swap_animation(tile1, tile2, gameBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)
         gameBoard = manaLib.swapTile(tile1, tile2, gameBoard)
         
         matches_list = [[0,3],[1,3],[2,3]]
         manaLib.show_matches(matches_list, gameBoard, runeBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)
   
         playerScore += 150
         
         manaLib.tile_destroyed_animation(matches_list, screen)
         manaLib.play_gem_break_sound()
         gameBoard = manaLib.removeTiles(matches_list, gameBoard)

         # RUNE CALCULATIONS
         rune_list = ["apt"] # collect all the matching groups into a list ##################################################################
         runeBoard = manaLib.removeTiles(matches_list, runeBoard)

         gameBoard[0][3] = "yellow"
         gameBoard[1][3] = "yellow"
         gameBoard[2][3] = "green"

         tile1 = None # reset tile1 and tile2 when a swap has been done
         tile2 = None
         
      screen.blit(background, (0, 0))
      
      # print all the tutorial descriptions here
      screen.blit(tutorial_box, (40, 430)) 
      line_pos = (50, 440) # start from the top of the text box
      for line in tutorial_lines[(tutorial_stage - 1) * 4: tutorial_stage * 4]:
         current_line = tutorial_font.render(line[:-1], False, text_color) # line[:-1] removes the \n char at end when reading from file
         screen.blit(current_line, line_pos) 
         line_pos = (line_pos[0], line_pos[1] + 20) # move to the next line in text box

      if tutorial_stage == 4:
         manaLib.blit_tile_highlight(manaLib.indice_to_coordinate((2,2)), screen)
      elif tutorial_stage == 5:
         manaLib.blit_tile_highlight(manaLib.indice_to_coordinate((2,3)), screen)
      elif tutorial_stage == 6:
         manaLib.blit_tile_highlight(manaLib.indice_to_coordinate((2,4)), screen)   
      elif tutorial_stage == 7:
         manaLib.blit_tile_highlight(manaLib.indice_to_coordinate((2,5)), screen)
                    
      score_display = score_font.render(str(playerScore), False, text_color)
      screen.blit(score_display, (300, 450))
      
      screen.blit(exit_display, (350, 560))
      
      if tile1 == None and tutorial_stage == 8:
         manaLib.blit_tile_highlight(manaLib.indice_to_coordinate((2,2)),  screen) # show which tile has been selected
      elif tile2 == None and tutorial_stage == 9:
         manaLib.blit_tile_highlight(manaLib.indice_to_coordinate((2,3)),  screen)
         
      manaLib.blit_gameBoard(gameBoard, screen, red_gem, green_gem, blue_gem, yellow_gem)
      manaLib.blit_runes(runeBoard, screen)
      
      pygame.display.flip()

   manaLib.play_gem_break_sound() # play sound to let player know he is leaving this menu
   pygame.time.wait(300)
   if treasuresDict["apt"] == 0: # player gets a free "apt" Treasure if they have not gotten one already
      treasuresDict["apt"] += 1
   return treasuresDict


def main_menu(bg_color, text_color):
   # Parameters:     two tuples, "bg_color" and "text_color"
   # Returns:        a string, "button selection"
   # Description:    this function handles the main menu, the very first screen that the player will interact with. This function
   #              simply defines regions of the screen that act as buttons. These buttons determine which menu the player will move
   #              to. The return value is the button that was selected;
   #                 This menu has four secret buttons; the four coloured gems below the main menu buttons control
   #              what music is playing. 
   
   # INITIALIZE GRAPHICS
   pygame.display.set_caption("MANASWAP release version: 2.65")
   screen_dimensions = (480, 640)
   screen = pygame.display.set_mode(screen_dimensions)

   red_gem = pygame.image.load("assets\images\\redgem.png")
   green_gem = pygame.image.load("assets\images\\greengem.png")
   blue_gem = pygame.image.load("assets\images\\bluegem.png")
   yellow_gem = pygame.image.load("assets\images\\yellowgem.png")

   background = pygame.Surface(screen_dimensions).convert()
   background.fill(bg_color)

   title_font = pygame.font.Font("assets/fonts//fawn.ttf", 100)
   title_display = title_font.render("ManaSwap", False, text_color)
   title_red_glow = title_font.render("Mana", False, (160, 50, 100))
   xpos_ManaSwap = manaLib.get_xcenter(screen_dimensions, title_display.get_rect()) # this is the x-coordinate needed to center the title
   
   button_font = pygame.font.Font("assets/fonts//vani.ttf", 48)
   button_selected = pygame.Surface((200, 60)).convert()
   button_selected.fill((210, 180, 179))
   
   start_display = button_font.render("start", False, text_color)
   tutorial_display = button_font.render("tutorial", False, text_color)
   highscore_display = button_font.render("highscores", False, text_color)
   treasures_display = button_font.render("treasures", False, text_color)
   exit_display = button_font.render("exit", False, text_color)

   # MAIN GAME LOOP
   clock = pygame.time.Clock()
   keep_going = True
   button_selection = None
   mouseOver = None

   while keep_going:
      clock.tick(30)

      for ev in pygame.event.get():
         mousePos = pygame.mouse.get_pos()

         # CHECK FOR MOUSEOVER
         if 170 < mousePos[0] < 270 and 180 < mousePos[1] < 220:
            mouseOver = "start"
         elif 170 < mousePos[0] < 270 and 240 < mousePos[1] < 300:
            mouseOver = "tutorial"
         elif 170 < mousePos[0] < 270 and 300 < mousePos[1] < 340:
            mouseOver = "highscores"
         elif 170 < mousePos[0] < 270 and 360 < mousePos[1] < 400:
            mouseOver = "treasures"
         elif 170 < mousePos[0] < 270 and 420 < mousePos[1] < 460:
            mouseOver = "exit"
         elif 60 < mousePos[0] < 460 and 20 < mousePos[1] < 120:
            mouseOver = "title"
         else:
            mouseOver = None

         # CHECK FOR EXIT       
         if ev.type == QUIT:
            button_selection = "quit"
            keep_going = False

         # CHECK FOR LEFT-CLICK
         if pygame.mouse.get_pressed()[0] == True:
            if 160 < mousePos[0] < 280 and 180 < mousePos[1] < 220: # go to play_normal_game()
               button_selection = "play"
               keep_going = False
            elif 170 < mousePos[0] < 270 and 240 < mousePos[1] < 300: # go to tutorial_type_selection_menu()
               button_selection = "tutorial"
               keep_going = False
            elif 170 < mousePos[0] < 270 and 300 < mousePos[1] < 360: #  go to score_menu()
               button_selection = "highscores"
               keep_going = False
            elif 170 < mousePos[0] < 270 and 360 < mousePos[1] < 400: # go to treasures_menu()
               button_selection = "treasures"
               keep_going = False
            elif 170 < mousePos[0] < 270 and 420 < mousePos[1] < 480: # quit the program
               button_selection = "quit"
               keep_going = False

            # SECRET MUSIC PLAYER BUTTONS,
            # click on the title text to get the jingling sound effect
            elif 60 < mousePos[0] < 460 and 20 < mousePos[1] < 120:
               manaLib.play_gem_break_sound()
            # click on a gem on the main title to change the music for the game
            elif 120 < mousePos[0] < 180 and 500 < mousePos[1] < 560:
               pygame.mixer.music.load("assets\soundtrack\\theme.mp3")
               pygame.mixer.music.set_volume(0.4)
               pygame.mixer.music.play(-1)
            elif 180 < mousePos[0] < 240 and 500 < mousePos[1] < 560:
               pygame.mixer.music.load("assets\soundtrack\\rainytheme.mp3")
               pygame.mixer.music.set_volume(0.4)
               pygame.mixer.music.play(-1)
            elif 240 < mousePos[0] < 300 and 500 < mousePos[1] < 560:
               pygame.mixer.music.load("assets\soundtrack\\guitartheme.mp3")
               pygame.mixer.music.set_volume(0.4)
               pygame.mixer.music.play(-1)
            elif 300 < mousePos[0] < 360 and 500 < mousePos[1] < 560:
               pygame.mixer.music.load("assets\soundtrack\\olombretheme.mp3")
               pygame.mixer.music.set_volume(0.4)
               pygame.mixer.music.play(-1)
               
      
      screen.blit(background, (0, 0))
      screen.blit(title_display, (xpos_ManaSwap, 40))

      # HIGHLIGHT OVER BUTTON
      if mouseOver == "start":
         button_selected = pygame.Surface((160, 60)).convert()
         button_selected.fill((210, 180, 179))
         screen.blit(button_selected, (135, 180))
      elif mouseOver == "tutorial":
         button_selected = pygame.Surface((220, 60)).convert()
         button_selected.fill((210, 180, 179))
         screen.blit(button_selected, (135, 240))
      elif mouseOver == "highscores":
         button_selected = pygame.Surface((280, 60)).convert()
         button_selected.fill((210, 180, 179))
         screen.blit(button_selected, (135, 300))
      elif mouseOver == "treasures":
         button_selected = pygame.Surface((240, 60)).convert()
         button_selected.fill((210, 180, 179))
         screen.blit(button_selected, (135, 360))
      elif mouseOver == "exit":
         button_selected = pygame.Surface((140, 60)).convert()
         button_selected.fill((210, 180, 179))
         screen.blit(button_selected, (135, 420))
      elif mouseOver == "title":
         screen.blit(title_red_glow, (xpos_ManaSwap, 40))
         
      screen.blit(start_display, (160, 180))
      screen.blit(tutorial_display, (160, 240))
      screen.blit(highscore_display, (160, 300))
      screen.blit(treasures_display, (160, 360))
      screen.blit(exit_display, (160, 420))
      
      screen.blit(red_gem, (120, 500))
      screen.blit(blue_gem, (180, 500))
      screen.blit(green_gem, (240, 500))
      screen.blit(yellow_gem, (300, 500))
      
      pygame.display.flip()

   manaLib.play_gem_break_sound() # play sound to signal player they are leaving this menu
   pygame.time.wait(500)
   return button_selection


def gametype_selection_menu(bg_color, text_color):
   # Parametres:     two tuples, "bg_color" and "text_color"
   # Returns:        a multidimensional array, "gameBoard"
   # Description:    this function handles the menu that allows the player to select a gametype; there are two
   #              buttons defined by this function, one for each gamemode; there are two gamemodes: normal and
   #              excavation. 
   
   # INITIALIZE GRAPHICS
   pygame.display.set_caption("MANASWAP release version: 2.65")
   screen_dimensions = (480, 640)
   screen = pygame.display.set_mode(screen_dimensions)

   background = pygame.Surface(screen_dimensions).convert()
   background.fill(bg_color)

   button_font = pygame.font.Font("assets/fonts//vani.ttf", 35)
   description = button_font.render("Choose a gamemode", False, text_color)

   normal_button = button_font.render("Normal", False, text_color)   
   normal_button_selected = pygame.Surface((150, 40)).convert()
   normal_button_selected.fill((210, 180, 179))
   normal_highlight_center = manaLib.get_xcenter(screen_dimensions, normal_button_selected.get_rect())
   normal_button_center = manaLib.get_xcenter(screen_dimensions, normal_button.get_rect())
   
   excavation_button = button_font.render("Excavation", False, text_color)
   excavation_button_selected = pygame.Surface((200, 40)).convert()
   excavation_button_selected.fill((210, 180, 179))
   excavation_highlight_center = manaLib.get_xcenter(screen_dimensions, excavation_button_selected.get_rect())
   excavation_button_center = manaLib.get_xcenter(screen_dimensions, excavation_button.get_rect())
   
   return_button = button_font.render("Back to main menu", False, text_color)
   return_button_selected = pygame.Surface((300, 40)).convert()
   return_button_selected.fill((210, 180, 179))
   return_highlight_center = manaLib.get_xcenter(screen_dimensions, return_button_selected.get_rect())
   return_button_center = manaLib.get_xcenter(screen_dimensions, return_button.get_rect())

   # MAIN GAME LOOP
   clock = pygame.time.Clock()
   keep_going = True
   mouseOver = None
   gametype = None

   while keep_going:
      clock.tick(30)

      for ev in pygame.event.get():
         mousePos = pygame.mouse.get_pos()

         # CHECK FOR MOUSEOVER
         if 165 <= mousePos[0] <= 305 and 130 <= mousePos[1] <= 190:
            mouseOver = "normal"
         elif 165 <= mousePos[0] <= 340 and 200 <= mousePos[1] <= 260:
            mouseOver = "excavation"
         elif 165 <= mousePos[0] <= 400 and 300 <= mousePos[1] <= 360:
            mouseOver = "return"
         else:
            mouseOver = None

         # CHECK FOR LEFT-CLICK
         if pygame.mouse.get_pressed()[0] == True:
            if 165 <= mousePos[0] <= 305 and 130 <= mousePos[1] <= 190:
               gametype = "normal"
               keep_going = False
            elif 165 <= mousePos[0] <= 340 and 200 <= mousePos[1] <= 260:
               gametype = "excavation"
               keep_going = False
            elif 165 <= mousePos[0] <= 400 and 300 <= mousePos[1] <= 360:
               keep_going = False

      screen.blit(background, (0, 0))
      screen.blit(description, (75, 60))
            
      if mouseOver == "normal":
         screen.blit(normal_button_selected, (normal_highlight_center, 130))
      elif mouseOver == "excavation":
         screen.blit(excavation_button_selected, (excavation_highlight_center, 200))
      elif mouseOver == "return":
         screen.blit(return_button_selected, (return_highlight_center, 300))
      
      screen.blit(normal_button, (normal_button_center, 130))
      screen.blit(excavation_button, (excavation_button_center, 200))
      screen.blit(return_button, (return_button_center, 300))
      
      pygame.display.flip()

   manaLib.play_gem_break_sound() # signal to player they are leaving this menu
   pygame.time.wait(300)
   return gametype


def normal_game_over_menu(score, bg_color, text_color):
   # Parameters:     an integer value, "score"; two tuples, "bg_color" and "text_color"
   # Returns:        a list of length 2, "highscore_entry", all entries are strings
   # Description:    this function handles the game over menu. In this menu, players will be asked to enter their name.
   #              The name will be stored alongside the player's score in a list called "highscore_entry", which is returned.

   pygame.display.set_caption("MANASWAP release version: 2.65")
   screen_dimensions = (480, 640)
   screen = pygame.display.set_mode(screen_dimensions)

   background = pygame.Surface(screen_dimensions).convert()
   background.fill(bg_color)

   message_font = pygame.font.Font("assets/fonts//fawn.ttf", 50)
   exit_text = message_font.render("EXCAVATION COMPLETE!", False, text_color)
   exit_text_center = manaLib.get_xcenter(screen_dimensions, exit_text.get_rect())

   playerName = "" 
   name_font = pygame.font.Font("assets/fonts//vani.ttf", 25)
   name_text = name_font.render(playerName, False, text_color)
   name_box = pygame.Surface((220, 40)).convert() # this rect encloses the player's name
   name_box.fill((63, 50, 113))
   name_box_center = manaLib.get_xcenter(screen_dimensions, name_box.get_rect())
   
   score_count = 0
   your_score_text = name_font.render("Your score", False, text_color)
   your_score_text_center = manaLib.get_xcenter(screen_dimensions, your_score_text.get_rect())
   score_number = name_font.render(str(score_count), False, text_color)
   
   enter_name_text = name_font.render("Please enter your name", False, text_color)
   enter_name_text_center = manaLib.get_xcenter(screen_dimensions, enter_name_text.get_rect())

   exit_display = name_font.render("Return to main menu", False, text_color)
   exit_display_center = manaLib.get_xcenter(screen_dimensions, exit_display.get_rect())
   button_font = pygame.font.Font("assets/fonts//vani.ttf", 24)
   button_selected = pygame.Surface((260, 30)).convert()
   button_selected.fill((210, 180, 179))
   
   clock = pygame.time.Clock()
   keep_going = True
   mouseOver_exit = False
   delete_on = False

   while keep_going:
      clock.tick(30)

      # SCORE COUNTER 
      if score_count < score:
         # increase the player's score gradually from 0 to add dramatic effect
         if score > 210:  # The incrementing effect does not work with scores less than 210. 
            score_count += int(score / 210) # 210 = frame rate * 7 seconds, so the counter increases until you reach score in 7 seconds
         else: # A special exception must be made for scores under 210, because int(score / 210) == 0 if score <210
            score_count += int(score / 50) 
         score_number = name_font.render(str(score_count), False, text_color)
      else:
         # score_count may overflow, if above statement False, set score_count to score to ensure right number shown
         score_count = score
         score_number = name_font.render(str(score_count), False, text_color)

      if delete_on and len(playerName) > 0:
         playerName = playerName[:-1] #cut off last character

      for ev in pygame.event.get():
         mousePos = pygame.mouse.get_pos()

         # CHECK FOR MOUSEOVER
         if 130 < mousePos[0] < 340 and 500 < mousePos[1] < 530:
            mouseOver_exit = True
         else:
            mouseOver_exit = False

         # CHECK FOR LEFT-CLICK
         if pygame.mouse.get_pressed()[0] == True:
            if 130 < mousePos[0] < 340 and 500 < mousePos[1] < 530:
               keep_going = False

         # CHECK FOR KEY INPUT
         elif ev.type == KEYDOWN:
            if ev.key == K_BACKSPACE:
                delete_on = True
            elif ev.key == K_RETURN:
               keep_going = False
            elif (ev.unicode.isalnum() or ev.key==K_SPACE) and len(playerName) < 16:
                playerName+= ev.unicode #adds character value of key
            
         elif ev.type == KEYUP:
            if ev.key == K_BACKSPACE:
               delete_on = False

      screen.blit(background, (0, 0))        
      name_text = name_font.render(playerName, False, text_color)
      
      screen.blit(exit_text, (exit_text_center, 35))
      screen.blit(name_box, (name_box_center, 230))
      screen.blit(your_score_text, (your_score_text_center, 100))
      screen.blit(score_number, (manaLib.get_xcenter(screen_dimensions, score_number.get_rect()), 140))
      screen.blit(enter_name_text, (enter_name_text_center, 180))
      screen.blit(name_text, (manaLib.get_xcenter(screen_dimensions, name_text.get_rect()), 230))
      
      if mouseOver_exit:
         screen.blit(button_selected, (110, 500))
      screen.blit(exit_display, (exit_display_center, 500))
      pygame.display.flip()

   highscore_entry = [playerName, str(score)] # package player name and player score for return

   manaLib.play_gem_break_sound()
   pygame.time.wait(300)                  
   return highscore_entry


def excavation_game_over_menu(score, runes_collected, bg_color, text_color):
   # Parameters:     an integer value, "score"; two tuples, "bg_color" and "text_color"
   # Returns:        a list of length 2, "highscore_entry", all entries are strings
   # Description:    this function handles the game over menu. In this menu, players will be asked to enter their name.
   #              The name will be stored alongside the player's score in a list called "highscore_entry", which is returned.

   pygame.display.set_caption("MANASWAP release version: 2.65")
   screen_dimensions = (480, 640)
   screen = pygame.display.set_mode(screen_dimensions)

   background = pygame.Surface(screen_dimensions).convert()
   background.fill(bg_color)

   message_font = pygame.font.Font("assets/fonts//fawn.ttf", 50)
   exit_text = message_font.render("EXCAVATION COMPLETE!", False, text_color)
   exit_text_center = manaLib.get_xcenter(screen_dimensions, exit_text.get_rect())
   
   text_font = pygame.font.Font("assets/fonts//vani.ttf", 25)
   your_score_text = text_font.render("Your score", False, text_color)
   your_score_text_center = manaLib.get_xcenter(screen_dimensions, your_score_text.get_rect())
   score_count = 0
   score_number = text_font.render(str(score_count), False, text_color)

   your_runes_text = text_font.render("Runes collected", False, text_color)
   your_runes_text_center = manaLib.get_xcenter(screen_dimensions, your_runes_text.get_rect())
   treasures_box = pygame.Surface((360, 350)).convert()
   treasures_box.fill((63, 50, 113))
   treasures_box_center = manaLib.get_xcenter(screen_dimensions, treasures_box.get_rect())
   list_font = pygame.font.Font("assets/fonts//vani.ttf", 36)

   exit_display = text_font.render("Return to main menu", False, text_color)
   exit_display_center = manaLib.get_xcenter(screen_dimensions, exit_display.get_rect())
   button_font = pygame.font.Font("assets/fonts//vani.ttf", 24)
   button_selected = pygame.Surface((260, 30)).convert()
   button_selected.fill((210, 180, 179))
   
   clock = pygame.time.Clock()
   keep_going = True
   mouseOver_exit = False
   delete_on = False
   # Sort the runes_collected into an alphabetical listing that includes how many of each
   # rune permutation collected. This will be blitted onto the game over screen.
   ordered_runes_list = []
   runes_collected.sort()
   for rune in runes_collected:
      quantity = 1
      while runes_collected.count(rune) > 1:
         quantity += 1
         runes_collected.remove(rune)
      ordered_runes_list.append([rune, quantity])

   while keep_going:
      clock.tick(30)

      # SCORE COUNTER 
      if score_count < score:
         # increase the player's score gradually from 0 to add dramatic effect
         if score > 210:  # The below increment does not work with scores less than 210. 
            score_count += int(score / 210) # 150 = frame rate * 7 seconds, so the counter increases until you reach score in 7 seconds
         else: # A special exception must be made for scores under 210, because int(score / 210) == 0 if score <210
            score_count += int(score / 50) 
         score_number = text_font.render(str(score_count), False, text_color)
         
      else:
         # score_count may overflow, if above statement False, set score_count to score to ensure right number shown
         score_count = score
         score_number = text_font.render(str(score_count), False, text_color)

      for ev in pygame.event.get():
         mousePos = pygame.mouse.get_pos()

         # CHECK FOR MOUSEOVER
         if 130 < mousePos[0] < 340 and 580 < mousePos[1] < 610:
            mouseOver_exit = True
         else:
            mouseOver_exit = False

         # CHECK FOR LEFT-CLICK
         if pygame.mouse.get_pressed()[0] == True:
            if 130 < mousePos[0] < 340 and 580 < mousePos[1] < 610:
               keep_going = False
               
      screen.blit(background, (0, 0))

      # blit all of the runes that were collected
      screen.blit(treasures_box, (treasures_box_center, 200))
      screen.blit(your_runes_text, (your_runes_text_center, 180))
      for i in range(0, len(ordered_runes_list)):
         rune_permutation = ordered_runes_list[i][0]
         quantity = "x " + str(ordered_runes_list[i][1])

         permutation_text = list_font.render(rune_permutation, False, text_color)
         quantity_text = list_font.render(quantity, False, text_color)

         # all even index elements are located on the left, all odd index elements are located on the right
         # two elements lie on each row of the list
         screen.blit(permutation_text, (100 + (i % 2) * 150, 220 + (i // 2) * 50)) 
         screen.blit(quantity_text, (190 + (i % 2) * 150, 220 + (i // 2) * 50))
         
      screen.blit(exit_text, (exit_text_center, 35))
      screen.blit(your_score_text, (your_score_text_center, 100))
      screen.blit(score_number, (manaLib.get_xcenter(screen_dimensions, score_number.get_rect()), 140))
      
      if mouseOver_exit:
         screen.blit(button_selected, (110, 580))
      screen.blit(exit_display, (exit_display_center, 580))
      pygame.display.flip()

   manaLib.play_gem_break_sound()
   pygame.time.wait(300)                  
   return


def score_menu(bg_color, text_color):
   # Parameters:     two tuples, "bg_color" and "text_color"
   # Returns:        None
   # Description:    this function handles the highscores menu; the function extracts the top ten scores from "highscores.txt";
   #              The menu does not display more than ten scores at any given time. I have not figured out how to make a scroll-bar
   #              so that the player can look at all the scores.
   
   pygame.display.set_caption("ManaSwap release version: 2.65")
   screen_dimensions = (480, 640)
   screen = pygame.display.set_mode(screen_dimensions)

   background = pygame.Surface(screen_dimensions).convert()
   background.fill(bg_color)

   title_font = pygame.font.Font("assets/fonts//vani.ttf", 38)
   title_text = title_font.render("HIGH SCORES", False, text_color)
   title_text_center = manaLib.get_xcenter(screen_dimensions, title_text.get_rect())
   
   button_font = pygame.font.Font("assets/fonts//vani.ttf", 22)
   exit_display = button_font.render("return to main menu", False, text_color)
   exit_display_center = manaLib.get_xcenter(screen_dimensions, exit_display.get_rect())
   button_selected = pygame.Surface((220, 30)).convert()
   button_selected.fill((210, 180, 179))

   score_font = pygame.font.Font("assets/fonts//vani.ttf", 24)
   top_ten_scores = open("assets/savedata//highscores.txt", "r+").readlines()[:10]

   clock = pygame.time.Clock()
   keep_going = True
   mouseOver_exit = False
   
   while keep_going:
      clock.tick(30)

      for ev in pygame.event.get():
         mousePos = pygame.mouse.get_pos()

         # CHECK FOR MOUSEOVER
         if 135 < mousePos[0] < 300 and 500 < mousePos[1] < 600:
            mouseOver_exit = True
         else:
            mouseOver_exit = False

         # CHECK FOR LEFT-CLICK
         if pygame.mouse.get_pressed()[0] == True:
            if 135 < mousePos[0] < 300 and 500 < mousePos[1] < 600:
               keep_going = False

      screen.blit(background, (0, 0))
      screen.blit(title_text, (title_text_center, 60))
      if mouseOver_exit:
         screen.blit(button_selected, (exit_display_center - 10, 530))
      screen.blit(exit_display, (exit_display_center, 530))

      # blit the scores onto the screen
      entry_number = 1 # start with the best score
      for score in top_ten_scores:
         highscore_entry = manaLib.convert_from_CSV(score) # converts CSV data into list
         name_text = score_font.render(highscore_entry[0], False, text_color)
         score_text = score_font.render(highscore_entry[1], False, text_color)
         ranking = score_font.render(str(entry_number), False, text_color)
         screen.blit(ranking, (30, 90 + entry_number * 35)) # entry's vertical position corresponds with its entry_number
         screen.blit(name_text, (90, 90 + entry_number * 35))
         screen.blit(score_text, (385, 90 + entry_number * 35))
         entry_number += 1 # increment the ranking, so that the next entry is the second best, then third best, etc
         
      pygame.display.flip()

   manaLib.play_gem_break_sound() # signal player he is leaving this menu
   pygame.time.wait(500)


def tutorial_type_selection_menu(bg_color, text_color):
   # Parametres:     two tuples, "bg_color" and "text_color"
   # Returns:        a string, "tutorial_choice"
   # Description:    this function handles the menu that allows the player to select a tutorial type; the player's choice
   #              is stored as a string and returned by this function.
   
   # INITIALIZE GRAPHICS
   pygame.display.set_caption("MANASWAP release version: 2.65")
   screen_dimensions = (480, 640)
   screen = pygame.display.set_mode(screen_dimensions)

   background = pygame.Surface(screen_dimensions).convert()
   background.fill(bg_color)

   button_font = pygame.font.Font("assets/fonts//vani.ttf", 25)
   description = button_font.render("Which tutorial would you like to view?", False, text_color)
   
   basic_button = button_font.render("How to Play", False, text_color) # basic as in basic tutorial
   basic_button_selected = pygame.Surface((160, 40)).convert()
   basic_button_selected.fill((210, 180, 179))
   
   excavation_button = button_font.render("Excavation Mode", False, text_color)   
   excavation_button_selected = pygame.Surface((220, 40)).convert()
   excavation_button_selected.fill((210, 180, 179))
   
   exit_button = button_font.render("Return to main menu", False, text_color)  
   exit_button_selected = pygame.Surface((270, 40)).convert()
   exit_button_selected.fill((210, 180, 179))

   # MAIN GAME LOOP
   clock = pygame.time.Clock()
   keep_going = True
   mouseOver = None

   while keep_going:
      clock.tick(30)

      for ev in pygame.event.get():
         mousePos = pygame.mouse.get_pos()

         # CHECK FOR MOUSEOVER
         if 130 <= mousePos[0] <= 280 and 120 <= mousePos[1] <= 180:
            mouseOver = "basic"
         elif 130 <= mousePos[0] <= 330 and 185 <= mousePos[1] <= 245:
            mouseOver = "excavation"
         elif 130<= mousePos[0] <= 280 and 275 <= mousePos[1] <= 335:
            mouseOver = "exit"
         else:
            mouseOver = None

         # CHECK FOR LEFT-CLICK
         if pygame.mouse.get_pressed()[0] == True:
            if 130 <= mousePos[0] <= 280 and 120 <= mousePos[1] <= 180:
               tutorial_choice = "basic"
               keep_going = False
            elif 130 <= mousePos[0] <= 330 and 185 <= mousePos[1] <= 245:
               tutorial_choice = "excavation"
               keep_going = False
            elif 130<= mousePos[0] <= 280 and 275 <= mousePos[1] <= 335:
               tutorial_choice = "exit"
               keep_going = False

      screen.blit(background, (0, 0))
      
      if mouseOver == "basic":
         screen.blit(basic_button_selected, (130, 120))
      elif mouseOver == "excavation":
         screen.blit(excavation_button_selected, (130, 185))
      elif mouseOver == "exit":
         screen.blit(exit_button_selected, (130, 275))
         
      screen.blit(description, (30, 60))
      screen.blit(basic_button, (145, 125))
      screen.blit(excavation_button, (145, 190))
      screen.blit(exit_button, (145, 280))
      
      pygame.display.flip()
      
   manaLib.play_gem_break_sound()
   pygame.time.wait(1000)
   return tutorial_choice


def treasures_menu(treasuresList, manaPoints, bg_color, text_color):
   # Parameters:     a multidimensional array, "treasuresList"; two tuples, "bg_color" and "text_color"
   # Returns:        None
   # Description:    responsible for creating the "treasures" menu, which allows the player to view the
   #                 treasures they have earned according to the multidimensional array, "treasuresList";

   # INITIALIZE PRIMARY MENU
   pygame.display.set_caption("ManaSwap release version: 2.65")
   screen_dimensions = (480, 640)
   screen = pygame.display.set_mode(screen_dimensions)

   background = pygame.Surface(screen_dimensions).convert()
   background.fill(bg_color)

   title_font = pygame.font.Font("assets/fonts//vani.ttf", 38)
   title_text = title_font.render("TREASURES", False, text_color)
   title_text_center = manaLib.get_xcenter(screen_dimensions, title_text.get_rect())

   button_font = pygame.font.Font("assets/fonts//vani.ttf", 22)
                              
   exit_display = button_font.render("return to main menu", False, text_color)
   exit_display_center = manaLib.get_xcenter(screen_dimensions, exit_display.get_rect())
   exit_button_selected = pygame.Surface((220, 30)).convert()
   exit_button_selected.fill((210, 180, 179))
                              
   next_display = button_font.render("next", False, text_color)
   next_button_selected = pygame.Surface((50, 30)).convert()
   next_button_selected.fill((210, 180, 179))
                              
   back_display = button_font.render("back", False, text_color)
   back_button_selected = pygame.Surface((50, 30)).convert()
   back_button_selected.fill((210, 180, 179))

   list_font = pygame.font.Font("assets/fonts//vani.ttf", 42)
   treasures_box = pygame.Surface((360, 460)).convert()
   treasures_box.fill((63, 50, 113))
   treasures_box_center = manaLib.get_xcenter(screen_dimensions, treasures_box.get_rect())
   treasures_highlight = pygame.Surface((180, 92)).convert()
   treasures_highlight.fill((210, 180, 179))
   treasures_box_page = 1 # if var is 1, then index 0 - 9 in treasuresList shown
                         # if var is 2, then index 10 - 19 in treasuresList shown,
                         # etc

   # INITIALIZE SYNTHESIS SUBMENU GRAPHICS
   # create the mana points counter
   manaPoints_font = pygame.font.Font("assets/fonts//vani.ttf", 16)
   manaPoints_display = manaPoints_font.render("Mana Points: " + str(manaPoints), False, text_color)

   # create the synthesis button and instructional message
   synthesis_message = manaPoints_font.render("Select a Treasure", False, text_color)
   synthesis_display = manaPoints_font.render("Synthesis", False, text_color)
   synthesis_button_selected = pygame.Surface((85, 25)).convert()
   synthesis_button_selected.fill((210, 180, 179))

   # create the confirmation window                     
   synthesis_confirm_window = pygame.Surface((380, 100)).convert()
   synthesis_confirm_window.fill((63, 50, 113))
   synthesis_confirm_window_center = manaLib.get_xcenter(screen_dimensions, synthesis_confirm_window.get_rect())
   synthesis_white_border = pygame.Surface((382, 102)).convert()
   synthesis_white_border.fill((255, 255, 255))
   synthesis_window_message = manaPoints_font.render("Synthesize \"rune\" for X mana points?", False, text_color)

   # create the yes button on confirmation window
   yes_display = manaPoints_font.render("Yes", False, text_color)
   yes_button_selected = pygame.Surface((60, 40)).convert()
   yes_button_selected.fill((210, 180, 179))
   # create the no button on confirmation window                           
   no_display = manaPoints_font.render("No", False, text_color)
   no_button_selected = pygame.Surface((60, 40)).convert()
   no_button_selected.fill((210, 180, 179))

   # INITIALIZE TREASURE ENTRY SUBMENU GRAPHICS
   treasure_entry_font = pygame.font.Font("assets/fonts//vani.ttf", 15)
   close_window_font = pygame.font.Font("assets/fonts//vani.ttf", 24)
                              
   treasure_entry_box = pygame.Surface((380, 400)).convert()
   treasure_entry_box.fill((63, 50, 113))
   treasure_entry_box_center = manaLib.get_xcenter(screen_dimensions, treasure_entry_box.get_rect()) # value is 50
   white_border = pygame.Surface((382, 402)).convert()
   white_border.fill((255, 255, 255))
                              
   close_window_button = close_window_font.render("Close window", False, text_color)
   close_window_button_center = manaLib.get_xcenter(screen_dimensions, close_window_button.get_rect()) # value is 166
   close_button_highlight = pygame.Surface((200, 34)).convert()
   close_button_highlight.fill((210, 180, 179))
   close_button_highlight_center = manaLib.get_xcenter(screen_dimensions, close_button_highlight.get_rect()) # value is 140
                              
   treasure_entry_tier = 1 # determines what page of the Treasure's story is displayed

   clock = pygame.time.Clock()
   keep_going = True
   mouseOver = None
   active_submenu = None      # determines which submenu (synthesis_confirm or treasure_entry) is active
   item_selected = None         # the Treasure that is selected
   synthesize_treasure = False # when True, selecting a Treasure gives the option of upgrading it instead of opening its textfile
   error_exists = False            # when True, there is an error with synthesis, either Treasure is already at max level or not enough mana points
   error_message = ""
   
   
   while keep_going:
      clock.tick(30)

      for ev in pygame.event.get():
         mousePos = pygame.mouse.get_pos()

         if active_submenu == None: # primary menu; this set of inputs is only available when a submenu is not active
                  # CHECK FOR MOUSEOVER
                  if 135 < mousePos[0] < 300 and 580 < mousePos[1] < 680: 
                     mouseOver = "exit"
                  elif 60 < mousePos[0] < 420 and 100 < mousePos[1] < 560: # mouse over a Treasure entry
                     mouseOver = (mousePos[1] - 100) // 92 * 2 + (mousePos[0] - 60) // 180 + 10 * (treasures_box_page - 1) # get coordinates of entry
                  elif 40 < mousePos[0] < 140 and 580 < mousePos[1] < 610:
                     mouseOver = "back"
                  elif 400 < mousePos[0] < 500 and 580 < mousePos[1] < 610:
                     mouseOver = "next"
                  elif 355 < mousePos[0] < 440 and 70 < mousePos[1] < 100:
                     mouseOver = "synthesis"
                  else:
                     mouseOver = None

                  # CHECK FOR MOUSE INPUT
                  if ev.type == MOUSEBUTTONDOWN:
                     error_exists = False
                     error_message = ""

                     if ev.dict['button'] == 4:
                        # move to the previous ten treasures
                        if treasures_box_page > 1:
                           treasures_box_page -= 1

                     elif ev.dict['button'] == 5:
                        # move to the next ten treasures
                        if treasures_box_page < len(treasuresList) // 10 + 1: # every page contains a maximum of 10 treasures, and possible one additional page with less than 10 treasures
                           treasures_box_page += 1
                     
                     elif ev.dict["button"] == 1:
                        if 135 < mousePos[0] < 300 and 580 < mousePos[1] < 680: # exit Treasures menu
                           keep_going = False
                           
                        elif 40 < mousePos[0] < 140 and 580 < mousePos[1] < 610:
                           # move to the previous page in list of Treasures
                           if treasures_box_page > 1:
                              treasures_box_page -= 1
                              
                        elif 400 < mousePos[0] < 500 and 580 < mousePos[1] < 610:
                           # move to the next page in list of treasures
                           if treasures_box_page < len(treasuresList) // 10 + 1:
                              treasures_box_page += 1

                        elif 355 < mousePos[0] < 440 and 70 < mousePos[1] < 100: # turn on Synthesis mode, next Treasure selected asks whether it will synthesis or not
                           synthesize_treasure = True 
                              
                        elif 60 < mousePos[0] < 420 and 100 < mousePos[1] < 560: # selecting a Treasure
                              
                              if not synthesize_treasure:                  # if we are not synthesizing, then selecting a Treasure brings up its description
                                 treasure_entry_tier = 1                   # begin at the first page of the Treasure's story
                                 item_selected = (mousePos[1] - 100) // 92 * 2 + (mousePos[0] - 60) // 180 + 10 * (treasures_box_page - 1)
                                 # calculate the index of the Treasure based on the graphical coordinates
                                 
                                 if item_selected > len(treasuresList) - 1 or treasuresList[item_selected][1] <= 0:  # make sure item_selected, which is an index of treasuresList, does not go over
                                    item_selected = None
                                    
                                 if item_selected != None:
                                    active_submenu = "treasure_entry" # tell the program to open a window to show the treasure entry
                                    treasure_name = treasuresList[item_selected][0] # string containing rune letters, such as "apt" or "ttu"
                                    with open("assets/dialogue//" + treasure_name + ".txt", "r") as myFile:
                                       treasureLines = myFile.readlines()
                                    
                              elif synthesize_treasure:                  # if we are synthesizing then selecting a Treasure brings up a confirmation window  
                                    item_selected = (mousePos[1] - 100) // 92 * 2 + (mousePos[0] - 60) // 180 + 10 * (treasures_box_page - 1)
                                    
                                    if item_selected > len(treasuresList) - 1:  # make sure item_selected, which is an index of treasuresList, does not go over
                                       item_selected = None
                                       
                                    elif treasuresList[item_selected][1] < 3: # you cannot spent points to raise a Treasure's tier higher than 3
                                       active_submenu = "synthesis_confirm"
                                       treasure_name = '"' + treasuresList[item_selected][0] + '"' # quotation marks + name + end quote
                                       synthesis_cost = 20000 * 2 ** (treasuresList[item_selected][1]) # to unlock: tier 1 = 20000 mana, tier 2 = 40000 mana, tier 3 = 80000 mana
                                       synthesis_window_message = manaPoints_font.render("Synthesize " + treasure_name+  " for " + str(synthesis_cost) + " mana points?", False, text_color)
                                       if synthesis_cost > manaPoints:
                                          error_exists = True
                                          error_message = "Not enough mana"
                                          active_submenu = None
                                          synthesize_treasure = False
                                          item_selected = None
                              
                                    else:
                                          error_exists = True
                                          error_message = "Already at max tier"
                                          active_submenu = None
                                          synthesize_treasure = False
                                          item_selected = None


         elif active_submenu != None: # there is a submenu active, override all inputs to the primary menu
                  # CHECK FOR MOUSEOVER
                  if active_submenu == "treasure_entry":
                        if 140 < mousePos[0] < 340 and 480 < mousePos[1] < 514:
                           mouseOver = "close"
                        else:
                           mouseOver = None
                           
                        if ev.type == MOUSEBUTTONDOWN:
                              if ev.dict["button"] == 1:
                                 if 140 < mousePos[0] < 340 and 480 < mousePos[1] < 514:
                                    item_selected = None
                                    active_submenu = None
                                    
                              elif ev.dict['button'] == 4:
                                 if treasure_entry_tier > 1:
                                    treasure_entry_tier -= 1
                                    
                              elif ev.dict['button'] == 5:
                                 if treasure_entry_tier < min(3, treasuresList[item_selected][1]): # use min() because if # of numbers Treasure unlocks exceeds 3, then list index error occurs
                                    treasure_entry_tier += 1
                              
                  elif active_submenu == "synthesis_confirm":
                        if 130 < mousePos[0] < 190 and 180 < mousePos[1] < 220:
                           mouseOver = "yes"
                        elif 220 < mousePos[0] < 280 and 180 < mousePos[1] < 220:
                           mouseOver = "no"
                           
                        if ev.type == MOUSEBUTTONDOWN:
                           if ev.dict["button"] == 1:
                              if 130 < mousePos[0] < 190 and 180 < mousePos[1] < 220:
                                 treasuresList[item_selected][1] += 1 # increase the Treasure tier
                                 manaPoints -= synthesis_cost
                                 manaPoints_display = manaPoints_font.render("Mana Points: " + str(manaPoints), False, text_color) 
                                 active_submenu = None
                                 item_selected = None
                                 synthesize_treasure = False
                                 
                              elif 220 < mousePos[0] < 280 and 180 < mousePos[1] < 220:
                                 active_submenu = None
                                 item_selected = None
                                 synthesize_treasure = False
                     
      # BLIT MAIN MENU
      screen.blit(background, (0, 0))
      screen.blit(treasures_box, (treasures_box_center, 100))

      if error_exists:
         error_display = manaPoints_font.render(error_message, False, text_color)
         screen.blit(error_display, (200, 70))
      
      screen.blit(title_text, (title_text_center, 20))
      if mouseOver == "exit":
         screen.blit(exit_button_selected, (exit_display_center - 10, 580))
      elif mouseOver == "back":
         screen.blit(back_button_selected, (40, 580))
      elif mouseOver == "next":
         screen.blit(next_button_selected, (400, 580))
      elif mouseOver == "synthesis":
         screen.blit(synthesis_button_selected, (355, 70))
      screen.blit(next_display, (400, 580))
      screen.blit(back_display, (40, 580))
      screen.blit(exit_display, (exit_display_center, 580))
      screen.blit(synthesis_display, (360, 70))
      screen.blit(manaPoints_display, (30, 70))

      # GIVE PLAYERS INSTRUCTIONS IF SYNTHESIS IS TURNED ON
      if synthesize_treasure and item_selected == None:
         screen.blit(synthesis_message, (200, 70))

      # HIGHLIGHT THE TREASURE THAT IS MOUSED OVER
      if type(mouseOver) == int: # mouseOver is only int when it is storing the index of a treasure it is hovering over
         screen.blit(treasures_highlight, (60 + 180 * (mouseOver % 2), \
                                                       100 + 92 * (mouseOver // 2) - 460 * (treasures_box_page - 1)))

      # BLIT THE LIST OF TREASURES
      first_entry_index = 0 + 10 * (treasures_box_page - 1)
      last_entry_index = 10 + 10 * (treasures_box_page - 1)
      for i in range(first_entry_index, min(last_entry_index, len(treasuresList) )):
         if treasuresList[i][1] == 0:
            entry = list_font.render(treasuresList[i][0], False, (100, 100, 100))
         else:
            entry = list_font.render(treasuresList[i][0], False, text_color)
         x = i % 10 
         screen.blit(entry, (80 + 160 * (x % 2), 120 + 92 * (x // 2)))

      # BLIT ACTIVE SUB-MENUS
      if active_submenu == "treasure_entry": # blit a window to show the Treasure the player has selected
         screen.blit(white_border, (treasure_entry_box_center  - 1, 119))
         screen.blit(treasure_entry_box, (treasure_entry_box_center, 120))
         if mouseOver == "close":
            screen.blit(close_button_highlight, (close_button_highlight_center, 480))
         screen.blit(close_window_button, (close_window_button_center, 480))
         
         y_adjust = 0
         for i in range(0 + 10 * (treasure_entry_tier - 1), 10 + 10 * (treasure_entry_tier - 1)):
            line = treasure_entry_font.render(treasureLines[i][:-1], False, text_color)
            screen.blit(line, (70, 150 + y_adjust * 30))
            y_adjust += 1

      elif active_submenu == "synthesis_confirm": # blit a confirmation window that asks whether player wants to synthesize or not
         screen.blit(synthesis_white_border, (synthesis_confirm_window_center - 1, 119))
         screen.blit(synthesis_confirm_window, (synthesis_confirm_window_center, 120))
         screen.blit(synthesis_window_message, (60, 130))
         if mouseOver == "yes":
            screen.blit(yes_button_selected, (130, 180))
         elif mouseOver == "no":
            screen.blit(no_button_selected, (220, 180))
         screen.blit(yes_display, (130, 180))
         screen.blit(no_display, (220, 180))
      
      pygame.display.flip()

   manaLib.play_gem_break_sound() # signal player he is leaving this menu
   pygame.time.wait(300)
   return treasuresList, manaPoints
   

manaPoints, treasuresDict = manaLib.load_save_file()
runes_collected = []
treasuresList = manaLib.treasuresDict_to_list(treasuresDict)

pygame.mixer.music.load("assets\soundtrack\\theme.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# COLOR GUIDE
# Main Menu Color             -       (83, 70, 133)           -        Purple; good, relaxed tone; conveys overall "mysterious wonder" tone of the game
# Gameplay Menu Color     -        (83, 79, 105)           -       Dull purple; low intensity allows gem colours to be more apparent, which is important
# Button Highlight Color      -        (210, 180, 179)       -       Light pink, for button highlights; good for grabbing attention without being instrusive
# Text Color                       -        (225, 225, 225)       -       Dull white, for text; pure white is not good, as it distracts the eye

# COLOR VARIABLES
# these will be inputted in functions to change their text color or background colors;
# making colors a function parameters makes changing the color scheme of the game
# less laborious
settings_bg_color1 = (83, 79, 105) # for play_normal_game() and play_basic_tutorial()
settings_bg_color2 = (83, 70, 133) # for all other menus()
settings_text_color = (225, 225, 225)

# MENU HANDLING LOOP
keep_going = True
while keep_going:
   menu_choice = main_menu(settings_bg_color2, settings_text_color)
   
   if menu_choice == "play":
      gameType = gametype_selection_menu(settings_bg_color2, settings_text_color)

      # create the gameBoard that the players will play on
      gameBoard = manaLib.generate_grid(6, 6)
      manaLib.addTiles(gameBoard, ["red", "green", "blue", "yellow"])
      
      if gameType == "normal":
         score = play_normal_game(gameBoard, settings_bg_color1, settings_text_color)
         manaPoints += score
         new_highscore_entry = normal_game_over_menu(score, settings_bg_color2, settings_text_color)
         
         if int(new_highscore_entry[1]) > 0: # WINNERS ONLY CLUB BOUNCER
            manaLib.add_to_highscores(new_highscore_entry[0], new_highscore_entry[1])
            
      elif gameType == "excavation":
         runeBoard = manaLib.generate_grid(6,6)
         manaLib.addTiles(runeBoard, ["a", "p", "t", "u"])
         score, runes_collected = play_excavation_game(gameBoard, runeBoard, settings_bg_color1, settings_text_color)
         manaPoints += score
         for rune in runes_collected:
            # runes_collected potentially contains multiple copies of the same
            # rune; this is not a very useful form of data; convert it into
            # values in treasuresDict;
            if len(rune) == 3:
               treasuresDict[rune] += 1
            elif len(rune) == 4:
               # treasures for 4 rune chains have not been implemented, this is a placeholder counter for 4 rune treasures
               treasuresDict["xxxx"] += 1
            elif len(rune) == 5:
               # treasures for 5 rune chains have not been implemented, this is a placeholder counter for 5 rune treasures
               treasuresDict["xxxxx"] += 1
         excavation_game_over_menu(score, runes_collected, settings_bg_color2, settings_text_color)
         treasuresList = manaLib.treasuresDict_to_list(treasuresDict)
         
   elif menu_choice == "tutorial":
      tutorial_choice = tutorial_type_selection_menu(settings_bg_color2, settings_text_color)
      if tutorial_choice == "basic":
         play_basic_tutorial(settings_bg_color1, settings_text_color)
      elif tutorial_choice == "excavation":
         treasuresDict = play_excavation_tutorial(treasuresDict, settings_bg_color1, settings_text_color)
         treasuresList = manaLib.treasuresDict_to_list(treasuresDict)
                
   elif menu_choice == "highscores":
      score_menu(settings_bg_color2, settings_text_color)    

   elif menu_choice == "treasures":
      treasuresList, manaPoints = treasures_menu(treasuresList, manaPoints, settings_bg_color2, settings_text_color)
      for i in range(0, len(treasuresList)):
         treasuresDict[treasuresList[i][0]] = treasuresList[i][1] # [0] is treasure name, [1] is amount of times treasure was collected
      
   elif menu_choice == "quit":
      keep_going = False

manaLib.save_to_file(manaPoints, treasuresDict)

pygame.quit()


