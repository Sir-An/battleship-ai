#
# Battle ship!!
#     AI
#     menus
#     file-saving
#     file-loading
#



from random import random

import string
num = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J", 10: "K", 11: "L", 12: "M", 13: "N", 14: "O", 15: "P", 16: "Q", 17: "R", 18: "S", 19: "T", 20:"Z"}
alph = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19}
#Correlations from top board to bottom board
correlation = {"A": "K", "B": "L", "C": "M", "D": "N", "E": "O", "F": "P", "G": "Q", "H": "R", "I": "S", "J": "T"}
anticorrelation = {"K": "A", "L": "B", "M": "C", "N": "D", "O": "E", "P": "F", "Q": "G", "R": "H", "S": "I", "T": "J"}
#Bottom board rows
shipboard = ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]


class Board: 
    """a battleship board that we can place ships on and take shots at
    includes actions such as: 
    - creating & displaying the board
    - placing ships
    - taking shots
    - checking for wins
    - and all general game stuff
    """

    #hitQueue = [] #used in AI move for targeting near hits

    def __init__(self, width = 11, height = 20):            #WORKS
        """Contructs the two boards that show your attacks and your ships
        """
        self.width = width
        self.height = height
        self.pboard = 42
        self.AIboard = 42 
        self.hitQueue = []
        self.data = [[' ']*(width + 1) for row in range(height)]

        # contructor does not return anything

    def __repr__(self):         #WORKS
        """This method returns a string representation
           for an object of type Board.
        """
        
        GREEN = "\033[92m"
        RESET = "\033[0m"

        s = ''                          # The string to return
        for row in range(0, (self.height) // 2):
            for col in range(0, self.width + 1):
                cell = self.data[row][col]
                if cell == "Ship":
                    s += f"{GREEN}[{RESET} {GREEN}]{RESET}"
                elif cell == "X":
                    s += f"{GREEN}[{RESET}X{GREEN}]{RESET}"
                else:
                    s += f"[{cell}]"
            s += " " + chr(ord('A') + row) 
            s += '\n'
    
        # Insert numbers under board
        for col in range(0, self.width + 1):
            s += " " + str(col) + " "

        # Insert separator between two boards
        s+= '\n' + '=' * (self.width * 3 + 4) + '\n\n'

        
        for row in range(self.height // 2, self.height):
            for col in range(0, self.width + 1):
                cell = self.data[row][col]
                if cell == "Ship":
                    s += f"{GREEN}[{RESET} {GREEN}]{RESET}"
                elif cell == "X":
                    s += f"{GREEN}[{RESET}X{GREEN}]{RESET}"
                else:
                    s += f"[{cell}]"
            s += " " + chr(ord('A') + row)
            s += '\n'


        # Insert numbers under board
        for col in range(0, self.width + 1):
            s += " " + str(col) + " "

        return s       # The board is complete; return it
    

    #
    ## How do I make it so that it records it for the top board of the AI and the bottom board for the player? 
    #

    def allowsGuess(self, row, col):        #WORKS 
        """ Check if a guess coordinate is allowed. 
            returns true if the guess is 
                1. on the board
                2. has the cell thing of "Ship" or " " AKA not guessed
            returns false if the guess if elsewise   
        """

        #checks if the letter in the row or col is valid in terms of its values or like is a value
        if row not in alph:
            return False
        elif 0 <= alph[row] < self.height and col in range(0, self.width + 1):
            #print("at row, col is:", self.data[alph[row]][col], "row", row, "col", col )
            if self.data[alph[row]][col] == "O" or self.data[alph[row]][col] == "X":
                return False
            else: 
                return True
        else: 
            return False


    def checkHit(self, row, col):       #WORKS
        """Checks if a guess at coordinate is a hit or miss
        Returns True if hit, False if miss
        """
        if self.data[alph[row]][col] == "X":
            print("something went wrong")
            input("hit return to continue [due to error in checkHit]:")
            return False

        if self.data[alph[row]][col] == "Ship":
            return True
        else:
            return False

    def addGuess(self, row, col):       #WORKS
        """Adds a guess to the board at the specified row and column
        with the specified value (hit or miss)
        """
        if self.checkHit(row, col) == True:
            self.data[alph[row]][col] = "X" #HIT
        else: 
            self.data[alph[row]][col] = "O" #MISS 

    def clear(self):            #WORKS
        """Clears whole board
        """
        
        for row in range(0, self.height):
            for col in range(0, self.width + 1):
                if self.data[row][col] in ("X", "O"):   # hit or miss markers
                    self.data[row][col] = " " 
    
    def canPlaceShip(self, row, col, HV):              #WORKS
        """ Checks if ship can be placed at specified row and column
            H = horizontal and the selected coordinate is the leftmost block
            V = vertical and the selected coordinate is the topmost block
            basically just makes sure the  '[ ]' is empty
        """
        shipSize = 2

    
        if HV == 'H':
            if col + shipSize > self.width + 1: # border check
                return False
            for i in range(0, shipSize):
                if self.data[alph[row]][col + i] != " ": # no placement on other ships check
                    return False
            return True
        
        elif HV == 'V':
            if alph[row] + shipSize > self.height: # border check
                return False
            for i in range(0, shipSize):
                if self.data[alph[row] + i][col] != " ": # no placement on other ships check
                    return False
            return True

    def isClearWithBuffer(self, r, c):
        """Checks to see if ship placement means it does not touch nearby ships"""
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = alph[r] + dr, int(c) + dc
                if 0 <= nr < len(self.data) and 0 <= nc < len(self.data[0]):
                    if self.data[nr][nc] == "Ship":
                        return False
        return True



    def placeShip(self, row, col, HV):      #WORKS   
        """ Places ship on board at specified row and column
            H = horizontal and the selected coordinate is the leftmost block
            V = vertical and the selected coordinate is the topmost block
            basically just makes the  '[ ]' is green
        """
        
        shipSize = 2  # for now, all ships are 2 units long

        while self.isClearWithBuffer(row, col) == True:
            if HV == 'H':
                for i in range(0, shipSize):
                    self.data[alph[row]][col + i] = "Ship"
            elif HV == 'V':
                for i in range(0, shipSize):
                    self.data[alph[row] + i][col] = "Ship"
            else: 
                raise ValueError("hv must be 'H' or 'V'") #rewrite this so it asks another time
        
    def checkWin(self):                  # WORKS 
        """ checks if all ships have sunk by shipsToWin method
        """
        if self.shipsToWin() == 0:
            return True
        else:
            return False
            
        #
        ## make something that makes sure the whole ship stays within bounds of board
        #

    def hostGame(self):
        """ sets up the game
        """

        import random

        # autocreates two different board, one for player and one for AI, print player board
        pboard = Board(10, 20)
        self.pboard = pboard
        AIboard = Board(10, 20)
        self.AIboard = AIboard




        print(pboard)

        
        # random ship set up for AI [5 ships]
        
        aiships_placed = 0
        while aiships_placed != 5:
            row = random.choice(shipboard)  #line replaced for num dictionary
            col = random.randint(0, 9)
            hv = random.choice(["H", "V"])

            if AIboard.canPlaceShip(row, col, hv):
                AIboard.placeShip(row, col, hv)
                aiships_placed += 1
            else:
                aiships_placed -= 1


        #prompts user to set up their board
        
        pships_placed = 0
        while pships_placed != 5:
            userstr = input("place your ships! (Ex: P, 4, H  , rows K-T, cols 0-10, H or V for horizontal or vertical): ").split(', ')
            urow = userstr[0].strip().upper()
            ucol = int(userstr[1].strip())
            uHV = userstr[2].strip().upper()
            if urow not in shipboard:
                print("Row must be from K–T.")
                pships_placed -= 1
                continue

            if not pboard.canPlaceShip(urow, ucol, uHV):
                print("Invalid placement, try again.")
                pships_placed += 1
                continue

            pboard.placeShip(urow, ucol, uHV)
            print(pboard)

        
        # game loop for guessing
        while True : 
            # Guess
            uguess = str(input("make your guess [topboard] in the format B3: ")).strip().upper()
            ugr = correlation[uguess[0]]
            ugc = int(uguess[1:])
            if AIboard.allowsGuess(ugr, ugc) == True:
                if AIboard.checkHit(ugr, ugc) == True:
                    pboard.data[alph[uguess[0]]][ugc] = "X"

                    print("hit!")
                else:
                    pboard.data[alph[uguess[0]]][ugc] = "O"

                    print("miss!")

                AIboard.addGuess(ugr, ugc)
            else: 
                print("invalid guess, try again.")
                continue
            print(pboard)

            # test sink:
            if AIboard.shipSunk(ugr, ugc):
                print("You sunk a ship!")
                print("you have", AIboard.shipsToWin(), "ships left to sink.")

            # test win:
            if AIboard.checkWin() == True:
                print("You win!!")
                print("Opponent Board")
                print(AIboard)
                break

            # AI Guess:
            #ai move needs to return a tuple that will be the row and col I will plug into
            row, col = AIboard.aiMove()  #row is a string (bottom board), col is am int'
            acorrow = anticorrelation[row]  #correlate to top board row
            if pboard.allowsGuess(row, col) == True:
                pboard.addGuess(row, col) # interacts with ships

                if pboard.checkHit(row, col) == True:
                    AIboard.data[alph[acorrow]][col] = "X"
                    
                    print("hit!")
                else:
                    AIboard.data[alph[acorrow]][col] = "O"
                    print("miss!")
            else:
                print(row,", ", col, "is not allowed but it should be")            
            
            
            
            print(pboard)

            # test sink:
            if pboard.shipSunk(row, col):
                print("Ship down!")
                print("you have", pboard.shipsToWin(), "ships left.")

            # test win:
            if pboard.checkWin() == True:
                print("AI wins, you lose :(")
                print("Opponent Board")
                print(AIboard)
                break


    def hostGame2(self):        
        """ sets up the game but only two ai players
        """

        import random

        # autocreates two different board, one for player and one for AI, print player board
        pboard = Board(10, 20)
        self.pboard = pboard
        AIboard = Board(10, 20)
        self.AIboard = AIboard


        
        # random ship set up for AI [5 ships] ai board
        aiships_placed = 0
        while aiships_placed != 5:
            row = random.choice(shipboard)  #line replaced for num dictionary
            col = random.randint(0, 9)
            hv = random.choice(["H", "V"])

            if AIboard.canPlaceShip(row, col, hv):
                AIboard.placeShip(row, col, hv)
                aiships_placed += 1
            else:
                aiships_placed += 0

        pships_placed = 0
        while pships_placed != 5: #pboard but AI
            row = random.choice(shipboard)  #line replaced for num dictionary
            col = random.randint(0, 9)
            hv = random.choice(["H", "V"])

            if pboard.canPlaceShip(row, col, hv):
                pboard.placeShip(row, col, hv)
                pships_placed += 1
            else:
                pships_placed -= 1

    
        print(pboard)
        print()
        print("<--------------------------- ship setup done --------------------------->" )
        print()

        
        # game loop for guessing
        while True : 
            # Guess
            # for top board pboard, bottom board AIboard
            row, col = AIboard.aiMove()  #row is a string (bottom board), col is am int'
            acorrow = anticorrelation[row]  #correlate to top board row
            if AIboard.allowsGuess(row, col) == True:

                if AIboard.checkHit(row, col) == True:
                    pboard.data[alph[acorrow]][col] = "X"
                    
                    print("AI1(pboard) hit @", acorrow, ", ", col)
                elif AIboard.checkHit(row, col) == False:
                    pboard.data[alph[acorrow]][col] = "O"
                    print("AI1(pboard) miss @ ", acorrow, ", ", col)
                else: 
                    print("Smth went wrong in pboard ai")

                AIboard.addGuess(row, col) # interacts with ships
            else:
                print(row,", ", col, "is not allowed PBOARD but it should be")
                input("return to continue")  
                        

            # test sink:
            if AIboard.shipSunk(row, col):
                print("You sunk a ship!")
                print("you have", AIboard.shipsToWin(), "ships left to sink.")
                #print("hitqueue from test sink:", self.hitQueue)

            # test win:
            if AIboard.checkWin() == True:
                print("You win!!")
                print("Opponent Board")
                print(AIboard)
                break

            # AI Guess:
            #ai move needs to return a tuple that will be the row and col I will plug into
            row, col = pboard.aiMove()  #row is a string (bottom board), col is am int'
            acorrow = anticorrelation[row]  #correlate to top board row
            if pboard.allowsGuess(row, col) == True:

                if pboard.checkHit(row, col) == True:
                    AIboard.data[alph[acorrow]][col] = "X"
                    
                    print("AI2(AIboard) hit!", row, ", ", col)
                else:
                    AIboard.data[alph[acorrow]][col] = "O"
                    print("AI2(AIboard) miss!", row, ", ", col)

                pboard.addGuess(row, col) # interacts with ships after check hit so that the x is in the right place
            else:
                print(row,", ", col, "is not allowed  AIBOARD but it should be")  
                input("return to continue")  

            
            
            print()
            print()
            print("board (AI1)___________________________________________________________________________________________")
            print()
            print(pboard)
            

            # test sink:
            if pboard.shipSunk(row, col):
                print("Ship down!")
                print("you have", pboard.shipsToWin(), "ships left.")

            # test win:
            if pboard.checkWin() == True:
                print("AIboard wins, you lose :(")
                print("Opponent Board")
                print(AIboard)
                break

            input("hit return to continue [end of hostGame2]")

        # Check if hit ship from other board
    
    # ships to win: (for AI)
    def shipsToWin(self):
        """ determines how many ships are left to sink for win condition
        """
        shipsLeft = 0

        N = 2
        A = self.data
        ch = "Ship"

        for row in range(0, self.height):
            for col in range(0, self.width):
                if inarow_Neast(ch, row, col, A, N) == True:
                    shipsLeft += 1
                elif inarow_Nsouth(ch, row, col, A, N) == True:
                    shipsLeft += 1
        return shipsLeft

    # ship sunk function
    def shipSunk(self, row, col):   #WORKS
        """ Checks if a ship has sunk by testing for where there are two X's in a row
            either H or V
            returns true for ship sunk and false if not sunk
            prints "ship sunk!" if sunk
        """
        shipsSunk = 0
        N = 2
        A = self.data
        ch = "X"

        for row in range(self.height):
            for col in range(self.width):
                if inarow_Neast(ch, row, col, A, N) == True:
                    shipsSunk += 1
                    print('Ship sunk!')
                elif inarow_Nsouth(ch, row, col, A, N) == True:
                    shipsSunk += 1
                    print('Ship sunk!')
                
        return shipsSunk

      

    # Ai Move
    def aiMove(self):
        """Makes a random move for AI
           Targets only unguessed cells using the allowsGuess method
           guesses at random until it hits a ship
           then targets the legal four corners around the hit until it sinks the ship
        """
        # first goes random
        import random
        
        if len(self.hitQueue) > 0:
            print("Went to AI Target")
            return self.aiTarget()
        
        else: 
            #print(" in AI Move self.hitQueue: ", self.hitQueue)
            aigr = random.choice(shipboard) #shipboard = lower letter rows
            aigc = random.choice(range(0, self.width + 1))
            if self.allowsGuess(aigr, aigc) == True:
        # until it hits a ship
                if self.checkHit(aigr, aigc) == True:
                    #print("[in AIMOVE] hit at", aigr, ", ", aigc)
                    self.hitQueue.append((aigr, aigc))
                return aigr, aigc
            else:
                return self.aiMove()  #recalls itself until it gets a valid guess


    

    def aiTarget(self):
        """ Targets around previous hits that have not sunk
            should only hit around the first in the list and does not consider directions that we have tried but were misses
            identifies legal 4 corners to hit
            clears all from hitQueue once ship sinks
        """
        # pulls first thing in hitQueue
        print("hitQueue:", self.hitQueue)
        aigr = self.hitQueue[0][0]
        aigc = self.hitQueue[0][1]

        # four corners around hit
        fourcorners = [(num[(alph[aigr] - 1)], aigc), #UP
                    (num[(alph[aigr] + 1)], aigc),    #DOWN 
                    (aigr, aigc - 1),                  #LEFT
                    (aigr, aigc + 1)]                  #RIGHT
        
        valid = []
        for r,c in fourcorners:
            if r in shipboard and self.allowsGuess(r, c):
                valid.append((r,c))

        if valid == []:
            self.hitQueue.clear()
            return self.aiMove()  #goes back to random if no valid targets

        
        while True:
            import random
            row, col = random.choice(valid)
            if row in shipboard and self.allowsGuess(row, col):
                break

        
        
        if self.checkHit(row, col) == True:
            #print("[in AI TARGET]hit at", row, col)
            if self.shipSunk(row, col) == True:
                self.hitQueue.clear()
            return row, col
        else: 
            #print("[in AI TARGET]miss at", row, col)
            
            return row, col




#Functions for checking in a row East, West, South, and North for shipSunk(self)
#r_start = row, c_start = col, N = 2, A = self.data, ch = "X"

#EAST
def inarow_Neast(ch, r_start, c_start, A, N):
    """ checks for N in a row eastward for element ch, returning
    True or False as appropriate
    """
    num_rows = len(A)      # Number of rows is len(A)
    num_cols = len(A[0])   # Number of columns is len(A[0])

    # check edges
    if r_start < 0 or r_start >= num_rows:
        return False
    
    if c_start < 0 or c_start > num_cols - N:
        return False

    for i in range(N):
        if A[r_start][c_start + i] != ch: #eastward
            return False
    return True

#WEST
def inarow_Nwest(ch, r_start, c_start, A, N):
    """ checks for N in a row eastward for element ch, returning
    True or False as appropriate
    """
    num_rows = len(A)      # Number of rows is len(A)
    num_cols = len(A[0])   # Number of columns is len(A[0])

    # check edges
    if r_start < 0 or r_start >= num_rows:
        return False
    
    if c_start < 0 + N or c_start > num_cols:
        return False

    for i in range(N):
        if A[r_start][c_start - i] != ch: #westward
            return False
    return True

#SOUTH
def inarow_Nsouth(ch, r_start, c_start, A, N):
    """ Checks for N in a row southward
    """
    num_rows = len(A)      # Number of rows is len(A)
    num_cols = len(A[0])   # Number of columns is len(A[0])

    # check edges
    if r_start < 0 or r_start > num_rows - N:
        return False
    
    if c_start < 0 or c_start >=  num_cols:
        return False

    for i in range(N):
        if A[r_start + i][c_start] != ch: #southward
            return False
    return True

#NORTH
def inarow_Nnorth(ch, r_start, c_start, A, N):
    """ Checks for N in a row southward
    """
    num_rows = len(A)      # Number of rows is len(A)
    num_cols = len(A[0])   # Number of columns is len(A[0])

    # check edges
    if r_start < 0 + N or r_start > num_rows:
        return False
    
    if c_start < 0 or c_start >=  num_cols:
        return False

    for i in range(N):
        if A[r_start - i][c_start] != ch: #northward
            return False
    return True





b = Board(10, 20)

#b.hostGame2()

