# Monopoly Duel
#### Video Demo:  <URL HERE>
#### Description:
Text based two player monopoly game developed using python. Utilized concepts such as list manipulation and object oriented programming.
 
#### Code Analysis: 
  This project is my first python project which I have made and I am very excited to showcase it on GitHub. The entire developement process had many ups and down and I had to solve many bugs and logic issues when developing this game. As stated in the description above, this project is a mulitplayer (2 player) text based monopoly game. At the start of the game, the players are given instructions on the rules of the game and are prompted to select a token and a color. 
  The names are player 1 and 2. To implement this, I used the input function in Python and stored the entries inside of a player_profile class.
In order to define empty properties, I created an instance o fthe player class called "computer". After that, the program proceeds to set up the necessary variables and create the board. The board is an array where each entry is an instance of the property_profile class. I made use of OOP, something which we learned in the lectures on C. Within these classes, I also define different methods/ functions. I decided to use OOP as opposed to dictionaries because I felt as if classes and objects are very efficient and easy ways to store specific data. Also, by using a list to store a series of location objects, I was able to keep track of the different properties, who owns them, who is currently on top of a specific property, and the type of property etc. I was also able to easily maniplate the location of the piecies by randomizing a dice roll and then adding that number to the tokens current position in the array.
    Additionally, I created many functions near the top of the file which carry out specific actions (i.e. bankrupt, mortgage etc.). These functions would be called within the game loop depending on the outcome of the player's roll and the player's decisions. These functions would also take in multiple paramters such as the player, the property etc. and call on these properties to perform some sort of operations. Finally, the game loop. The game loop is an infinite loop which keep running until the playing variable becomes false (by the opponent declaring bankruptcy). The turn variable would be used to keep track of the player's turn: if turn = 1 then its player 1's turn and vice versa. Breaking up the loop even further is an if statement which checks if the player is in jail, if so, then play by the "jail rules" else play the turn as normal. 
  
 #### Instructions: 
  
Run the python file as any other, no need for any requirements since the program only uses libraries that come pre-installed with python.
