from problem import QAPProblem
import random
import math
from typing import List

# Standardowe instancje testowe pochodzą z biblioteki QAPLIB.
# Pierwotne źródło: https://qaplib.mgi.polymtl.ca/
# Alternatywny adres: https://coral.ise.lehigh.edu/data-sets/qaplib/
# Instancje mine1, mine2 i mine3 wygenerowano na potrzeby projektu.

def generate_start_flow(size:int, min_flow: int, max_flow: int, percent_0_flow: float):
    return [
        [0 if i == j or random.random() < percent_0_flow 
         else random.randint(min_flow, max_flow)
          for j in range(size)]
        for i in range(size)
    ]

def generate_claster_flow(size:int, min_flow: int, max_flow: int, min_claster_flow: int,
                             max_claster_flow: int, percent_0_flow: float):
    
    side = int(math.sqrt(size))

    clasters = [
        list(range(i * side, (i + 1) * side))
        for i in range(side)
    ] 
    clasters.append(list(range(side**2, size)))

    flow = generate_start_flow(size, min_flow, max_flow, percent_0_flow) 
    for claster in clasters:
        for j in claster:
            for i in claster:
                if i == j or random.random() < percent_0_flow :
                    continue
                else:
                    flow[i][j] = random.randint(min_claster_flow, max_claster_flow )
    return flow

def generate_not_balans_flow(size:int, min_flow: int, max_flow: int, percent_0_flow: float,
                             percent_big_flow: float, number_great_flow: int, ):
    flow = []
    

    for i in range(size):
        row = []
        for j in range(size):
            if i == j or random.random() < percent_0_flow :
                 row.append(0)
            elif random.random() < percent_big_flow :
                 row.append(random.randint(min_flow*10, max_flow*10 ))
            else:
                 row.append( random.randint(min_flow, max_flow ) )
    
        flow.append(row)

    great_flows_points = set()

    while len(great_flows_points) < number_great_flow:
        point = (random.randrange(size), random.randrange(size) )
        if point[0] != point[1]:
            great_flows_points.add(
                (random.randrange(size), random.randrange(size))
            )

    for i, j in great_flows_points:
        if i != j:
            flow[i][j] = random.randint(
                20 * max_flow,
                50 * max_flow
            )

    return flow


def generate_euclidean_distance(size, coord_range):
               
    # Losowe współrzędne punktów (x, y).
    points = set()
    while(len(points) < size):
        points.add( (random.uniform(0, coord_range), random.uniform(0, coord_range) ) )
    
    points = list(points)

    distance = []
    max_distance = 0
    for point1 in points:
        row = []
        for point2 in points:
            row.append(1+int( math.dist(point1, point2)) )
        distance.append(row)
        max_distance = max(max_distance, max(row))

    return distance
 

def load_problem_from_file(fileName: str) ->  QAPProblem:
    fileName = "qaplib/in/" + fileName.strip() + (".txt" if '.' not in fileName else "" )
    with open(fileName) as file:
        size = int( file.readline().strip() )
        flows = []
        while(line := file.readline()):
            if(len(flows) >= size):
                break
            if(not line.strip()):
                continue

            flows.append([ int(flow) for flow in line.split() ])

        distances = []
        while(line := file.readline()):
            if(not line.strip()):
                continue
            distances.append([ int(distance) for distance in line.split() ])

    if(len(distances) != size or size != len(flows)):
        raise ValueError(f"worng size, expected {size} got: distances{len(distances)},  flows {len(flows)} ")
    

    if any(len(row) != size for row in flows):
        raise ValueError("Flow matrix is not square")

    if any(len(row) != size for row in distances):
        raise ValueError("Distance matrix is not square")
    
    return QAPProblem(flow=flows, distance=distances)

def create_and_save_problem(
    file_name: str,
    flow: List[List[int]],
    distance: List[List[int]],
    size: int,
):

    problem = QAPProblem(flow, distance)


    path = f"qaplib/in/{file_name}.txt"

    with open(path, "w") as file:
        file.write(f"{size}\n")
        file.write("\n")

        for row in problem.flow:
            file.write(" ".join(map(str, row)))
            file.write("\n")

        file.write("\n")

        for row in problem.distance:
            file.write(" ".join(map(str, row)))
            file.write("\n")

    print(f"Zapisano: {path}")
if __name__ == "__main__":

    # Instancja z przepływami w zakresie 5–10 i losowymi przepływami zerowymi.
    size = 25
    distance = generate_euclidean_distance(size, coord_range=100)
    flow = generate_start_flow(size, 5, 10, 0.1)
    problem = create_and_save_problem( "mine1", flow, distance, size)

    # Instancja z podwyższonymi przepływami i kilkoma dużymi wartościami.
    size = 25
    distance = generate_euclidean_distance(size, coord_range=100)
    flow = generate_not_balans_flow(size, 5, 10, 0.1, 0.1, 4)
    problem = create_and_save_problem( "mine2", flow, distance, size)

    # Instancja klastrowa: duże przepływy wewnątrz klastrów, małe między nimi.
    size = 25
    distance = generate_euclidean_distance(size, coord_range=100)
    flow = generate_claster_flow(size, 0, 2, 10, 50, 0.2)
    problem = create_and_save_problem( "mine3", flow, distance, size)


