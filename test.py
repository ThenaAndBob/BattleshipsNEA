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

#Grid
squareSize = 40
squares = []
for x in range(0, WIDTH, squareSize):
    for y in range(0, HEIGHT, squareSize):
        squares.append(pg.Rect(x, y, squareSize, squareSize))

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                point = pg.mouse.get_pos()
                for square in squares:
                    if square.collidepoint(point):
                        #attack that square.
                        pass
                pass
    for square in squares:
        pg.draw.rect(screen, (255,255,255), square, 1) # white colour
    # for x in range(len(rects)):
    #     screen.blit(buttonimages[x], rects[x])

    pg.display.update()

pg.QUIT