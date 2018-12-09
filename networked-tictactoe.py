# Networked Tic-Tac-Toe

import socket, threading, struct

def send_one_message(sock, data):
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)
    
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
    
def recv_one_message(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def drawBoard(board):
    # This function prints out the board that it was passed.

    # "board" is a list of 10 strings representing the board (ignore index 0).
    print(board[7] + '|' + board[8] + '|' + board[9])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[1] + '|' + board[2] + '|' + board[3])

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use "bo" instead of "board" and "le" instead of "letter" so we don't have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # Across the top
    (bo[4] == le and bo[5] == le and bo[6] == le) or # Across the middle
    (bo[1] == le and bo[2] == le and bo[3] == le) or # Across the bottom
    (bo[7] == le and bo[4] == le and bo[1] == le) or # Down the left side
    (bo[8] == le and bo[5] == le and bo[2] == le) or # Down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # Down the right side
    (bo[7] == le and bo[5] == le and bo[3] == le) or # Diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # Diagonal

def isSpaceFree(board, move):
    # Return True if the passed move is free on the passed board.
    return board[move] == ' '

def getPlayerMove(board):
    # Let the player enter their move.
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)

def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise, return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


print('Welcome to Tic-Tac-Toe!')

host = input('Server address:')
port = 5023
username = input('Username:')
password = input('Password:')
otherplayer = input('Who do you want to play with? ')
startchoice = input("'start' a game or 'join' a game?")
# the person who starts is always X
if startchoice == 'start':
    playerLetter, computerLetter = ['X', 'O']
    turn = 'you'
else:
    playerLetter, computerLetter = ['O', 'X']
    turn = 'other'
theBoard = [' '] * 10
gameIsPlaying = True
      
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((bytes(host, 'utf-8'), port))     
print('Connected to remote host...')
send_one_message(client_sock, bytes(username, 'utf-8'))
send_one_message(client_sock, bytes(password, 'utf-8'))
send_one_message(client_sock, bytes('SYS:REG:'+otherplayer+':TICTACTOE', 'utf-8'))

input("Press ENTER to begin")

while gameIsPlaying:
  if turn == 'you':
      # Player's turn
      drawBoard(theBoard)
      move = getPlayerMove(theBoard)
      makeMove(theBoard, playerLetter, move)
      send_one_message(client_sock, bytes(otherplayer+":TICTACTOE:"+str(move), 'utf-8'))

      if isWinner(theBoard, playerLetter):
          drawBoard(theBoard)
          print('Hooray! You have won the game!')
          gameIsPlaying = False
      else:
          if isBoardFull(theBoard):
              drawBoard(theBoard)
              print('The game is a tie!')
              break
          else:
              turn = 'other'

  else:
      drawBoard(theBoard)
      print("Waiting for",otherplayer,"to move...")
      msg = recv_one_message(client_sock).decode("utf-8").split(':')
      print(msg)
      move = int(msg[3])
      print(otherplayer,"chose",move)
      makeMove(theBoard, computerLetter, move)

      if isWinner(theBoard, computerLetter):
          drawBoard(theBoard)
          print(otherplayer,'has beaten you! You lose.')
          gameIsPlaying = False
      else:
          if isBoardFull(theBoard):
              drawBoard(theBoard)
              print('The game is a tie!')
              break
          else:
              turn = 'you'

input('Press ENTER to exit')
