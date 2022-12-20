import mouse
import keyboard
import pygame as pg
import time

def click():
    running = True
    time.sleep(1)
    print("started")
    while running:
        try:
            if keyboard.is_pressed("s"):
                running = False
        except:
            pass
        mouse.click()
    print("stopped")
    return

pg.init()

running = True
while running:
    try:
        if keyboard.is_pressed("s"):
            click()
            time.sleep(1)
    except:
        pass

