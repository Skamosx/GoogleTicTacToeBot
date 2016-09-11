# Imports
import math
import time
from selenium import webdriver

driver = webdriver.Chrome('chromedriver/chromedriver.exe')
driver.get('https://www.google.de/xhtml')
search_box = driver.find_element_by_name('q')
#send tic-tac-toe to the Gooogle Search Bar
search_box.send_keys('tic-tac-toe')
search_box.submit()
time.sleep(2)
googleboard = []


board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
seed = 1
oppSeed = -1

def getValidMoves():
    nm = []

    for index, element in enumerate(board):
        if element == 0:
            nm.append(index)
    return nm

def evaluateLine(idx1, idx2, idx3):
    s = 0

    if board[idx1] == seed:
        s = 1
    elif board[idx1] == oppSeed:
        s = -1

    if board[idx2] == seed:
        if s == 1:
            s = 10
        elif s == -1:
            return 0
        else:
            s = 1
    elif board[idx2] == oppSeed:
        if s == -1:
            s = -10
        elif s == 1:
            return 0
        else:
            s = -1

    if board[idx3] == seed:
        if s > 0:
            s *= 10
        elif s < 0:
            return 0
        else:
            s = 1
    elif board[idx3] == oppSeed:
        if s < 0:
            s *= 10
        elif s > 0:
            return 0
        else:
            s = -1

    return s

def evaluate():
    s = 0

    s += evaluateLine(0, 1, 2)
    s += evaluateLine(3, 4, 5)
    s += evaluateLine(6, 7, 8)
    s += evaluateLine(0, 3, 6)
    s += evaluateLine(1, 4, 7)
    s += evaluateLine(2, 5, 8)
    s += evaluateLine(0, 4, 8)
    s += evaluateLine(2, 4, 6)

    return s

def minimax(depth, player):
    nextMoves = getValidMoves()

    best = -math.exp(100) if player == seed else math.exp(100)
    current = 0
    bestidx = -1

    if (len(nextMoves) == 0) or depth == 0:
        best = evaluate()
    else:
        for index, element in enumerate(nextMoves):
            m = nextMoves[index]
            board[m] = player

            if player == seed:
                current = minimax(depth - 1, oppSeed)[0]
                if current > best:
                    best = current
                    bestidx = m
            else:
                current = minimax(depth - 1, seed)[0]
                if current < best:
                    best = current
                    bestidx = m

            board[m] = 0

    return [best, bestidx]


table = driver.find_element_by_class_name('_i7i')
rows = table.find_elements_by_tag_name('tr')
if len(rows) == 3:
    for index, element in enumerate(rows):
        columns = element.find_elements_by_tag_name('td')
        if len(columns) == 3:
            for i, elm in enumerate(columns):
                googleboard.append(elm)
        else:
            print('Tic-Tac-Toe Feld konnte nicht gefunden werden.')
else:
    print('Tic-Tac-Toe Feld konnte nicht gefunden werden.')

for num in range(0, 8):
    move = minimax(2, seed)[1]
    board[move] = seed
    googleboard[move].click()
    # wait for Google
    time.sleep(5)
    for index, element in enumerate(googleboard):
        if (board[index] != 1) and (board[index] != -1):
                svgs = element.find_elements_by_tag_name('svg')
                display = svgs[1].value_of_css_property('display')
                if display == 'block':
                    board[index] = -1
