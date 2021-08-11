from py2pddl import Domain, create_type
from py2pddl import predicate, action, goal, init
import networkx as nx

import os
import shutil
import os.path as path
import re
import numpy as np
import cv2

def img_to_networkx(img_path):
    img = np.flip(np.squeeze(cv2.imread(img_path)), axis=0)
    graph_size = img.shape[0]
    graph = nx.grid_graph([graph_size] * 2)
    black = [0, 0, 0]

    for i in range(graph_size):
        for j in range(graph_size):
            if not 'x' in graph.nodes[(i, j)]:
                graph.nodes[(i, j)].update({'x' : [i, j]})

            if all(img[i, j] == black):
                graph.remove_node((i, j))


    for x, y in graph.nodes():
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 or j == 0:
                    continue
                diagonal_x = x + i
                diagonal_y = y + j

                if graph.has_node((diagonal_x, diagonal_y)):
                    graph.add_edge((diagonal_x, diagonal_y), (x, y))
                    graph.add_edge((x, y), (diagonal_x, diagonal_y))

    return graph


class GraphPlanDomain(Domain):
    Location = create_type("Location")
    Ant = create_type("Ant")

    @predicate(Location, Ant)
    def ant_at(self, l, a):
        """Complete the method signature and specify
        the respective types in the decorator"""
    
    @predicate(Location, Location)
    def next_to(self, l1, l2):
        """Compleete the method signature and specify""" 
    @action(Ant, Location, Location)
    def move_to(self, a, l1, l2):
        precond: list = [self.ant_at(l1, a), self.next_to(l1, l2)]
        effect: list = [~self.ant_at(l1, a), self.ant_at(l2, a)]
        return precond, effect


class GraphPlanProblem(GraphPlanDomain):
    def __init__(self, graph : nx.graph):
        super().__init__()
        self.ants = GraphPlanDomain.Ant.create_objs([1], prefix="p")
   
        location_list = [(i, j) for i, j in graph.nodes()]
        self.locations = GraphPlanDomain.Location.create_objs(location_list)
        self.g = graph

    @init
    def init(self) -> list:
        # To fill in
        # Return type is a list
        start_cond = []
        for ((i, j), (k, l)) in self.g.edges:
            start_cond.append(self.next_to(self.locations[(i, j)], self.locations[(k, l)]))

        start_cond.append(self.ant_at(self.locations[(0, 0)], self.ants[1]))

        return start_cond

    @goal
    def goal(self) -> list:
        # To fill in
        # Return type is a list
        (i, j) = list(self.g.nodes)[-1]
        return [self.ant_at(self.locations[(i, j)], self.ants[1])]

def load_data(folder : str):
        paths = [path.join(folder, f) for f in os.listdir(folder) if f.endswith('.png')]
        def numericalSort(value):
            numbers = re.compile(r'(\d+)')
            parts = numbers.split(value)
            parts[1::2] = map(int, parts[1::2])
            return parts
        return sorted(paths, key=numericalSort)

def convert_data_to_pdll(path : str):
    paths = load_data(path)
    target_loc = './converted/'
    for i, img_path in enumerate(paths):
        print("Starting to convert:", img_path)

        g = img_to_networkx(img_path)
        p = GraphPlanProblem(g)
        p.generate_domain_pddl()
        p.generate_problem_pddl()
        
        shutil.move("./domain.pddl", target_loc + f"domain_{i}.pddl")
        shutil.move("problem.pddl", target_loc + f"problem_{i}.pddl")

location = "/home/michalpandy/dev/nx_to_pddl/motion_planning_datasets/alternating_gaps/test"
convert_data_to_pdll(location)
