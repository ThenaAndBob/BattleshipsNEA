from UI import GUI, Terminal
from sys import argv

#python scripts\Battleships.py t
#python scripts\Battleships.py g

def usage():   
    print(f"""
Usage: {argv[0]} [g | t]
g : play with the GUI
t : play with the Terminal""")
    quit()


if __name__ == "__main__":
    if argv[1] == 'g':
        ui = GUI()
        ui.run()
    elif argv[1] == 't':
        ui = Terminal()
        ui.run()
    else:
        print("Run using t or g option")
        usage()