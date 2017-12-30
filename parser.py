import re


class Edge:
    def __init__(self, u, v, s):
        self.begin = u
        self.end = v
        self.s = s

    def __eq__(self, other):
        return self.begin == other.begin and self.end == other.end and self.s == other.s
        
    def __hash__(self):
        return self.begin ^ self.end


def parse_graph(filename):
    graph = []
    with open(filename) as f:
        p = re.compile(r"(?P<lp>\d*) -> (?P<rp>\d*).*\"(?P<label>\d*)\".*")
        nodes = [next(f) for _ in range(3)][2]
        size = nodes.count(';')  # number of nodes
        for line in f:
            match = p.match(line)
            if match:
                graph.append(Edge(match.group('lp'), match.group('rp'), match.group('label')))
    return graph, size

def parse_grammar(filename):
    graph = []
    start = {}
    end = []
    with open(filename) as f:
        edge = re.compile(r"(?P<lp>\d*) -> (?P<rp>\d*).*\"(?P<label>[a-zA-Z0-9_]*)\".*")
        state = re.compile(r"(?P<node>\d*)\[label=\"(?P<label>[a-zA-Z0-9_]*)\".*")
        startState = re.compile(r".*color=\"green\".*")
        endState = re.compile(r".*shape=\"doublecircle\".*")
        nodes = [next(f) for _ in range(3)] [2]
        size = nodes.count(';')
        graph = []
        end = [[] for _ in range(size)]
        for line in f:
            matchEdge = edge.match(line)
            if matchEdge:
                graph.append(Edge(matchEdge.group('lp'), matchEdge.group('rp'), matchEdge.group('label')))
            matchState = state.match(line)
            if matchState:
                matchStart = startState.match(line)
                matchEnd = endState.match(line)
                if matchStart:
                    if not start.get(matchState.group('label')):
                        start[matchState.group('label')] = []
                    start[matchState.group('label')].append(int(matchState.group('node')))
                if matchEnd:
                    end[int(matchState.group('node'))].append(matchState.group('label'))
    return graph, start, end, size

