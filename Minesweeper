from tkinter import *
from tkinter import messagebox
import random
class MineSweeperCell(Label):
    '''represents a MineSweeper cell'''
    colors = ['black','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
    
    def __init__(self,master,coord, isBomb):
        '''MineSweeperCell(master,coordm isoB) -> MineSweeperCell
        creates a new blank MineSweeperCell with (row,column) coord'''
        Label.__init__(self,master,height=1,width=2,text='',\
                       bg='white',font=('Arial',24), relief = RAISED)
        self.coords = coord  # (row,column) coordinate tuple
        self.number = 0  # 0 represents an empty cell
        self.clicked = False # if cell has already been clicked
        self.color = self.colors[self.number]
        self.isBomb = isBomb
        # DELETE THIS
        if self.isBomb:
            self['text'] = '∫'
        # set up listeners
        self.bind('<Button-1>',self.change)
        self.bind('<Button-2>', self.toggle_flagged)
        
    def change(self, event):
        ''' MineSweeperCell.change()
        only works on cells that haven't been clicked
        calls the master's goto_lose_screen function if cell is bomb
        Else displays the number of surrounding bombs and uses the master's
        autoexpose method to expose all of the surrounding blank cells'''
        if not self.clicked: # check if button has already been clicked
            if self.isBomb: # if the cell is a bomb
                if self.master.firstClick: # prevent user from getting a bomb on first click
                    self.master.change_bomb(self.coords)  
                    self.master.firstClick = False
                else:
                    self.master.goto_lose_screen() # go to the losing screen
            else:
                self.master.firstClick = False 
                self.number = self.master.find_bombs(self.coords) # find the number of bombs by using the master's function
                #if self.number > 0: # if player click on a blank square
                self['text'] = str(self.number) # change the cell's text to display the number of bombs
                self['bg'] = 'lightgray'
                self['fg'] = self.colors[self.number] # change the color of the cell to correspond with it's number
                self.clicked = True # make the button no longer clickable
                self.master.autoexpose(self.coords) # expose all of the surrounding blank cells
                self.master.check_for_win() # check if player has won 
                
    def toggle_flagged(self, event):
        '''MineSweeperCell.toggle_flagged()
        flags or unflags the cell
        if cell becomes flagged it displays an asterix
        otherwise the cell no longer displays an asterix'''
        if self.isBomb or not self.clicked:
            
            if self['text'] == '*': # if cell is flagged
                self['text'] = '' # remove the asterix
                self.master.bombsRemaining += 1 # add one to the bombs remaining counter
                self.master.bombsRemainingLabel['text'] = str(self.master.bombsRemaining) # update the bombss remaining label
            
            else: # if the cell isn't flagged
                self['text'] = '*' # make it flagged
                self.master.bombsRemaining -= 1
                self.master.bombsRemainingLabel['text'] = str(self.master.bombsRemaining)
        # otherwise do nothing
            
    def get_coords(self):
        '''MineSweeperCell.get_coords() -> tuple
        returns the cell's coords'''
        return self.coords

    def is_bomb(self):
        '''MineSweeperCell.is_bomb() -> Boolean
        returns True if the cell is a bomb and
        False if not'''
        return self.isBomb
    
    def change_bomb(self, isBomb):
        '''MineSweeperCell.change_bomb()
        Makes the cell a bomb if isBomb is True
        and a normal cell if isBomb is False'''
        self.isBomb = isBomb

    def is_flagged(self):
        '''MineSweeperCell.is_flagged()
        returns True if the cell is flagged
        and False if not'''
        return self['text'] == '*'

    def is_clicked(self):
        '''MineSweeperCell.is_clicked() -> Bool
        returns True if cell is clicked and
        false if not'''
        return self.clicked

class MineSweeperGrid(Frame):
    ''' object for a MineSweeper grid'''
    def __init__(self, master, width, height, numBombs):
        '''MineSweeperGrid(master)
        creates a new blank MineSweeper grid'''
        # intialize a new Frame
        Frame.__init__(self, master, bg = 'black')
        self.grid()
        self.firstClick = True # set attribute for first click
        # store the width and height attributes
        self.width = width
        self.height = height
        
        self.numBombs = numBombs # store the number of bombs
        self.bombCellCoords = [] # list for the coordinates of the bomb cells
        self.cellCoords = [] # list of all the possible coordinates
        for column in range(self.width): # for every column
            for row in range(self.height): # for every row
                self.cellCoords.append((column, row)) # append a tuple representing the current coordinates
        
        for bomb in range(numBombs): # for every bomb
            bombCell = random.choice(self.cellCoords) # pick a random tuple of coordinates to be a bomb
            self.bombCellCoords.append(bombCell) # append that tuple to the list of bomb cell coords
            self.cellCoords.remove(bombCell) # remove that tuple from the list of cellCoords to prevent it from being picked twice

        self.mineSweeperCells = [] # embedded list of columns of minesweeper cells
        for column in range(self.width): # for every column
            columnCells = [] # list of all the cells in a column
            for row in range(self.height): # for every row
                isBomb = (column, row) in self.bombCellCoords # check if the current cell will be a bomb
                cell = MineSweeperCell(self, (column, row), isBomb) # create the cell
                cell.grid(row = row, column = column) # grid the cell
                columnCells.append(cell) # append the cell to the list of column cells
            self.mineSweeperCells.append(columnCells) # append the list of column cells to the list of minesweeper cells
            
        self.bombsRemaining = self.numBombs
        self.bombsRemainingLabel = Label(self, text = str(self.numBombs), font=('Arial', 24))
        self.bombsRemainingLabel.grid(row = self.height, column = 0, columnspan = self.width )

    def goto_lose_screen(self):
        ''' MineSweeperGrid.goto_lose_screen()
        raises a message box telling the player that they have lost
        displays all of the bombs'''
        messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)
        for column in self.mineSweeperCells: # for every cell
            for cell in column:
                
                if cell.get_coords() in self.bombCellCoords: # if it is a bomb cell
                    # if it isn't already flagged
                    if not cell.is_flagged():
                        # flag the cell and make it red
                        cell['text'] = '*'
                        cell['bg'] = 'red'

        
           
    def goto_win_screen(self):
        ''' MineSweeperGrid.goto_win_screen()
        raises a message box telling the player that they have won'''
        messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)


    def find_adjacent_cells(self, coords):
        adjCells = []
        column = coords[0]
        row = coords[1]
        for currRow in range(3):
            
            currCellRow = (row + 1) - currRow # find the current cell's row
            
            for currColumn in range(3):
                
                if currRow != 1 or currColumn != 1: # avoid checking original cell
                    
                    currCellCol = (column + 1) - currColumn # find the current cell's column
                    
                    if currCellRow >= 0 and currCellRow <= self.height - 1 and currCellCol >= 0 and currCellCol <= self.width - 1: # if the cell is on the grid
                        adjCells.append(self.mineSweeperCells[currCellCol][currCellRow])
                        
        return adjCells

    def find_bombs(self, coords):
        ''' MineSweeperGrid.find_bombs() -> int
        returns an integer representing the number of
        adjacent squares that are bombs'''
        bombCounter = 0 # intialize the bomb counter
        adjCells = self.find_adjacent_cells(coords) # find adjacent cells
        
        for cell in adjCells: # for every adjacent cell
            if cell.is_bomb(): # if it is a bomb
                bombCounter += 1 # add one to the bomb counter 
        return bombCounter
    
    def autoexpose(self, coords):
        ''' MineSweeperGrid.autoexpose()
        exposes all of the surrounding squares that are blank'''
        pass
        
    def check_for_win(self):
        ''' MineSweeperGrid.check_for_win()
        checks if player has won the game and uses the
        goto_win_screen method if so'''
        hasWon = True
        # for every cell
        for column in self.mineSweeperCells:
            for cell in column:
                        
                if not cell.is_clicked(): # check if cell has not been clicked on or flagged
                    hasWon = False # if player has not yet won, hasWon = False
                    
        if hasWon: # if player has won
            self.goto_win_screen() # go to win screen
            
    def change_bomb(self, coords):
        ''' MineSweeperGrid.change_bomb()
        removes a bomb from the cell at coords if there is one
        and reassigns it to a random cell
        coords -> tuple: (row, column) that represents the cell which will
        have it's bomb removed and reassigned'''
        column = coords[0] # find the column
        row = coords[1] # find the row
        cell = self.mineSweeperCells[column][row] # find the cell
        self.bombCellCoords.remove(coords) # remove the cell's coordinates from the list of bomb cell coords
        
        if cell.is_bomb(): # if the cell is a bomb
            cell.change_bomb(False) # remove the bomb from the cell
            mineSweeperCells = self.mineSweeperCells[:] # create a copy of the mineSweeperCells
        
            # remove the cell that had the bomb removed to prevent the same cell from getting chosen for a bomb
            for item in mineSweeperCells:
                if cell in item:
                    item.remove(cell)

            # choose a cell to have the new bomb 
            chosenColumn = random.choice(mineSweeperCells) # chose the column the the new bomb will be in
            chosenCell = random.choice(chosenColumn) # choose a cell from the chosen column to contain the new bomb
            chosenCell.change_bomb(True) # make the chosen cell contain a bomb
            self.bombCellCoords.append(chosenCell.get_coords()) # add the new cell's coordinates to the list of bomb cell coords
            #DELETE THIS
            chosenCell['text'] = 9
            cell['text'] = ''
            

def play_minesweeper(width, height, numBombs):
    '''play_minesweeper(width, height, numBombs)
    width is an integer representing the width of the grid
    height is an integer representing the height of the grid
    numBombs is an integer representing the number of bombs in the grid
    plays a game of minesweeper with a grid that is width units wide,
    height units tall, and has numBombs bombs'''
    root = Tk()
    root.title('Minesweeper')
    sg = MineSweeperGrid(root, width, height, numBombs)
    root.mainloop()
    
play_minesweeper(10, 8, 10)