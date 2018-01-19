import parser
import sys
import answer

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

def check_small(matrix, idx, size):
    ans = 0
    for i in range(size):
        for j in range(size):
            for val in matrix[i][j]:
                if val == "S":
                    if [i, val, j] not in answer.small[idx]:
                        print("fail")
                        return
                    ans += 1
                   
    if ans != len(answer.small[idx]):
        print("fail")
        return
    print("passed")



def run(grammar_path, graph_path):
    grammar = parse_grammar(grammar_path)
    graph, size = parser.parse_graph(graph_path)
    matrix = solver(grammar, graph, size)
    for i in range(size):
        for j in range(size):
            print(matrix[i][j], end=" ")
        print()
    print(calc_result(matrix, size))
    
def run_all():
    run_big()
    run_small()

def run_big():
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

def run_small():
    path_graph = "data/small/"
    name_graphs = ["1/graph.txt", "2/graph.txt", "3/graph.txt", "4/graph.txt"]
    path_grammar = "data/small/"
    name_grammars = ["1/hom.txt", "2/hom.txt", "3/hom.txt", "4/hom.txt"]
    for i in range(4):
        grammar = parse_grammar(path_grammar + name_grammars[i])
        graph, size = parser.parse_graph(path_graph + name_graphs[i])
        matrix = solver(grammar, graph, size)
        print(name_grammars[i] + " " + name_graphs[i])
        if i < 3:
            check_small(matrix, i, size)
        else:
            num = calc_result(matrix, size)
            if num == 2652:
                print("passed")
            else:
                print("fail")

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("number of arguments < 3")
        sys.exit()

    grammar = parse_grammar(sys.argv[1])
    graph, size = parser.parse_graph(sys.argv[2])
    matrix = solver(grammar, graph, size)
    if len(sys.argv) == 3:
        for i in range(size):
            for j in range(size):
                print(matrix[i][j], end=" ")
            print() 
    else:
        with open(sys.argv[3],'w') as f:
            for i in range(size):
                for j in range(size):
                    f.write(' ' + str(matrix[i][j]))
                f.write('\n')


