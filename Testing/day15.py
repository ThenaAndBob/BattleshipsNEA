data = """Sensor at x=2483411, y=3902983: closest beacon is at x=2289579, y=3633785
Sensor at x=3429446, y=303715: closest beacon is at x=2876111, y=-261280
Sensor at x=666423, y=3063763: closest beacon is at x=2264411, y=2779977
Sensor at x=3021606, y=145606: closest beacon is at x=2876111, y=-261280
Sensor at x=2707326, y=2596893: closest beacon is at x=2264411, y=2779977
Sensor at x=3103704, y=1560342: closest beacon is at x=2551409, y=2000000
Sensor at x=3497040, y=3018067: closest beacon is at x=3565168, y=2949938
Sensor at x=1708530, y=855013: closest beacon is at x=2551409, y=2000000
Sensor at x=3107437, y=3263465: closest beacon is at x=3404814, y=3120160
Sensor at x=2155249, y=2476196: closest beacon is at x=2264411, y=2779977
Sensor at x=3447897, y=3070850: closest beacon is at x=3404814, y=3120160
Sensor at x=2643048, y=3390796: closest beacon is at x=2289579, y=3633785
Sensor at x=3533132, y=3679388: closest beacon is at x=3404814, y=3120160
Sensor at x=3683790, y=3017900: closest beacon is at x=3565168, y=2949938
Sensor at x=1943208, y=3830506: closest beacon is at x=2289579, y=3633785
Sensor at x=3940100, y=3979653: closest beacon is at x=2846628, y=4143786
Sensor at x=3789719, y=1225738: closest beacon is at x=4072555, y=1179859
Sensor at x=3939775, y=578381: closest beacon is at x=4072555, y=1179859
Sensor at x=3880152, y=3327397: closest beacon is at x=3404814, y=3120160
Sensor at x=3280639, y=2446475: closest beacon is at x=3565168, y=2949938
Sensor at x=2348869, y=2240374: closest beacon is at x=2551409, y=2000000
Sensor at x=3727441, y=2797456: closest beacon is at x=3565168, y=2949938
Sensor at x=3973153, y=2034945: closest beacon is at x=4072555, y=1179859
Sensor at x=38670, y=785556: closest beacon is at x=311084, y=-402911
Sensor at x=3181909, y=2862960: closest beacon is at x=3565168, y=2949938
Sensor at x=3099490, y=3946226: closest beacon is at x=2846628, y=4143786""".splitlines()

#4880737 is too low

considerRow = 2000000
fin = set()
doesContain = set()
sensorSet = set()

for sensor in data:
    a = sensor.split(": closest beacon is at ")
    a[0] = a[0].strip("Sensor at ")
    sensorCoords = a[0].split(", ")
    sensorX = int(sensorCoords[0].split("=")[1])
    sensorY = int(sensorCoords[1].split("=")[1])

    beaconCoords = a[1].split(", ")
    beaconX = int(beaconCoords [0].split("=")[1])
    beaconY = int(beaconCoords[1].split("=")[1])
    sensorSet.add((sensorX, sensorY))

    if beaconY == considerRow:
        doesContain.add(beaconX)

    distance = abs(beaconX-sensorX) + abs(beaconY - sensorY)
    numImpossibleSquares = 2*(distance - abs(sensorY-considerRow)) + 1
    if numImpossibleSquares > 0:
        startX = sensorX - (numImpossibleSquares - 1)//2
        for deltaX in range(numImpossibleSquares):
            if startX+deltaX not in doesContain:
                fin.add(startX+deltaX)
print(fin)
print(len(fin))
print(sensorSet)


part2
"""data = Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3.splitlines()

fin = []
for sensor in data:
    a = sensor.split(": closest beacon is at ")
    a[0] = a[0].strip("Sensor at ")
    sensorCoords = a[0].split(", ")
    sensorX = int(sensorCoords[0].split("=")[1])
    sensorY = int(sensorCoords[1].split("=")[1])

    beaconCoords = a[1].split(", ")
    beaconX = int(beaconCoords [0].split("=")[1])
    beaconY = int(beaconCoords[1].split("=")[1])

    distance = abs(beaconX-sensorX) + abs(beaconY - sensorY)
    fin.append([sensorX, sensorY, distance])


bounds = [[] for _ in range(len(fin))]
for index, sensor in enumerate(fin):
    x,y,d = sensor
    bounds[0].append(f"-x+{y-d+x-1}") # top left
    bounds[1].append(f"-x+{y+d+x+1}") # bottom right
    bounds[2].append(f"x+{y-d-x-1}") # top right
    bounds[3].append(f"x+{y+d-x+1}") # bottom left

for b1 in bounds[0]:
    if b1 in bounds[1]:
        print(b1)

for b3 in bounds[2]:
    if b3 in bounds[3]:
        print(b3)
"""
