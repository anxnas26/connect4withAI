#libraries setup
from numpy import square
import pygame
import sys

import math
import random
import time
from time import sleep
import copy

print("\n\nBy: Anas")
print("email: anxnas26@gmail.com\n\n")

print("*** CONNECT4 GAME ***\n\n")

sleep(1)

#Setup Board

blue =  (3, 155, 229)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)

pygame.init()

mainBoard = [
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0]
]

def resetBoard(board): #useful method for testing etc. clears up the board
  for row in range(6):
    for col in range(7):
      board[row][col] = 0

#Helper methods 

def printBoard(board): #Drawing the board on console
  print("   1   2   3   4   5   6   7")
  
  for row in range(6):
    print(" |---+---+---+---+---+---+---|")
    print(" | ", end = '')
    
    for col in range(7):
      if board[row][col] == 0:
        print( ' ' + " | ", end = '')
      else:
        print( str(board[row][col]) + " | ", end = '')
    print("")
  print(" |---+---+---+---+---+---+---|")
  print('')


def placeTile(currentBoard, col, piece):  #Method for Placing Tile in Board
  y=5
  for row in range(6):
    # if currentBoard[0][col] != 0:
    #   print("Column is full.\n")
    #   break
    
    if currentBoard[y][col] == 0:
      currentBoard[y][col] = piece
      break
    elif currentBoard[y][col] != 0:
      y-=1
      
    else:
      print("Error.")
      break

def removeTile(currentBoard, col, piece):  #Method for Removing Tile in Board
  y=0
  for i in range(6):
    if currentBoard[y][col] == piece:
      currentBoard[y][col] = 0
      break

    elif currentBoard[y][col] == 0:
      y+=1
    else:
      break
    
def allowedMove(currentBoard, col): #Checks if move is legal (wont give an error) (PvP)
  continues = True
  
  if choice >= 7 or choice <0:
    # print("\nColumn does not Exist. Try Again.\n")
    continues = False
    return continues
    
  elif currentBoard[0][col] != 0:
    # print("\nColumn is full. Try Again.\n")
    continues = False
    return continues
    
  return continues


def getAllowedMoves(board): #Returns list with available moves (AI)
  moves = []
  for i in range(7):
    if allowedMove(board, i):
      moves.append(i)
  return moves

def gameWinX(Board, tile): #Count 4 in a row X 
  counter = 0
  win = False
  for row in range(6):
    for col in range(7):
      if Board[row][col] == tile:
        counter +=1
      else:
        counter = 0
      if counter == 4:
        win = True
        break
    counter = 0
  return win
#Count 4 in a row Y
def gameWinY(Board, tile):
  counter = 0
  win = False
  for col in range(7):
    for row in range(6):
      if Board[row][col] == tile:
        counter +=1
      else:
        counter = 0
      if counter == 4:
        win = True
        break
    counter = 0
  return win

def gameWinNE(Board, tile): #Count 4 in a row Diagonal NE
  counter = 0
  win = False
  for x in range(12):
    if x<=5:
      for i in range(x,-1,-1):
        if Board[i][x-i] == tile:
          counter +=1
        else:
          counter = 0
        if counter == 4:
          win = True
          return win

    else:
      for i in range(5,x-7,-1):
        if Board[i][x-i] == tile:
          counter +=1
        else:
          counter = 0
        if counter == 4:
          win = True
          return win
        
    counter = 0
  return win

def gameWinSE(Board, tile): #Count 4 in a row Diagonal SE
  counter = 0
  win = False
  
  for x in range(12):
    if x<=5:
      for i in range(x,-1,-1):
        if Board[5-i][x-i] == tile:
          counter += 1
        else:
          counter = 0
        if counter == 4:
          win = True
          return win
      
    else:
      for i in range(5,x-7,-1):
        if Board[5-i][x-i] == tile:
          counter += 1
        else:
          counter = 0
        if counter == 4:
          win = True
          return win

    counter = 0      
      
  return win
#Uses the counting 4inarow methods in one method
def winningBoard(Board, tile):
  win = False
  if gameWinX(Board, tile) or gameWinY(Board, tile) or gameWinNE(Board, tile) or gameWinSE(Board, tile):
    win = True
    return win


  
#AI Methods


#Tilecounter helper methods
def tileCounterX(Board, tile, count): #Counts tiles in a row Horizontally
  counter = 0
  counts = 0
  for row in range(6):
    for col in range(7):
      if Board[row][col] == tile:
        counter +=1
      else:
        counter = 0
      
      if counter == count:
        counts += 1
        counter = 0
  
    counter = 0
  return counts
def tileCounterY(Board, tile, count): #Counts tiles in a row Vertically
  counter = 0
  counts = 0
  for col in range(7):
    for row in range(6):
      if Board[row][col] == tile:
        counter +=1
      else:
        counter = 0
      if counter == count:
        counts += 1
        counter = 0
        
    counter = 0
  return counts
def tileCounterNE(Board, tile, count): #Counts tiles in a row Diagonal NE
  counter = 0
  counts = 0
  for x in range(12):
    if x<=5:
      for i in range(x,-1,-1):
        if Board[i][x-i] == tile:
          counter +=1
        else:
          counter = 0
          
        if counter == count:
          counts += 1

    else:
      for i in range(5,x-7,-1):
        if Board[i][x-i] == tile:
          counter +=1
        else:
          counter = 0
        if counter == count:
          counts += 1

        
    counter = 0
  return counts
def tileCounterSE(Board, tile, count): #Count 4 in a row Diagonal SE
  counter = 0
  counts = 0
  
  for x in range(12):
    if x<=5:
      for i in range(x,-1,-1):
        if Board[5-i][x-i] == tile:
          counter += 1
        else:
          counter = 0
        if counter == count:
          counts+=1
      
    else:
      for i in range(5,x-7,-1):
        if Board[5-i][x-i] == tile:
          counter += 1
        else:
          counter = 0
        if counter == count:
          counts+=1

    counter = 0      
      
  return counts

def tileCounter(Board, tile, count): #tileCounter counts the amount of tiles in a row given amount
  points = 0

  points += tileCounterX(Board, tile, count)
  points += tileCounterY(Board, tile, count)
  points += tileCounterNE(Board, tile, count)
  points += tileCounterSE(Board, tile, count)

  return points

def getVal(board, move, tile): #getValue does the move and returns value of the move 
  newBoard = copy.deepcopy(board)
  value = 0
  placeTile(newBoard, move, tile)
  
  if winningBoard(newBoard, tile):
    value+=1000000

  value += tileCounter(newBoard, tile, 2) * 2
  value += tileCounter(newBoard, tile, 3) * 6

  #if placed in the middle column
  if move == 3:
    value += 10


    
  return value

def isGameOver(board): #board states when game is over. for the minimax algortithm
  return winningBoard(board, AITile) or winningBoard(board, pTile) or len(getAllowedMoves(board)) == 0

def boardVal(board, tile): #function for only checking the value of the board (for minmax)
  value = 0
  if winningBoard(board, tile):
    value+=1000000
  value += tileCounter(board, tile, 2) * 3
  value += tileCounter(board, tile, 3) * 7
  for row in range(6):
    if board[row][4] == tile:
      value+=15
      break
   
  return value
def minimax(board, depth, alpha, beta, maximizingPlayer): #MinMax Algorithm
  validLocations = getAllowedMoves(board)
  gameOver = isGameOver(board)
  if depth == 0 or gameOver: 
    if gameOver:
      if winningBoard(board, AITile):
        return (None, 100000000)
      elif winningBoard(board, pTile):
        return (None, -100000000)
      else:
        return (None, 0)
    else:
      return (None, boardVal(board, AITile))

  if maximizingPlayer: #AIs turn (maximizing)
    val = -math.inf
    col = random.choice(validLocations)

    for i in validLocations:
      newBoard = copy.deepcopy(board)
      placeTile(newBoard, i, AITile)
      newVal = minimax(newBoard, depth-1, alpha, beta, False)[1]
      if newVal > val:
        val = newVal
        col = i
      alpha = max(alpha, val) #alpha beta pruning
      if alpha >= beta:
        break
    return col, val


  
  else:   #Players turn (minimizing)
    val = math.inf
    col = random.choice(validLocations)

    for i in validLocations:
      newBoard = copy.deepcopy(board)
      placeTile(newBoard, i, pTile)
      newVal = minimax(newBoard, depth-1, alpha, beta, True)[1]
      if newVal < val:
        val = newVal
        col = i
      beta = min(beta, val)
      if alpha >= beta:
        break
        
    return col, val

    
#Pygame methods
def drawBoard(board): #Draws the board in pygame
  for c in range(7):
    for r in range(6):
      pygame.draw.rect(screen, blue, (c*squaresize, r*squaresize+squaresize, squaresize, squaresize))
      pygame.draw.circle(screen, black, (int(c*squaresize+squaresize/2), int(r*squaresize+squaresize+squaresize/2)), radius)

  for c in range(7):
    for r in range(6):		
      if board[r][c] == 1:
        pygame.draw.circle(screen, red, (int(c*squaresize+squaresize/2), int(r*squaresize+squaresize+squaresize/2)), radius)
      elif board[r][c] == 2: 
        pygame.draw.circle(screen, yellow, (int(c*squaresize+squaresize/2), int(r*squaresize+squaresize+squaresize/2)), radius)
  pygame.display.update()


def getLeaderboard(): #this prints the content of the leaderboard.txt file
  boardfile = open('leaderboard.txt')
  boardlist = []
  print('\n\n')
  for line in boardfile.readlines():
    boardlist.append(line)
  for i in boardlist:
    print(i)

#Actual Game

currentBoard = mainBoard


squaresize = 100
width = 7 * squaresize
height =  (6+1) * squaresize
size = (width, height)
radius = int(squaresize/2 - 5)
myfont = pygame.font.SysFont('monospace', 75)

screen = pygame.display.set_mode(size)
drawBoard(currentBoard)
pygame.display.update()

gameMode = 'AI' #You can change this but I wanted this to only put you against the AI

if gameMode == "BOARD": #Shows scores of all players
  getLeaderboard()

elif gameMode == "P":
  #Setup Game
  pTile = 1
  p2Tile = 2
  turn = 1

  #Game Start
  game = True
  print('\n')
  printBoard(currentBoard)
  
  while game:
    #pygame setup
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

      if event.type == pygame.MOUSEMOTION:
        pygame.draw.rect(screen, black, (0,0, width, squaresize))
        xpos = event.pos[0]
        if turn == 1:
          pygame.draw.circle(screen, red, (xpos, int(squaresize/2)), radius)
        else: 
          pygame.draw.circle(screen, yellow, (xpos, int(squaresize/2)), radius)
      pygame.display.update()

      if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.draw.rect(screen, black, (0,0, width, squaresize))

        #Player 1
        if turn == 1:
          print("\n\nPlayer 1's turn.\n")
          
          
          xpos = event.pos[0]
          choice = int(math.floor(xpos/squaresize))
          printBoard(currentBoard)
            
          print('')
          if allowedMove(currentBoard, choice):
            placeTile(currentBoard, choice, pTile)
            turn +=1
          printBoard(currentBoard)
          drawBoard(currentBoard)
          
          #Checks if game over
          if winningBoard(currentBoard, pTile):
            # label = myfont.render("Player 1 wins!!", 1, red)
            # screen.blit(label, (10,10))
            print('')
            printBoard(currentBoard)
            pygame.time.wait(3000)
            print("\n\nGame Over. Player 1 Wins!!\n")
            printBoard(currentBoard)
            game = False
          elif len(getAllowedMoves(currentBoard)) == 0:
            print('')
            printBoard(currentBoard)
            pygame.time.wait(3000)
            print("\n\nGame Over. Board is Full & it's a TIE!!\n")
            printBoard(currentBoard)
            game = False

            
        # #Player 2
        elif turn == 2:
          print("\n\nPlayer 2's turn.\n")
          
          
          xpos = event.pos[0]
          choice = int(math.floor(xpos/squaresize))
          printBoard(currentBoard)
            
          print('')
          if allowedMove(currentBoard, choice):
            placeTile(currentBoard, choice, p2Tile)
            turn -=1
          printBoard(currentBoard)
          drawBoard(currentBoard)
          
          #Checks if game over
          if winningBoard(currentBoard, p2Tile):
            print('')
            printBoard(currentBoard)
            pygame.time.wait(10000)
            print("\n\nGame Over. Player 2 Wins!!\n")
            printBoard(currentBoard)
            game = False
          elif len(getAllowedMoves(currentBoard)) == 0:
            print('')
            printBoard(currentBoard)
            pygame.time.wait(10000)
            print("\n\nGame Over. Board is Full & it's a TIE!!\n")
            printBoard(currentBoard)
            game = False

    
    

elif gameMode == "AI":
  #Setup Game
  pTile = 1
  AITile = 2
  turn = 1

  #Game Start
  game = True
  start = time.time()
  print('\n')

  while game:
    #pygame setup
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.MOUSEMOTION:
        pygame.draw.rect(screen, black, (0,0, width, squaresize))
        xpos = event.pos[0]
        if turn == 1:
          pygame.draw.circle(screen, red, (xpos, int(squaresize/2)), radius)
        else: 
          pass
        #   pygame.draw.circle(screen, yellow, (xpos, int(squaresize/2)), radius)
      pygame.display.update()

      if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.draw.rect(screen, black, (0,0, width, squaresize))

        #Players turn 
        if turn == 1:
          print("\n\nPlayer 1's turn.\n")
          
          
          xpos = event.pos[0]
          choice = int(math.floor(xpos/squaresize))
          printBoard(currentBoard)

          a = random.randint(1,2)
          if a == 2:
            randfile = open('random.txt')
            listFile = []
            for line in randfile.readlines():
              listFile.append(line)
            print(random.choice(listFile))
            print('\n')
            
          print('')
          if allowedMove(currentBoard, choice):
            placeTile(currentBoard, choice, pTile)
            turn +=1
          printBoard(currentBoard)
          drawBoard(currentBoard)
          
          #Checks if game over
          if winningBoard(currentBoard, pTile):
            print('')
            printBoard(currentBoard)
            pygame.time.wait(10000)
            print("\n\nGame Over. Player 1 Wins!!\n")
            timetaken = round((time.time() - start), 2)
            print("It took you: " + str(timetaken) + "s to beat the AI.\n")
            saveScore = input("Would you like to save your name as a winner against the AI? [y/n] : ").upper()
            if saveScore == "Y":
              name = str(input("What's your name? "))
              scoreFile = open('leaderboard.txt', 'a')
              scoreFile.write('Name: '+name+',  Time taken: '+str(timetaken)+'s\n')
              getLeaderboard()
              
            game = False
          #Checks if board is full
          elif len(getAllowedMoves(currentBoard)) == 0:
            print('')
            printBoard(currentBoard)
            pygame.time.wait(10000)
            print("\n\nGame Over. Board is Full & it's a TIE!!\n")
            printBoard(currentBoard)
            game = False


    #AIs Turn
    if turn == 2 and game:
      print("\n\nAI's turn.\n")
      printBoard(currentBoard)
      #sleep(1)

      choice = 0
      # newVal = 0
      # val = 0
      choice, score = minimax(currentBoard, 7, -math.inf, math.inf, True)
      # for i in range(7):

        # val = getVal(currentBoard, i, AITile)
        # val += getVal(currentBoard, i, pTile) 

        # if val > newVal:
        #   newVal = val
        #   choice = i 
        # else:
        #   pass

      print("\n")
      print("AI chose column " + str(choice+1))
        
      placeTile(currentBoard, choice, AITile)
      drawBoard(currentBoard)

      #Checks if game over
      if winningBoard(currentBoard, AITile):
        print('')
        printBoard(currentBoard)
        pygame.time.wait(10000)
        print("\n\nGame Over. AI Wins!!\n")
        printBoard(currentBoard)
        game = False
      elif len(getAllowedMoves(currentBoard)) == 0:
        print('')
        printBoard(currentBoard)
        pygame.time.wait(10000)
        print("\n\nGame Over. Board is Full & it's a TIE!!\n")
        printBoard(currentBoard)
        game = False
  
      turn-=1

elif gameMode == "T":
  pass

else:
  print("Run program again and select an actual mode ")