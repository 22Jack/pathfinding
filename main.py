import drawMaze
import pathfinding

if __name__=="__main__":
    end=False
    while not end:
        data=drawMaze.getData()

        print("\n\nCHe operazioen vuoi svolgere?\n0 --> termina il programma\n1 --> modifica/crea una nuova stanza\n2 --> visualizza il percosro\n3 --> visualizza i dati della stanza")
        operation=int(input(">>> "))
        if operation==1:
            drawMaze.mainDraw()
            pathfinding.mainPathfinding()
        elif operation==2:
            pathfinding.printPath(data["path"])
        elif operation==3:
            print("Larghezza stanza:", data["width"], "metri")
            print("lunghezza stanza:", data["height"], "metri")
            print("Direzione robot:", data["facing"])
            print("Percorso:", data["path"])
            print("Percorso codificato:", data["encodedPath"])
        elif operation==0:
            end=True


