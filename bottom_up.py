import parser
import time
import collections
import gc


def solver(graph, grammar, start, end, sizeGrammar, sizeGraph):
    gc.enable()
    matrix = [[[] for _ in range(sizeGrammar * sizeGraph)] for _ in range(sizeGrammar * sizeGraph)]
    run = True
    idx = 0
    while run:
        print("iteration #" + str(idx))
        idx += 1
        run = False
        for graph_edge in graph:
            for grammar_edge in grammar:
                if grammar_edge.s == graph_edge.s:
                    p_from_grammar = int(grammar_edge.begin)
                    p_to_grammar = int(grammar_edge.end)
                    p_from_graph = int(graph_edge.begin)
                    p_to_graph = int(graph_edge.end)
                    p_from = p_from_grammar * sizeGraph + p_from_graph
                    p_to = p_to_grammar * sizeGraph + p_to_graph
                    if grammar_edge.s not in matrix[p_from][p_to]:
                        matrix[p_from][p_to].append(graph_edge.s)
        print("matrix has been updated")
        for nonterminal in start:
            print("new edges with nonterminal:" + str(nonterminal))
            for node in start[nonterminal]:
                for i in range(sizeGraph):
                    history = set()
                    queue = collections.deque()
                    p_from = int(node) * sizeGraph + i
                    queue.append(p_from)
                    history.add(p_from)
                    while len(queue) > 0:
                        temp = queue.popleft()
                        if nonterminal in end[temp // sizeGraph]:
                            p_to = temp
                            new_edge = parser.Edge(p_from % sizeGraph, p_to % sizeGraph, nonterminal)
                            if new_edge not in graph:
                                graph.append(new_edge)
                                run = True
                        for j in range(sizeGraph * sizeGrammar):
                            if j not in history:
                                for char in matrix[temp][j]:
                                        queue.append(j)
                                        history.add(j)
					break
    return graph


def calc_result(nonterminal, graph):
    ans = 0
    for edge in graph:
        if edge.s == nonterminal:
            ans += 1
    return ans

def run(grammar_path, graph_path, nonterminal):
    graph_grammar, start, end, size_grammar = parser.parse_grammar(grammar_path)
    graph, size = parser.parse_graph(graph_path)
    matrix = solver(graph, graph_grammar, start, end, size_grammar, size_graph)
    print("done")


def run_tests():
    path_graph = "data/graphs/"
    name_graphs = ["skos.dot", "generations.dot", "travel.dot", "univ-bench.dot", "atom-primitive.dot",
             "biomedical-mesure-primitive.dot", "foaf.dot", "people_pets.dot", "funding.dot", "wine.dot", "pizza.dot"]
    path_grammar = "data/grammars/"
    name_grammars = ["Q1_automata.txt", "Q2_automata.txt"]
    for name_grammar in name_grammars:
        for name_graph in name_graphs:
            graph_grammar, start, end, size_grammar = parser.parse_grammar(path_grammar + name_grammar)
            graph, size_graph = parser.parse_graph(path_graph + name_graph)
            ans = solver(graph, graph_grammar, start, end, size_grammar, size_graph)
            print("\r" + name_grammar + " " + name_graph + ": " + str(calc_result("S", ans)))
