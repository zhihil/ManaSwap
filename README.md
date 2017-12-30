# ManaSwap
A Python match-three game

########################### INTRODUCTION ###########################
This textfile describes the purpose of every file within the ManaSwap folder.
To ensure the game functions properly, do not move or alter any files.

########################### HOW TO START MANASWAP ###########################
Step 1 - Double-click on main.py
Step 2 - Wait. Do not delete the black window.
Step 3 - Play the game.

########################### MANASWAP FOLDER ###########################
main.py -     This is the primary executable of ManaSwap. It takes functions from manaLib.py
	      and combines them into functions that generate menus. These menus make up the
	      entirety of the game. Double-click on this file to execute ManaSwap.
	      Do not attempt to alter this file.

manaLib.py -  This contains various functions that main.py utilises to create
	      the ManaSwap game. Double-clicking on this file will open a command-line window,
	      but this will effectively do nothing. You do not need to open this file to
	      play the game. Do not attempt to alter this file.

__pycache__ - This folder will be created when you run main.py. Deleting this folder
	      creates no problems, however, running main.py once more will simply create another
	      __pycache__.

########################### ASSETS FOLDER ###########################
The assets folder contains various images, textfiles, fontfiles and soundfiles 
used in the game. There are six distinct folders within the assets folder.

########### DIALOGUE FOLDER
The dialogue folder contains 24 .txt files. These textfiles are used to store
in-game dialogue. The textfiles have been carefully formatted, so adding new lines  
or deleting pre-existing ones may cause undesirable results.

basic_tutorial_messages.txt & excavation_tutorial_messages.txt - These contain the
	      instructions that will be given to the player during the basic and Excavation
	      tutorials. They called during the play_excavation_tutorial() and 
	      play_basic_tutorial() menus in main.py. Do NOT attempt to alter these files.

aaa, ppp, ttt, uuu, etc - These textfiles are denoted with a sequence of letters.
	      These files contain the descriptions that in-game Treasures will display. 
	      These files are called by treasures_menu() in main.py. Do NOT attempt to alter 
        these files.

########### FONTS FOLDER
The fonts folder contains 2 .ttf files. These are two unique fonts "fawnscript"
and "vani", stored in "fawn.ttf" and "vani.ttf" respectively, and they are used
to create fancy lettering for the game's text. These .ttf files are called
throughout main.py and in some functions in manaLib.py, whenever text needs to
be displayed on the screen. Do NOT attempt to alter these files.

########### IMAGES FOLDER
The images folder contains 4 .png files, which are 55 x 55 images of the different
coloured gems used by various functions in main.py and manaLib.py. Do NOT attempt 
to alter these files.

########### SAVEDATA FOLDER
The savedata folder contains 2 .txt files, which track the player's progress
through the game. It is highly recommended that you do NOT alter these files, however, you 
can cheat by altering some of the file data. Make sure that the new data that you enter
follows the pre-existing format of the file, otherwise the game may break.

highscores.txt - This consists of different player names and their scores stored from greatest at the top to 
		 lowest at the bottom. Different players and their scores are located on their own line, with 
		 no spaces inbetween. A single comma separates the player's name and their score. This .txt file
		 is opened by score_menu() in main.py and add_to_highscores() in manaLib.py.

			To manually enter a new highscore. Press "Enter" to create a new line, then on that 
		 line, write your name, a comma, and then your score. You entry may not initially appear on 
		 the highscores, as it only displays the top ten scores in the list. You can turn on main.py, 
		 play a Normal game and immediately hit "exit", which causes the program to sort the highscores. 
		 If your entry still does not appear at this point, then your score was too low to be displayed.

			Make sure that you do not add any empty lines between entries or any data
	   	 that is not formatted exactly as described above. 

treasures.txt  - This file begins with an integer at the beginning, representing the player's mana
		 points. In each successive line, there is a sequence of letters, a comma, and an integer 
		 value. These string and number entries are the different Treasures available in-game
		 and the number of times they were unlocked. This file is called by load_save_file()
		 and save_to_file() in manaLib.py

		 You can cheat by increasing the first integer to give free mana points. Make sure that 
		 the new number you enter is not a decimal and is written out as arabic numerals.
		 	In the following lines, the sequence of letters is the name of a treasure and
		 the integer represents the maximum tier of that treasure that was unlocked. You can
		 give yourself access to higher level treasures by changing the integer. Make sure that
		 the number you enter is not negative or a decimal. You can increase the integer to as
		 large as you would like, however there is no benefit to having a value greater than 3.

########### SOUNDEFFECTS FOLDER
The soundeffects folder contains 2 .wav files, which are used as sound-effects for the game. Do not
attempt to alter these files.

gem_break_sound.wav   - Commonly used when the player clicks a menu button or breaks gems in the game.
			This is triggered by the function play_gem_break_sound()

gem_landing_sound.wav - Used when the gems hit the ground after they fall. This is triggered by
			play_thump()

########### SOUNDTRACK FOLDER
The soundtrack folder contains 4 .mp3 files, which make up the game's soundtrack. By default
"theme.mp3" is played. To play one of three other songs, click on the gems in the main
menu. This is a secret feature.

theme.mp3 	 -  This is played by default and loops infinitely unless another track is selected.
		   Click on the red gem to play this track.

rainytheme.mp3   -  This is played when the blue gem on the main menu is selected. 

guitartheme.mp3  -  This is played when the yellow gem on the main menu is selected.

olombretheme.mp3 -  This is played when the green gem on the main menu is selected.

