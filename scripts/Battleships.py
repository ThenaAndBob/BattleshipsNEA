from UI import GUI, Terminal
from sys import argv
import os

def usage():   
    print(f"""
Usage: python {argv[0]} [g | t]
g : play with the GUI
t : play with the Terminal""")


if __name__ == "__main__":
    try:
        if argv[1] == 'g':
            print("Starting GUI version")
            ui = GUI()
            ui.run()
        elif argv[1] == 't':
            print("Starting Terminal version")
            ui = Terminal()
            ui.run()
    except IndexError:
        try:
            print(os. getcwd())
            i = input("GUI or Terminal (g/t)")
            if i == "g":
                print("Starting GUI version")
                ui = GUI()
                ui.run()
            elif i == "t":
                print("Starting Terminal version")
                ui = Terminal()
                ui.run()
            else:
                usage()
        except Exception as e:
            print(e)
        


input()