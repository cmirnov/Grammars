import parser


class GrammarRule:
    def __init__(self, list):
        self.rule = []
        for s in list:
            if s != " " and s != ":":
                self.rule.append(s)


def parse_grammar(filename):
    grammar = []
    with open(filename) as f:
        for line in f:
            line = line.rstrip('\n')
            if len(line) > 0:
                grammar.append(GrammarRule(line.split(' ')))
    return grammar


def solver(grammar, graph, size):
    matrix = [[[] for j in range(size)] for i in range(size)]
    for rule in grammar:
        if len(rule.rule) == 2:
            for edge in graph:
                if edge.s == rule.rule[1] and rule.rule[0] not in matrix[int(edge.begin)][int(edge.end)]:
                    matrix[int(edge.begin)][int(edge.end)].append(rule.rule[0])
    run = True
    while run:
        run = False
        for k in range(size):
            for u in range(size):
                if len(matrix[u][k]) > 0:
                    for v in range(size):
                        if len(matrix[k][v]) > 0:
                            for elem1 in matrix[u][k]:
                                for elem2 in matrix[k][v]:
                                        for rule in grammar:
                                            if len(rule.rule) == 3 and rule.rule[1] == elem1 and rule.rule[2] == elem2:
                                                if rule.rule[0] not in matrix[u][v]:
                                                    run = True
                                                    matrix[u][v].append(rule.rule[0])
    return matrix

def calc_result(matrix, size):
    ans = 0
    for i in range(size):
        for j in range(size):
            if "S" in matrix[i][j]:
                ans += 1
    return ans


def run(grammar_path, graph_path):
    grammar = parse_grammar(grammar_path)
    graph, size = parser.parse_graph(graph_path)
    matrix = solver(grammar, graph, size)

def run_tests():
    path_graph = "data/graphs/"
    name_graphs = ["skos.dot", "generations.dot", "travel.dot", "univ-bench.dot", "atom-primitive.dot",
             "biomedical-mesure-primitive.dot", "foaf.dot", "people_pets.dot", "funding.dot", "wine.dot", "pizza.dot"]
    path_grammar = "data/grammars/"
    name_grammars = ["Q1_hom.txt", "Q2_hom.txt"]
    for name_grammar in name_grammars:
        for name_graph in name_graphs:
            grammar = parse_grammar(path_grammar + name_grammar)
            graph, size = parser.parse_graph(path_graph + name_graph)
            matrix = solver(grammar, graph, size)
            print(name_grammar + " " + name_graph + ": " + str(calc_result(matrix, size)))


