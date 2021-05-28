import json
import pygame as pg
import time

def inputData():
    op=0
    while op not in (1, 2):
        print("CHe operazione vuoi svolgere?")
        print("1 --> crea una nuova stanza\n2 --> modifica una stanza")
        op=int(input(">>> "))
        if op==1:
            print("\nInserire le misure della stanza (in metri)")
            x = float(input("X: "))
            y = float(input("Y: "))
            file = open("maze.json", "r")
            data = json.load(file)
            file.close()

            data["width"]=x
            data["height"]=y
            file = open("maze.json", "w")
            json.dump(data, file)
            file.close()

            return (x, y, None)
        elif op==2:
            file = open("maze.json", "r")
            data = json.load(file)
            maze = data["maze"]
            x=data["width"]
            y=data["height"]
            file.close()
            return (x, y, maze)

def mazeSetup(x, y):
    maze = []
    for i in range(y + 2):
        maze += [[]]
        for c in range(x + 2):
            if i == 0 or i == y + 1:
                maze[i].append(1)
            elif c == 0 or c == x + 1:
                maze[i].append(1)
            else:
                maze[i].append(0)
    return maze

def printInfo():
    print("\nINFORMAZIONI\nLa scala adottata e' di 25 cm\nQ --> esci dal programma e salva le modifiche\nD --> disegna\nE --> cancella\nM --> muoviti\nBACKSPACE + E --> cancella tutto\n1 --> imposta il punto di partenza\n2 --> imposta il punto di arrivo")

def getData():
    file = open("maze.json", "r")
    data = json.load(file)
    file.close()
    return data

def drawMaze():
    inData = inputData()
    fileData=getData()
    width = int(inData[0] * 4)
    height = int(inData[1] * 4)

    if inData[2]==None:
        maze=mazeSetup(width, height)
        start, end1 = [], []
    else:
        maze=inData[2]
        start, end1 = fileData["start"], fileData["end"]

    mx=max(height, width)
    squareSize=int(800/mx)

    pg.init()
    screen = pg.display.set_mode((width * squareSize, height * squareSize))
    printInfo()

    currentX, currentY = 0, 0
    draw, end, erase, move = False, False, False, True

    while not end:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                end = True

        if pg.mouse.get_pressed():
            px, py = pg.mouse.get_pos()
            currentX=px//squareSize
            currentY=py//squareSize

        key = pg.key.get_pressed()


        if key[pg.K_BACKSPACE] and key[pg.K_e]:
            maze=mazeSetup(width, height)
        elif key[pg.K_d]:
            draw = True
            erase=False
            move=False
        elif key[pg.K_m]:
            draw = False
            erase=False
            move=True
        elif key[pg.K_e]:
            draw = False
            erase=True
            move=False
        elif key[pg.K_1]:
            if start != []:
                maze[start[1]][start[0]] = 0
            start=[currentX+1, currentY+1]
            maze[currentY+1][currentX+1] = "O"
        elif key[pg.K_2]:
            if end1 != []:
                maze[end1[1]][end1[0]] = 0
            end1=[currentX+1, currentY+1]
            maze[currentY+1][currentX+1] = "X"
        elif key[pg.K_q]:
            end=True

        if draw == True and maze[currentY+1][currentX+1] not in ("O", "X"):
            maze[currentY+1][currentX+1] = 1
        elif erase==True and maze[currentY+1][currentX+1] not in ("O", "X"):
            maze[currentY+1][currentX+1] = 0

        screen.fill((255, 255, 255))
        for i in range(height):
            for c in range(width):
                if maze[i+1][c+1]==1:
                    pg.draw.rect(screen, (0, 0, 255), (c * squareSize, i * squareSize, squareSize, squareSize))
                elif maze[i+1][c+1]=="O":
                    pg.draw.rect(screen, (255, 255, 0), (c * squareSize, i * squareSize, squareSize, squareSize))
                elif maze[i+1][c+1]=="X":
                    pg.draw.rect(screen, (0, 255, 255), (c * squareSize, i * squareSize, squareSize, squareSize))
                
                if i==currentY and c==currentX and move:
                    pg.draw.circle(screen, (0, 255, 0), (currentX*squareSize+squareSize//2, currentY*squareSize+squareSize//2), squareSize//3)
                elif i == currentY and c == currentX and erase:
                    pg.draw.circle(screen, (255, 0, 0), (currentX * squareSize + squareSize // 2, currentY * squareSize + squareSize // 2), squareSize // 3)
                pg.draw.line(screen, (0, 0, 0), (0, i * squareSize), (width * squareSize, i * squareSize))
                pg.draw.line(screen, (0, 0, 0), (c * squareSize, 0), (c * squareSize, height * squareSize))
        pg.display.update()

    return (inData[0], inData[1], maze, start, end1)

def mainDraw():
    drawData=drawMaze()
    facing=input("In che direzione e' rivolto il robot?\nD --> in basso\nU --> in alto\nR --> a destra\nL --> a sinistra\n>>> ")
    file = open("maze.json", "r")
    data = json.load(file)
    file.close()
    maze=drawData[2]
    for i in range(len(maze)):
        for c in range(len(maze[i])):
            if maze[i][c] in ("X", "O"):
                maze[i][c]=0

    data["width"]=drawData[0]
    data["height"]=drawData[1]
    data["maze"]=maze
    data["start"]=drawData[3]
    data["end"]=drawData[4]
    data["facing"]=facing

    file = open("maze.json", "w")
    json.dump(data, file)
    file.close()
