data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""".splitlines()

from pprint import pprint

def move(currentMinute, currentValve, opened, values, releasedPressure, graph):
    if currentMinute > 30:
        values.append(releasedPressure)
    elif currentValve not in opened:
        opened.append(currentValve)
        currentMinute += 1
        move(currentMinute, currentValve, opened, values, releasedPressure, graph)
    else:
        for valve in graph[currentValve]:
            if valve not in opened:
                currentValve = valve
                currentMinute += 1
                move(currentMinute, currentValve, opened, values, releasedPressure, graph)
            

graph = {}

for line in data:
    line = line.split(" ")
    valveName = line[1]
    flowRate = line[4].strip("rate=")[:-1]
    destValves = line[9:]
    for valve in destValves:
        valve = valve.strip(",")
    graph[valveName] = [flowRate, destValves]

move(1, "AA", [], [], 0, graph)
    


