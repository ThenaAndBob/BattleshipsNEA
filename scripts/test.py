data = """R 3
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
currentX = 0 
currentY = 0
taken = set()
directionDict = {
    "U": [0, 1],
    "D": [0, -1],
    "R": [1,0],
    "L": [-1, 0]
}
direction = ""
for line in data.splitlines():
    print(currentX, currentY)
    prevDirection = direction
    direction = line.split(" ")[0]
    amount = int(line.split(" ")[1])
    if (prevDirection == "U" or prevDirection == "D") and (direction == "L" or direction == "R"):
        amount -= 2
        currentX += directionDict[direction][0]
        currentY += directionDict[prevDirection][1]
    elif (prevDirection == "L" or prevDirection == "R") and (direction == "U" or direction == "D"):
        amount -= 2
        currentX += directionDict[prevDirection][0]
        currentY += directionDict[direction][1]

    for _ in range(amount):
        taken.add((currentX, currentY))
        currentX += directionDict[direction][0]
        currentY += directionDict[direction][1]

print(len(taken))
