from UI import GUI, Terminal
from sys import argv

def usage():   
    print(f"""
Usage: python {argv[0]} [g | t]
g : play with the GUI
t : play with the Terminal""")
    quit()


if __name__ == "__main__":
    if argv[1] == 'g':
        print("Starting GUI version")
        ui = GUI()
        ui.run()
    elif argv[1] == 't':
        print("Starting Terminal version")
        ui = Terminal()
        ui.run()
    else:
        print("Run using t or g option")
        usage()
