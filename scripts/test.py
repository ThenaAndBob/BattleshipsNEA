def bruteForce(board, ships, width, height)
    countBoard = [[] * width] * height
    for square in board:
        if square is not empty:
            add index(square) to taken
                
    while simululationsCounter > 0
        tempTaken = taken
        for shiplength in ships:
            x = random.RANDOM_INT(0, width-1) # inclusive
            y = random.RANDOM_INT(0, height-1)
            dir = random.RANDOM_INT(0,3)
            if isValid(x,y,dir,shiplength):
                for square covered by ship in countBoard:
                    square += 1
            
        simululationsCounter -= 1
    
    return index(max(countBoard))