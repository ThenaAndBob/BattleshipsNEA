import pygame as pg

# Initialise menu
pg.init()
WIDTH = 400
HEIGHT = 400
screen = pg.display.set_mode((WIDTH, HEIGHT))
running = True

# Buttons
buttonimages = [pg.image.load("images.png")] # .convert() ?
rects = [buttonimages[0].get_rect()]
rects[0].center = screen.get_rect().center
blockSize = 40
blocks = []

while running:
    for x in range(0, WIDTH, blockSize):
        for y in range(0, HEIGHT, blockSize):
            blocks.append(pg.Rect(x, y, blockSize, blockSize))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                #check collision
                pass

    for block in blocks:
        pg.draw.rect(screen, (200,200,200), block, 1)

    pg.display.update()


    # for x in range(len(rects)):
    #     screen.blit(buttonimages[x], rects[x])

pg.QUIT