# Brennan Lu
# 24 May 2016 (?)
# Submitted to ICS3U1-03, Mr. Cope

# manaLib.py
#     This python file is the main executable for the ManaSwap game. It references from the manaLib.py library stored within the same folder.
# This python file is composed of several functions that handle the creation of game menus. Each function contains one and only one
# game loop, which is active when the function is called and ends when the function collapses. A "main" while loop at the very bottom
# of this file determines which menu is opened. No more than one menu is active at any time.

#     Each menu function is typically composed of three parts: graphics initialization, game loop, and data return. The graphics initialization defines
# graphics, images, and text. The main game loop takes the graphics defined by the first part and implements them. As well, the main game loop
# is takes player input and changes the game's variables accordingly. The data return stage typically returns some menu choice, although it also
# returns the player's final score in a game session;
#     Each menu functions' return value is rarely used by another function menu, this is because it is usually unnecessary. The few instances where
# a function uses another function's return value includes normal_game_over_menu() taking the player score from play_normal_game().

from random import randint
import pygame
pygame.mixer.pre_init(44100, -16, 2, 1024)

######################### NOTES ABOUT GRID #########################
# "grid" is a common variable being passed into the functions below
# for this version of ManaSwap, "grid" is limited to a 6 x 6 multidimensional array;
# for greater clarity, it is best if "grid" were written like so:

# grid = [ [None, None, None, None, None, None],
#             [None, None, None, None, None, None],
#             [None, None, None, None, None, None],
#             [None, None, None, None, None, None],
#             [None, None, None, None, None, None],
#             [None, None, None, None, None, None] ] 

# In the above representation, each sub-array in "grid" is called the "row";
# therefore, each vertical stack of 6 None values is said to form a "column";
# the None values in this representation are said to be the values of "grid";
# a value in "grid" can be one of None, "red", "blue", "green", or "yellow";
# a "gametile", "tile", or "gem" is any non-None value;

# if a value, grid[y][x], is said to be above another value, then that other
# value is defined as grid[y + 1][x]; in other words, the first index represents
# the value's row

# if a value, grid[y][x], is directly left of another value, then that other value
# is grid[y][x + 1]; thus, the second index represents the value's column

# "indice-form" is the tile's position in the grid, in terms of its indices; if a tile
# is defined as grid[y][x], then its first index or row is "y" and its second index or
# column is "x"; these coordinates are often expressed as tuples in the form: (y, x);

# "coordinate-form" is the position of a tile's graphical representation; if (y, x) is
# the indice-form of a tile in grid, then (60 * (x + 1) + 2.5, 60 * (y + 1) + 2.5) is
# position of the tile's rect's top-left corner; in this program, all tiles are 55 x 55 with a
# 5 pixel space between adjacent tile images.

# three or more consecutive tiles with the same colour in a row or column is called a "matching
# row" or "matching column", respectively; alternatively, it is referred to as a "matching group"

# if above any None value, there lies at least 1 tile, then we call this None value
# a "gap"; the shiftTiles() function fills in gaps by causing the tiles above a gap to
# shift down their column, as though affected by gravity, until no "gap" remains in the grid


######################### DATA MANIPULATION #########################
# These functions are responsible for processing the data that is crucial for the game play
# These functions do not call graphical manipulation functions below, at all. They may, however,
# call each other.

def generate_grid(rows, columns):
   # parameters:     two integers, "width" and "height"
   # returns:        a multidimensional array filled with None values that has the dimensions width x height
   # description:    this function generates a multidimensional array populated by None values; this
   #                 array is called a "grid" in this program;
   grid = []
   for i in range(0, rows):
      grid.append([None] * columns)
   return grid

def swapTile(tile1, tile2, grid):
   # parameters:     tuples: "tile1", "tile2"; multidimensional array: "grid"
   # returns:        a multidimensional array, "grid"
   # description:    this function swaps the two values in "grid", whose indices are
   #                 stored in the tuples "tile1" and "tile2"
   
   grid[ tile1[0] ][ tile1[1] ],   grid[ tile2[0] ][ tile2[1] ] = grid[ tile2[0] ][ tile2[1] ],  grid[ tile1[0] ][ tile1[1] ]
   return grid


def find_verticalMatches(tile, grid):
   # parameters:     tuple: "tile"; multidimensional array: "grid"
   # returns:        a list, "list_matches"; an integer, "veritcal_match_length"
   # description:    function starts from the initial tile, whose indice is stored in the tuple "tile"; the function looks
   #                 "above" and "below" the tile by decreasing then increasing its first index, respectively; if a tile
   #                 above or below the initial tile matches that tile's value, then it is stored and the next tile is
   #                 evaluated
   #                       note that this function does NOT return the initial tile in the list, but its matches 
   
   y_coord = tile[0]
   x_coord = tile[1]
   vertical_matches = []
   vertical_match_length = 0
   
   shift = 1 # look below the initial tile for any matches
   # while we are still in range of the column and the next tile is of the same value as the current
   while (y_coord + shift <= len(grid) - 1) and (grid[y_coord + shift][x_coord] == grid[y_coord][x_coord]):
       vertical_matches.append([y_coord + shift, x_coord])
       shift += 1 # look further down for any additional matches

   shift = -1
   while (y_coord + shift >= 0) and (grid[y_coord + shift][x_coord] == grid[y_coord][x_coord]):
       vertical_matches.append([y_coord + shift, x_coord])
       shift -= 1 # look further up for any additional matches

   if len(vertical_matches) >= 2:
      vertical_match_length = len(vertical_matches) + 1 # including the initial tile
   else:
      vertical_matches = []
      
   return vertical_matches, vertical_match_length


def find_horizontalMatches(tile, grid):
   # parameters:     tuple: "tile"; multidimensional array: "grid"
   # returns:        a list, "list_matches"; an integer, "veritcal_match_length"
   # description:    function starts from the initial tile, whose indice is stored in the tuple "tile"; the function looks
   #                 "left" and "right" of the tile by decreasing then increasing its first index, respectively; if a tile
   #                 left or right of the initial tile matches that tile's value, then it is stored and the next tile is
   #                 evaluated
   #                       note that this function does NOT return the initial tile in the list, but its matches 
   
   y_coord = tile[0]
   x_coord = tile[1]
   horizontal_matches = []
   horizontal_match_length = 0
   
   shift = 1      # look to the right of the initial tile by 1 for any matches
   # while we are still in range of the row and the next tile is of the same colour as the current
   while (x_coord + shift <= len(grid[0]) - 1) and (grid[y_coord][x_coord + shift] == grid[y_coord][x_coord]):
       horizontal_matches.append([y_coord, x_coord + shift])
       shift += 1 # look the right further for any additional matching tiles

   shift = -1    
   while (x_coord + shift >= 0) and (grid[y_coord][x_coord + shift] == grid[y_coord][x_coord]):
       horizontal_matches.append([y_coord, x_coord + shift])
       shift -= 1 # look to the left of initial tile by 1 more unit

   if len(horizontal_matches) >= 2:
      horizontal_match_length = len(horizontal_matches) + 1 # including the initial tile
   else:
      horizontal_matches = []
      
   return horizontal_matches, horizontal_match_length


def findMatches(tile, grid):
   # parameters:     tuple: "tile"; multidimensional array: "grid"
   # returns:        multidimensional array,  "list_matches"; integers, "horizontal_match_length" and 
   #                 "vertical_match_length"; multidimensional arrays, "horizontal_matches" and
   #                 "vertical_matches"              
   # description:    this function look at the tiles above, below, left and right of the input tile, called
   #                 the "initial tile"; if these tiles match the colour of the "initial tile", then their position is
   #                 stored in "indice-form" in a list, "total_matches", and returned; "total_matches" is useful for
   #                 deleting tiles, because the shape of the rows and columns formed don't matter;
   #                       this function also returns the length of any matching row and/or matching column
   #                 containing tile; this is useful for calculating score, because the length of the matching
   #                 group affects how much points are awarded per gem.
   #                       the last two return values are "horizontal_matches" and "vertical_matches"; this is
   #                 useful only in the Excavation game-mode, where the specific matched tile indices are
   #                 required to determine what rune permutation was formed.
   #                       colours are not the only possible matches that this function can find; this function
   #                 is also used to find matching runes for the Excavation game mode.
   
   y_coord = tile[0]
   x_coord = tile[1]
   total_matches = []
   horizontal_matches = []
   vertical_matches = []
   horizontal_match_length = 0
   vertical_match_length = 0

   horizontal_matches, horizontal_match_length = find_horizontalMatches(tile, grid)
   vertical_matches, vertical_match_length = find_verticalMatches(tile, grid)

   if len(horizontal_matches) >= 2: # two other tiles (+ initial tile) forms a proper matching row
      for i in horizontal_matches:
         total_matches.append(i) 
         
   if len(vertical_matches) >= 2:  # two other tiles (+ initial tile) forms a proper matching column
      for i in vertical_matches:
         total_matches.append(i) # ditto, forms a matching column
         
   if len(total_matches) > 0:
      total_matches.append([tile[0], tile[1]]) # don't forget to the add the initial tile!

   if len(horizontal_matches) >= 2: # two other tiles (+ initial tile) forms a proper matching row
      horizontal_matches.append([tile[0], tile[1]])
         
   if len(vertical_matches) >= 2:  # two other tiles (+ initial tile) forms a proper matching column
      vertical_matches.append([tile[0], tile[1]])

   return total_matches, horizontal_match_length, vertical_match_length, horizontal_matches, vertical_matches


def calculateScore(horizontal_lengths, vertical_lengths, bug_correction):
   # parameters:     two lists, "horizontal_lengths", and "vertical_lengths"; a boolean, "bug_correct"
   # returns:        integer value, "playerScore"
   # description:    the first two inputs to this function are two lists of integers,
   #                    each integer being the length of a matching row or column;
   #                    this function awards the players points based on the matching
   #                    group lengths; longer groups means more points per gem;

   #                       ABOUT "BUG_CORRECTION" VARIABLE
   #                       this function works as intended when the player is selecting tiles
   #                    to match; the issue arises when this function is used in the refreshBoard()
   #                    function; refreshBoard() calls calculateScore() on every single gem on the
   #                    gameboard in order to find and award points for randomly produced matching
   #                    rows or columns, and here lies the issue; every single gem is called for any
   #                    matches it makes, so in a matching row of length 3, each of the 3 gems is
   #                    called for their matches, but since each gem is part of the same matching row,
   #                    the same row is counted three times;
   #                       in general the bug works like this; if a matching row or column of length "n" is
   #                    processed by refreshBoard(), then refreshBoard() calls calculateScore() on this
   #                    matching row or column "n" times; mathematically, the bug causes points to be
   #                    awarded as (intended_score * n)
   #                       "bug_correction" is the simplest possible solution to this bug; it is a boolean
   #                    value that is True when this function is called in refreshBoard() and False otherwise;
   #                    when "bug_correction" is true, the points awarded by calculateScore() is divided by
   #                    "n"; this operation is essentially the inverse of the bug's effects; therefore, the effects
   #                    are cancelled out;
   
   playerScore = 0

   # here are the rules for scorestreaks
   #  50 points per gem for 3 gems in series; 150 points awarded
   #  75 points per gem for 4 gems in series; 300 points awarded
   #  100 points per gem for 5 gems in series; 500 points awarded
   #  125 points per gem for 6 gems in series; 750 points awarded
   #  0 points per gem for 7 gems in series, because rows and columns are 6 gems in length you cheater!
   #  etc
  
   #  if there is any overlap between matching rows or columns it doesn't matter
   if bug_correction == True:
      for group_length in horizontal_lengths:
         # since "n" == group_length,
         # we have, group_length * (50 + 25 * (group_length - 3)) / group_length)
         #            = 50 + 25 * (group_length - 3)
         playerScore +=  50 + 25 * (group_length - 3) 
         
      for group_length in vertical_lengths:
         playerScore += 50 + 25 * (group_length - 3)

   else:
      for group_length in horizontal_lengths:
         playerScore += group_length * (50 + 25 * (group_length - 3))
         
      for group_length in vertical_lengths:
         playerScore += group_length * (50 + 25 * (group_length - 3))

   return playerScore
         

def eliminateDuplicates(xlist):
   # parameters:     a list, "xlist", containing tuples; there may be duplicates of same tuple values
   # returns:        a list, "xlist" 
   # description:    this function eliminates all duplicates of elements in "xlist"

   duplicates_exist = True
   
   while duplicates_exist:
      
      duplicates_exist = False

      for i in xlist:
         if xlist.count(i) > 1:
            duplicates_exist = True
            xlist.remove(i)
           
   return xlist


def removeTiles(tiles_list, grid):
   # parameters:     a list, "tiles_list", containing tuples of length 2; a multidimensional array
   #                 "grid"
   # returns:        "grid" but with all tiles that have their indices recorded in "tiles_list",
   #                 have their values set to None
   # description:    this function sets all the values of all tiles described in tiles_list
   #                 to None
   
   for tile in tiles_list:
      grid[tile[0]][tile[1]] = None
      
   return grid


def shiftTiles(grid):
   # parameter:      tuple coordinates tile
   # returns:        multidimensional array: grid
   # description:    this function fills in any "gaps" in "grid", such that any tiles above the gap
   #                 are shifted down until the gap is replaced by a tile; this process is similar
   #                 to the tiles falling to the bottom due to gravity.

   # check each column 1 by 1
   # check each row in the column starting from the bottom-most row for tile (non-None values)
   # the first tile found should go to the bottom-most position
   # the second tile found should go to the second bottom-most position

   # Useful side-effect, if the bottom-most position already has a tile, then that tile
   # will be the first non-None value that the function encounters. The function switches
   # the bottom-most tile with the first tile (which are the same in this case), so effectively
   # nothing changes.

   # Note that the function deletes the original copy of the tile after it has moved the tile to a new position.
   # In the special case above, the tile should not be replaced with None, since the tile has
   # not changed position. This prevents tiles already in their intended location from being deleted. 

   for column in range(0, len(grid[0])):
      # grid[0] is an arbitrary row of grid. The amount of elements in the row is the number of columns
      
      target_row = len(grid) - 1                         # let the first tile found be moved to the bottom-most position of the column
      
      for row in range(len(grid) - 1, -1, -1):
         if grid[row][column] != None:
            grid[target_row][column] = grid[row][column] # move the tile to the bottom-most None value in column
            if row != target_row:                        # if the tile's original position was not the target position
              grid[row][column] = None                   # delete the tile in order to prevent duplicates
            target_row -= 1                              # go to the next bottom-most row

   return grid


def addTiles(grid, tileValues):
   # parameter:      a multidimensional array, "grid"; list "tileValues"
   # returns:        a multidimensional array, "grid"
   # description:    fills all empty tiles in "grid", represented by None value
   #                 with a random string that is stored in the list "tileValues";
   #                 while this function allows any number of distinct values to be
   #                 added to a grid object, it is not recommended to use any
   #                 list is not ["red", "blue", "green", "yellow"] or ["a", "p", "t", "u"] inside
   #                 this program, since it was not designed to handle any other list;

   possible_values = len(tileValues)
   for row in range(0, len(grid)):
      for column in range(0, len(grid[0])):
         if grid[row][column] == None:
            x = randint(0, possible_values - 1)
            grid[row][column] = tileValues[x]

   return grid


def identifyRunes(runeGrid, match_group):
   # parameters:     a multidimensional array, "matches_list"
   # returns:        a list, "rune_list"
   # descriptions:   takes a three-dimensional array "matches_list"; matches_list[x] is a matching
   #                 row or column; matches_list[x][y] is a tile, in indice-form, thatis part of the matching row;
   #                 or column; matches_list[x][y][z] is the row or column of the tile;
   #                    this function finds the rune permutation that is inscribed over each of the matching groups;
   #                 these permutations are converted into strings, which are processed by other functions for
   #                 the Excavation gamemode

   rune_list = []
   rune_permutation = ""
   for i in range(0, len(match_group)):
      tile = match_group[i]
      if runeGrid[tile[0]][tile[1]] != None:
         rune_list.append(runeGrid[tile[0]][tile[1]])
      else:
         match_group[i] = None # mark this tile for deletion, because we shouldn't remove it

   while None in match_group: # ignore any None values in the list
      match_group.remove(None)

   rune_list.sort()

   for char in rune_list:
      rune_permutation += char
   
   return rune_permutation, match_group


def convert_from_CSV(csv_string):
   # parameters:     a string, "csv_string"
   # returns:        a list of length two, "csv_contents" which has two elements, both strings
   # description:    this function extracts the information stored in csv format; it removes the newline
   #                 character and separates all of the contents of one row and one row only.
   
   csv_string = csv_string[:-1] # exclude the last character, which is "\n"
   csv_contents = csv_string.split(",")
   return csv_contents


def sort_highscores(highscores):
   # parameters:     a multidimensional array, "highscores" which contains sub-arrays with two elements, 
   #                 both strings; one is the name and the other the score of a highscores entry
   # returns:        None
   # description:    this function makes use of the insertion sort algorithm; this algorithm starts with an
   #                 element at the end of list; the algorithm moves this element until it is in order from greatest to least
   #                 within the sub-array, which is defined as index 0 to the index of the element.

   for i in range(1, len(highscores)):
      current_entry = highscores[i] # the actual score is located at index 1, the name is at index 0
      current_pos = i
      while current_pos > 0 and current_entry[1] > highscores[current_pos - 1][1]:
         # while we have not gone off the list and the value to the left is lesser than the current_score
         highscores[current_pos] = highscores[current_pos -1]
         current_pos -= 1

      highscores[current_pos] = current_entry

   
def add_to_highscores(name, score):
   # parameters:     a string, "name"; a string, "score"
   # returns:        None
   # description:    this function takes in the name and score of a new highscores entry and puts it in
   #                 "highscores.txt" so that all the entries in the textfile are ranked from highest
   #                 score to lowest.
   
   with open("assets/savedata//highscores.txt", "r+") as myFile:
      ranked_list = [[name, int(score)]]
      for csv_entry in myFile.readlines():
         list_entry = convert_from_CSV(csv_entry)
         ranked_list.append([list_entry[0], int(list_entry[1])])

      sort_highscores(ranked_list)

   with open("assets/savedata//highscores.txt", "w+") as myFile:
      for list_entry in ranked_list:
         myFile.write(list_entry[0] + "," + str(list_entry[1]) + "\n")


def load_save_file():
   # parameters:        None
   # returns:           an integer, "manaPoints", and a dictionary, "treasures"
   # descriptions:      unpackages the data stored in "treasures.txt"; the first line is an integer value, the
   #                    next two lines are CSV stored values for a rune permutation for a treasure and the
   #                    number of treasure pieces unlocked;
   
   treasures = {}
   manaPoints = 0
   with open("assets/savedata//treasures.txt", "r+") as myFile:
      manaPoints = int(myFile.readline()[:-1]) # cut off newline character
      saveData = myFile.readlines()
   for i in range(0, len(saveData)):
      entry = convert_from_CSV(saveData[i])
      treasures[entry[0]] = int(entry[1])

   return manaPoints, treasures


def save_to_file(manaPoints, treasures):
   # parameters:     an integer, "manaPoints", a dictionary, "treasures"
   # returns:        None
   # description:    reverse of load_save_file() above; takes in the dictionary treasures and integer
   #                 manaPoints and stores it in the savefile
   
   with open("assets/savedata//treasures.txt", "w+") as myFile:
      myFile.write(str(manaPoints) + "\n")
      for key in treasures.keys():
         myFile.write(key + "," + str(treasures[key]) + "\n")


def treasuresDict_to_list(treasuresDict):
   # parameters:     a dictionary "treasuresDict"
   # returns:        a multidimensional array, "treasuresList"
   # descriptions:   takes in the dictionary "treasuresDict" and converts it into a multidimensional array
   #                 containing sub-lists of length 2; this array is ordered alphabetically by the value
   #                 in index 0 in each sub-list, that is, the "rune permutation"

   treasuresList = []
   for permutation in treasuresDict.keys():
      treasuresList.append(permutation)
   treasuresList.sort()
   for i in range(0, len(treasuresList)):
      treasuresList[i] = [treasuresList[i], treasuresDict[treasuresList[i]]] # set value to [rune_permutation, quantity]

   return treasuresList



######################### GRAPHICAL AND AUDIO FUNCTIONS #########################
# These functions are responsible for displaying the information processed by the above data manipulation functions
# These function do not call any data manipulation functions at all, but may call each other; this category also
# includes auditory functions

def indice_to_coordinate(indice):
   # parameters:     a tuple, "indice"
   # returns:        a tuple, "coordinate"
   # description:    there are two ways to express a tile's position, indice form or coordinate form;
   #                 indice form will tell you the tile's location in the multidimensional array, "grid" or "gameBoard"
   #                 coordinate form will tell you the tile's location on the screen as a graphic. This function
   #                 converts an indice to a coordinate.
   return (60 * (indice[1] + 1) + 2.5, 60 * (indice[0] + 1) + 2.5)


def coordinate_to_indice(coordinate):
   # parameters:     a tuple, "coordinate"
   # returns:        a tuple, "indice"
   # description:    there are two ways to express a tile's position, indice form or coordinate form;
   #                 indice form will tell you the tile's location in the multidimensional array, "grid" or "gameBoard"
   #                 coordinate form will tell you the tile's location on the screen as a graphic
   
   # NEVER use this function while a tile's graphical image is moving, this function is specifically designed
   # for stationary tiles
   
   return (int((coordinate[1] - 2.5) / 60 - 1), int((coordinate[0] - 2.5) / 60 - 1))


def get_xcenter(screen_dimensions, rect):
   # parameters:     a tuple, "screen_dimensions"; a pyGame rect object, "rect";
   # returns:           an integer
   # description:    this function considers the dimensions of the screen it is working
   #                    with and finds the x-position that when blitted at, so that "rect" will
   #                    appear horizontally centered
   
   screen_xcenter = screen_dimensions[0] // 2 # get the whole screen object's centre's position
   textrect_length = rect.width - rect.left # find the text's length in pixels
   return screen_xcenter - (textrect_length // 2) # subtract to get the x-position we should blit text at


def get_tile_img(grid, tile, red_gem, blue_gem, green_gem, yellow_gem):
   # parameters:  a multidimensional array, "grid"; a tuple, "tile"; 4 img files;
   # returns:     a img file, "tile_img"
   # description:    this function reads "tile"'s value in grid and returns the corresponding
   #                 image file associated with the value
   
   row = tile[0]
   column = tile[1]
   
   if grid[row][column] == "red":
      tile_img = red_gem
   elif grid[row][column] == "green":
      tile_img = green_gem
   elif grid[row][column] == "blue":
      tile_img = blue_gem
   elif grid[row][column] == "yellow":
      tile_img = yellow_gem

   return tile_img


def get_tile_kinematics(grid, red_gem, green_gem, blue_gem, yellow_gem):
   # parameters:     a multidimensional array, "grid"; 4 img files, one for each tile colour
   # returns:        a multidimensional array, "tile_kinmatic_data", where each element of this array is another array
   #                 that contains the current position, target position, and colour of each tile on the board
   # description:    analyzes the parameter "grid" to see if there any gaps (represented by None value) that need to be
   #                 "plugged" by tiles that lie above it; this function returns a list that describes how exactly every tile img
   #                 should move in order to "plug" all of the gaps on the board.

   # NOTE: the way that this function works is that it starts searching from the bottom of a column
   # the first tile (non-None value) that the function encounters is set so that it goes in the bottom-most position in the column
   # the second tile that the function encounters goes in the second bottom-most position, etc
   
   # This process has an interesting and elegant property. To animate the tiles falling, we can say that all
   # tiles must move down until they reach their target, that is, current_position = target_position.
   # If the first tile that the function encounters is actually located in the bottom-most tile, then its current
   # position is equal to its target position. Therefore, this tile will not move at all under our restriction.
   # This means that a special exception does not need to be made for tiles already in the correct position.

   # See tile_shift_animation() to see how the list "tile_kinematic_data" is used 
   
   tile_kinematic_data = []
   
   for column in range(0, len(grid[0])):
      target_row = len(grid) - 1 # start from the bottom-most position in the column
      for row in range(len(grid) - 1, -1, -1):
         if grid[row][column] != None: # we have found a tile
            
            tile_current_position = (60 * (column + 1) + 2.5, 60 * (row + 1) + 2.5) # this is where the tile currently is
            tile_target_position = (60 * (column + 1) + 2.5, 60 * (target_row + 1) + 2.5) # this is where the tile should go
            # find the tile's colour so that graphical functions can animate it falling
            tile_image = get_tile_img(grid, (row, column), red_gem, blue_gem, green_gem, yellow_gem)
               
            tile_kinematic_data.append([tile_current_position, tile_target_position, tile_image])
            target_row -= 1 # now go to the next bottom-most position in the column.
            
   return tile_kinematic_data


def blit_gameBoard(grid, screen, red_gem, green_gem, blue_gem, yellow_gem):
   # parameters:     a multidimensional array, "grid"; a pyGame screen object;
   #                 img files, "red_gem", "green_gem", "blue_gem", and "yellow_gem"
   # returns:        None
   # description:    function takes in "grid" and creates a graphical
   #                 representation of the grid onto the screen using the passed img files
   #                 imgs are 55 x 55 pixels (I think that's what units they're in
   
   for row in range(0, len(grid)):
     for column in range(0, len(grid[0])):
         tile_img = get_tile_img(grid, (row, column), red_gem, blue_gem, green_gem, yellow_gem)
         screen.blit(tile_img, (60 * (column + 1) + 2.5, 60 * (row + 1) + 2.5))

def show_matches(matches_list, grid, runeGrid, screen, red_gem, green_gem, blue_gem, yellow_gem):
   # parameters:     a list of tuples, "matches_list"; a multidimensional array, "grid"; a multidimensional
   #                 array, "runeGrid", a pyGame screen object, "screen"; 4 img files, one for each tile colour;   
   # returns:        None
   # description:    function highlights matching tiles that form a row or column of length 3 or greater;
   #                    multidimensional "runeGrid" is an additional graphical element that must be blit if
   #                    the gamemode is "Excavation"; we set "runeGrid" = [] if we don't need to blit any
   #                    runes and pass a multidimensional array otherwise.
   
   img_cover = pygame.Surface((55, 55)).convert() # this is used to erase old frames in the animation
   img_cover.fill((103, 99, 125))

   for tile in matches_list:
      screen.blit(img_cover, (60 * (tile[1] + 1) + 2.5, 60 * (tile[0] + 1) + 2.5)) # put highlights in all the matched tiles
      
   blit_gameBoard(grid, screen, red_gem, green_gem, blue_gem, yellow_gem) # highlights are covering the tiles, so blit tiles again
   blit_runes(runeGrid, screen)
   pygame.display.flip()
   pygame.time.wait(600)                                                   # create a delay so that the matches are clearly shown

   # now cover over the highlights; the player has been given a visual cue as to where
   # the matches are; there is no need for them anymore
   
   img_cover = pygame.Surface((55, 55)).convert()           # this is used to erase old frames in the animation
   img_cover.fill((83, 79, 105))                            # background colour
   
   for tile in matches_list:
      screen.blit(img_cover, (60 * (tile[1] + 1) + 2.5, 60 * (tile[0] + 1) + 2.5)) # cover over the highlights
##   blit_gameBoard(grid, screen, red_gem, green_gem, blue_gem, yellow_gem) # ~ previous code, kept here in case bugs occur
      
   pygame.display.flip()


def blit_tile_highlight(tile_coord, screen):
   # parameters:     a tuple value, "tile_coord"; a pyGame screen object, "screen";
   # returns:        None
   # description:    function blits a surface object at the target coordinates, "tile", which highlights that tile
   #                 making it easier for players to know which tiles they've selected.
   
   img_cover = pygame.Surface((55, 55)).convert() # this is used to erase old frames in the animation
   img_cover.fill((103, 130, 125))

   screen.blit(img_cover, tile_coord)

   
def tile_move_animation(tile_cur_pos, grid, speed, direction, screen, tile_img):
      # parameters:     one tuple, "tile_cur_pos"; a multidimensional array, "grid"; a positive integer, "speed"; a string, "direction"
      #                 a pyGame screen object, "screen"; the image file for the tile, "tile_img"
      # returns:        a tuple, "new_tile_position"
      # description:    this function is used for animating tile movement; it returns a tuple, "new_tile_position", which can
      #                 be passed to this function again to move the tile again relative to its new position.

      # NOTE: if this function alone were to be used, the graphic will appear to "streak" because
      # previous images of the graphic were not erased. In order to properly erase the previous image
      # and produce the impression of animation, functions utilizing this tile_move_animation() should
      # define a 55 x 55 pyGame surface filled with the background colour and blit this surface over
      # previous images. This surface is called "img_cover"

      # The fact that tile_move_animation itself does not define this surface and erase previous images
      # was a deliberate design choice. Making the 55 x 55 surface a built-in feature of tile_move_animation
      # reduces the quality of animations. The swap_animaton() for example, must blit "img_cover" over
      # two tiles, but this function can only do so for one tile. What happens is that part of "img_cover"
      # overlaps the gem images, resulting in poor animation.
      
      if direction == "left":
         new_tile_position = (tile_cur_pos[0] - speed, tile_cur_pos[1]) 
      elif direction == "right":
         new_tile_position = (tile_cur_pos[0] + speed, tile_cur_pos[1]) 
      elif direction == "up":
         new_tile_position = (tile_cur_pos[0], tile_cur_pos[1] - speed) 
      elif direction == "down":
         new_tile_position = (tile_cur_pos[0], tile_cur_pos[1] + speed) 

      screen.blit(tile_img, new_tile_position)
      pygame.display.flip()

      return new_tile_position


def swap_animation(tile1, tile2, grid, screen, red_gem, green_gem, blue_gem, yellow_gem):
   # parameters:     two tuples, "tile1" and "tile2"; a multidimensional array, "grid"; pyGame screen, "screen";
   #                 4 img files, one for each colour gem
   # returns:        None
   # description:    swap_animation processes data and passes the results in tile_move_animation() above
   #                 swap_animation is not an "independent" animation, in that nothing new is being created, only a
   #                 more sophisticated application of tile_move_animation()

   img_cover = pygame.Surface((55, 55)).convert() # this is used to erase old frames in the animation
   img_cover.fill((83, 79, 105))
   
   tile1_img = get_tile_img(grid, tile1, red_gem, blue_gem, green_gem, yellow_gem)
   tile2_img = get_tile_img(grid, tile2, red_gem, blue_gem, green_gem, yellow_gem)

   tile1_start_pos = (60 * (tile1[1] + 1) + 2.5, 60 * (tile1[0] + 1) + 2.5)
   tile2_start_pos = (60 * (tile2[1] + 1) + 2.5, 60 * (tile2[0] + 1) + 2.5)
   tile1_cur_pos = (60 * (tile1[1] + 1) + 2.5, 60 * (tile1[0] + 1) + 2.5)
   tile2_cur_pos = (60 * (tile2[1] + 1) + 2.5, 60 * (tile2[0] + 1) + 2.5)
   
   if tile1_start_pos[0] < tile2_start_pos[0]:
      tile1_direc = "right" # tile1 will be moving right, towards tile2's initial position
      tile2_direc = "left" # tile2 will be moving left, towrds tile1's initial position
   elif tile1_start_pos[0] > tile2_start_pos[0]:
      tile1_direc = "left"
      tile2_direc = "right"
   elif tile1_start_pos[1] < tile2_start_pos[1]:
      tile1_direc = "down"
      tile2_direc = "up"
   elif tile1_start_pos[1] > tile2_start_pos[1]:
      tile1_direc = "up"
      tile2_direc = "down"

   clock = pygame.time.Clock()
   accel = True
   tile_speed = 1 # tile_speed must be set to 1, otherwise the animation goes out of sync and the game bugs out

   while tile1_cur_pos != tile2_start_pos and tile2_cur_pos != tile1_start_pos:
      clock.tick(30)
      screen.blit(img_cover, tile1_cur_pos)
      screen.blit(img_cover, tile2_cur_pos)

      # ACCELERATION FOR ANIMATION
      if accel:
         if tile_speed == 7: # do not change this; 8 is the maximum speed when tiles are shifting
            # animations look janky if the speed is altered
            accel = False
         tile_speed += 1
         
      elif not accel and abs(tile_speed) != 1:
         tile_speed -= 1
      # END OF ACCLERATION

      # Now move the images
      tile1_cur_pos = tile_move_animation(tile1_cur_pos, grid, tile_speed, tile1_direc, screen, tile1_img)
      tile2_cur_pos = tile_move_animation(tile2_cur_pos, grid, tile_speed, tile2_direc, screen, tile2_img)

      
def tile_destroyed_animation(tile_list, screen):
   # parameters:  a list, "tile_list"; a pygame screen object, "screen"
   # returns:     None
   # description: this function blits a 55 x 55 background coloured surface over
   #              the locations defined by tile_list; if any tiles imgs lie in these
   #              locations, then they are effectively erased
   
   img_cover = pygame.Surface((55, 55)).convert()
   img_cover.fill((83, 79, 105)) # background colour

   times_blitted = 0
   clock = pygame.time.Clock()
   
   while times_blitted < 10:
      clock.tick(30)
      for tile in tile_list:
         screen.blit(img_cover, ((tile[1] + 1) * 60 + 2.5 , (tile[0] + 1) * 60 + 2.5))
      times_blitted += 1
      pygame.display.flip()


def tile_shift_animation(grid, screen, tile_kinematic_data):
   # parameters:     a multidimensional array, "grid"; a pyGame screen object, "screen"; a multidimensional array,
   #                 "tile_kinematic_data"
   # returns:        None
   # description:    tile_kinematic_data is a list that contains kinematic data for each tile: target_position,
   #                 current_position, and tile_image; this function decreases current_position and blits
   #                 tile_img at current_position; this process repeats until current_position == target_position
   #                 for every single described in tile_kinematic_data

   img_cover = pygame.Surface((55, 55)).convert() # this is used to erase old frames in the animation
   img_cover.fill((83, 79, 105))
   
   speed = 4 # tile's falling speed
   if len(tile_kinematic_data) >= 1: # if there are no tiles to shift, make sure that doesn't create an infinite loop
     tiles_on_ground = False
   else:
      tiles_on_ground = True
   
   while not tiles_on_ground:
      tiles_on_ground = True
      for tile in tile_kinematic_data:
         # tile[0] is the tile's current position, so tile[0][0] is the x-position, tile[0][1] is the y-position
         # tile[1] is the tile's target position
         # tile[2] is the tile's image
         if tile[0] != tile[1]:
            tiles_on_ground = False
            screen.blit(img_cover, tile[0])
            tile[0] = tile_move_animation(tile[0], grid, speed, "down", screen, tile[2])
            if tile[0] == tile[1]: # if the tile has now reached the bottom
               play_thump()        # play a thumping sound; this can only once occur when the tile hits the ground
      pygame.display.flip()

   pygame.time.wait(200) # add a pause afterwards to give players time to read the changes


def blit_praise_matchLength(matchingRow_lengths, matchingColumn_lengths, text_color, screen):
   # parameters:     two lists, "horizontal_matches" and "vertical_matches"; a tuple, "text_color";
   #               a pygame screen object, "screen"
   # returns:         None
   # description:    blits text onto the screen; the word used depends on the largest match group in the
   #              lists "horizontal_matches" and "vertical_matches"; "text_font" and "text_color" are exactly
   #              what their name implies, these values are defined outside of functions and passed into them;

   text_font = pygame.font.Font("assets/fonts//fawn.ttf", 20)
   
   total_matches = matchingRow_lengths + matchingColumn_lengths
   max_streak = 0
   for scorestreak in total_matches:
      if scorestreak > max_streak:
         max_streak = scorestreak

   text_to_blit = text_font.render("", False, text_color)
   if max_streak == 3:
      text_to_blit = text_font.render("Mystical!", False, text_color)
   elif max_streak == 4:
      text_to_blit = text_font.render("Dazzling!", False, text_color)
   elif max_streak == 5:
      text_to_blit = text_font.render("Outrageous!!!", False, text_color)
   elif max_streak == 6:
      text_to_blit = text_font.render("EXTRAVAGANT", False, text_color)

   # erase any previous scorestreak word
   img_cover = pygame.Surface((155, 25)).convert()
   img_cover.fill((83, 79, 104))
   screen.blit(img_cover, (50, 445))
   screen.blit(text_to_blit, (50, 445))


def blit_praise_matchQuantity(total_matches, text_color, screen):
   # parameters:     two lists, "total_matches"; a tuple, "text_color";
   #              a pygame screen object, "screen"
   # returns:         None
   # description:    blits text onto the screen; the word used depends on the number of matching tiles in the
   #              list "total_matches";

   text_font = pygame.font.Font("assets/fonts//fawn.ttf", 20)
   
   number_tiles = len(total_matches)

   text_to_blit = text_font.render("", False, text_color)
   if number_tiles >= 10:
      text_to_blit = text_font.render("!!!EXALTED!!!", False, text_color)
   elif number_tiles >= 9:
      text_to_blit = text_font.render("INCANDESCENT", False, text_color)
   elif number_tiles >= 7:
      text_to_blit = text_font.render("Illuminating!!!", False, text_color)
   elif number_tiles >= 6:
      text_to_blit = text_font.render("Radiant!", False, text_color)
   elif number_tiles >= 5:
      text_to_blit = text_font.render("Blinding!", False, text_color)
   elif number_tiles >= 4:
      text_to_blit = text_font.render("Brilliant!", False, text_color)
      
   # erase any previous scorestreak word
   img_cover = pygame.Surface((165, 25)).convert()
   img_cover.fill((83, 79, 104))
   screen.blit(img_cover, (50, 485))
   # now blit the word
   screen.blit(text_to_blit, (50, 485))


def blit_runes(runeGrid, screen):
   # parameters:     a multidimensional array, "runeGrid"; a pygame screen object, "screen"
   # returns:     None
   # description:     this function blits all of the runes located in runeGrid onto the screen; 
   
   rune_font = pygame.font.SysFont("consolas", 30)
   atarn = rune_font.render("A", False, (255, 255, 255))
   phyxus = rune_font.render("P", False, (255, 255, 255))
   tentorii = rune_font.render("T", False, (255, 255, 255))
   unser = rune_font.render("U", False, (255, 255, 255))
   
   for row in range(0, len(runeGrid)):
     for column in range(0, len(runeGrid[0])):
         if runeGrid[row][column] == "a":
            screen.blit(atarn, (60 * (column + 1) + 20, 60 * (row + 1) + 12))
         elif runeGrid[row][column] == "p":
            screen.blit(phyxus, (60 * (column + 1) + 20, 60 * (row + 1) + 12))
         elif runeGrid[row][column] == "t":
            screen.blit(tentorii, (60 * (column + 1) + 20, 60 * (row + 1) + 12))
         elif runeGrid[row][column] == "u":
            screen.blit(unser, (60 * (column + 1) + 20, 60 * (row + 1) + 12))
                                   

def play_gem_break_sound():
   # parameters:     None
   # returns:        None
   # description:    plays the sound for when a gem breaks

   gem_break = pygame.mixer.Sound(file="assets\soundeffects\\gem_break_sound.wav")
   gem_break.play()


def play_thump():
   # parameters:     None
   # returns:        None
   # description:    plays the sound for when a gem breaks

   thump = pygame.mixer.Sound(file="assets\soundeffects\\gem_landing_sound.wav")
   thump.play()
   
   


######################### COMPOSITE FUNCTIONS #########################
# These functions combine both data manipulation and graphical functions from above

def refreshBoard(grid, runeGrid, screen, red_gem, green_gem, blue_gem, yellow_gem, text_font, text_color):
   # parameter:      two multidimensional arrays, "grid" and "runeGrid"; a pygame screen object, "screen"; 
   #                 "; 4 img files; a pygame font object, "text_font"; a tuple, "text_color"
   # returns:        a multidimensional array, "grid"; an integer, "score"
   # description:    takes "grid" and calls many of the functions defined above
   #                 to create a playable board; a playable board is defined as one where
   #                 there are no pre-existing rows or columns of 3 or more matching colours
   #                 and there are no gaps (represented by None value)
   
   playableBoard = False # a board is playable if there are no chains of 3 or more matching tiles are already existing
   score = 0 # a player score might create a domino effect of matched tiles, points are awarded for this

   while not playableBoard:
      playableBoard = True # reset playableBoard
      
      total_matches_list = [] # stores all randomly generated matches
      matchingRow_lengths = [] # stores the lengths of all matching rows formed
      matchingColumn_lengths = [] # stores the lengths of all matching columns formed

      tile_kinematic_data = get_tile_kinematics(grid, red_gem, green_gem, blue_gem, yellow_gem)
      tile_shift_animation(grid, screen, tile_kinematic_data)
      grid = shiftTiles(grid)
      grid = addTiles(grid, ["red", "blue", "green", "yellow"])

      # find all randomly occuring matches
      for row in range(0, len(grid)):
         for column in range(0, len(grid[0])):
            findMatches_return = findMatches((row, column), grid) # return values are three multidimensional arrays
            total_matches_list += findMatches_return[0]
            if findMatches_return[1] >= 3: # do not store matches_length that are not 3 or greater, as those are invalid
               matchingRow_lengths.append(findMatches_return[1])
            if findMatches_return[2] >= 3:
               matchingColumn_lengths.append(findMatches_return[2])
            
      show_matches(total_matches_list, grid, runeGrid, screen, red_gem, green_gem, blue_gem, yellow_gem)
      # refresh board, so changes are obvious
         
      if len(total_matches_list) != 0: # there are pre-existing matches in the grid
         total_matches_list = eliminateDuplicates(total_matches_list) # deletes any repeats of the same tile
         grid = removeTiles(total_matches_list, grid)

         # praise the player, depending on the longest match_group and the number of matches
         blit_praise_matchLength(matchingRow_lengths, matchingColumn_lengths, text_color, screen)
         blit_praise_matchQuantity(total_matches_list, text_color, screen)
            
         score += calculateScore(matchingRow_lengths, matchingColumn_lengths, True)
         play_gem_break_sound()
         playableBoard = False # findMatches() found matches for the tiles, so this is not a playable board

   return grid, score # matches_list is needed for tile_destroyed_animation to know which tiles to play the animation for


def refreshBoard_noGraphics(grid, screen, red_gem, green_gem, blue_gem, yellow_gem):
   # parameter:      a multidimensional array, "grid"
   # returns:        a multidimensional array, "grid"; an integer, "score"
   # description:    exactly as refreshBoard above, but does not put any graphical images on the screen or
   #                 calculate player score. The refreshBoard() function needs to be used in the beginning of the game to
   #                 generate a playableBoard, however, it is not attractive to see this process occuring as the game loads.
   #                 This function is created specifically to perform refreshBoard()'s purpose but to mask its actions,
   #                 for a better player experience;
   #                    technically, this function is not composite, because it has no graphical manipulation;
#                    this function is put here because it is closely related to refreshBoard() above;
   
   playableBoard = False # a board is playable if there are no chains of 3 or more matching tiles are already existing
   score = 0 # a player score might create a domino effect of matched tiles, points are awarded for this
   
   while not playableBoard:
      matches_list = [] # stores all randomly generated matches
      playableBoard = True # reset playableBoard

      grid = shiftTiles(grid)
      grid = addTiles(grid, ["red", "green", "blue", "yellow"])

      for row in range(0, len(grid)):
         for column in range(0, len(grid[0])):
            matches_list += findMatches((row, column), grid)[0] # we're not counting score here, so we don't need [1] and [2]
            
      if len(matches_list) != 0:
         matches_list = eliminateDuplicates(matches_list) 
         grid = removeTiles(matches_list, grid)
         playableBoard = False
         
   return grid, score 



######################### DEBUGGING FUNCTIONS #########################
# These functions will not be included in the final build, they are used to make debugging easier

def debug_print_grid(grid):
   # parameter:      a multidimensional array, "grid"
   # returns:        None
   # description:    prints "grid"
   
         for row in grid:
            for tile in row:
               print("{:^6}".format(tile), end=" ")
            print("\n")
         print("\n")





         
   
