from py2pddl import Domain, create_type
from py2pddl import predicate, action, goal, init


class GraphPlanDomain(Domain):
    Location = create_type("Location")
    Ant = create_type("Ant")

    @predicate(Location, Ant)
    def ant_at(self, l, a):
        """Complete the method signature and specify
        the respective types in the decorator"""
    
    @predicate(Location, Location)
    def next_to(self, l1, l2):

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
        (i, j) = list(self.graph.nodes)[-1]
        return [self.ant_at(self.locations[(i, j)], self.ants[1])]
