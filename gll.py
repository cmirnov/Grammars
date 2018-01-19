import parser
import time
import sys
import answer as an


class State:
    def __init__(self, grammar, graph, stack):
        self.grammarPointer = int(grammar)
        self.graphPointer = int(graph)
        self.stackPointer = int(stack)

    def __hash__(self):
        return self.stackPointer ^ self.graphPointer ^ self.grammarPointer

    def __eq__(self, other):
        return self.grammarPointer == other.grammarPointer and self.graphPointer == other.graphPointer and self.stackPointer == other.stackPointer


class StackState:
    def __init__(self, nonterminal, pointer):
        self.nonterminal = nonterminal
        self.pointer = pointer

    def __hash__(self):
        return self.pointer

    def __eq__(self, other):
        return self.nonterminal == other.nonterminal and self.pointer == other.pointer


class Ans:
    def __init__(self, p1, n, p2):
        self.p1 = p1
        self.p2 = p2
        self.n = n

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2 and self.n == other.n

    def __hash__(self):
        return self.p1 ^ self.p2

    def __str__(self):
        return str(self.p1) + " " + str(self.n) + " " +str(self.p2) 


animation = "|/-\\"


def GLL(graph, graphGrammar, start, end, firstNonTerminal, size):
    stack_state = []
    stack_edge = set()
    executed_stack_state = {}
    work_queue = []
    history = set()
    for node in start.get(firstNonTerminal):
        for i in range(size):
            work_queue.append(State(int(node), i, i))
            history.add(State(int(node), i, i))
    for i in range(size):
        stack_state.append(StackState(firstNonTerminal, i))
    answer = set()
    idx = 0
    while len(work_queue) > 0:
        idx += 1
        if idx % 5000 == 0:
            sys.stdout.write("\r" + animation[(idx // 5000) % len(animation)])
            sys.stdout.flush()
        state = work_queue.pop()
        for edgeGrammar in graphGrammar:
            if int(edgeGrammar.begin) == int(state.grammarPointer):
                for edgeGraph in graph:
                    if state.grammarPointer == int(edgeGrammar.begin) and state.graphPointer == int(
                            edgeGraph.begin) and edgeGrammar.s == edgeGraph.s:
                        new_state = State(int(edgeGrammar.end), int(edgeGraph.end), state.stackPointer)
                        if new_state not in history:
                            work_queue.append(new_state)
                            history.add(new_state)
                if not edgeGrammar.s.isdigit():  # nonterminal symbol
                    new_stack_state = StackState(edgeGrammar.s, state.graphPointer)
                    new_stack_edge = None
                    if new_stack_state not in stack_state:
                        new_stack_edge = parser.Edge(len(stack_state), state.stackPointer, edgeGrammar.end)
                        stack_state.append(new_stack_state)
                    else:
                        new_stack_edge = parser.Edge(stack_state.index(new_stack_state), state.stackPointer,
                                                     edgeGrammar.end)
                    if new_stack_edge not in stack_edge:
                        stack_edge.add(new_stack_edge)
                    if stack_state[new_stack_edge.begin] in executed_stack_state:  # add new states
                        for obj in executed_stack_state[stack_state[new_stack_edge.begin]]:
                            new_state = State(int(new_stack_edge.s), obj[1], new_stack_edge.end)
                            if new_state not in history:
                                work_queue.append(new_state)
                                history.add(new_state)
                            answer.add(Ans(int(state.graphPointer), new_stack_state.nonterminal, obj[1]))
                    for node in start.get(edgeGrammar.s):
                        new_state = State(int(node), state.graphPointer, new_stack_edge.begin)
                        if new_state not in history:
                            work_queue.append(new_state)
                            history.add(new_state)
        for finish in end[int(state.grammarPointer)]:
            if finish == stack_state[state.stackPointer].nonterminal:
                for edge in stack_edge:
                    if int(edge.begin) == int(state.stackPointer):
                        new_state = State(int(edge.s), state.graphPointer, int(edge.end))
                        if new_state not in history:
                            history.add(new_state)
                            work_queue.append(new_state)
                answer.add(Ans(stack_state[state.stackPointer].pointer, stack_state[state.stackPointer].nonterminal,
                               state.graphPointer))
                if stack_state[state.stackPointer] in executed_stack_state:
                    executed_stack_state[stack_state[state.stackPointer]].append(
                        [state.grammarPointer, state.graphPointer])
                else:
                    executed_stack_state[stack_state[state.stackPointer]] = [[state.grammarPointer, state.graphPointer]]
    return answer


def calc_result(nonterminal, paths):
    ans = 0
    ans_path = set()
    for val in paths:
        if val.n == nonterminal:
            ans += 1
            ans_path.add(val)
    return ans

def check_small(graph, idx):
    if idx == 3:
        if len(graph) == 2652:
            print("passed")
        else:
            print("fail")
        return
    for edge in graph:
        if [edge.p1, edge.n, edge.p2] not in an.small[idx] and edge.n == "S":
            print("fail")
            return
    for edge in an.small[idx]:
        if Ans(edge[0], edge[1], edge[2]) not in graph:
            print("fail")
            return
    print("passed")

def run(grammar_path, graph_path, nonterminal):
    graphGrammar, start, end, _ = parser.parse_grammar(grammar_path)
    graph, size = parser.parse_graph(graph_path)
    matrix = GLL(graph, graphGrammar, start, end, nonterminal, size)
    for val in matrix:
        print(val)
    print(calc_result(nonterminal, matrix))

def run_all():
    run_big()
    run_small()

def run_big():
    path_graph = "data/graphs/"
    name_graphs = ["skos.dot", "generations.dot", "travel.dot", "univ-bench.dot", "atom-primitive.dot",
                   "biomedical-mesure-primitive.dot", "foaf.dot", "people_pets.dot", "funding.dot", "wine.dot",
                   "pizza.dot"]
    path_grammar = "data/grammars/"
    name_grammars = ["Q1_automata.txt", "Q2_automata.txt"]
    for name_grammar in name_grammars:
        for name_graph in name_graphs:
            graphGrammar, start, end, _ = parser.parse_grammar(path_grammar + name_grammar)
            graph, size = parser.parse_graph(path_graph + name_graph)
            ans = GLL(graph, graphGrammar, start, end, "S", size)
            print("\r" + name_grammar + " " + name_graph + ": " + str(calc_result("S", ans)) + "\n")

def run_small():
    path_graph = "data/small/"
    name_graphs = ["1/graph.txt", "2/graph.txt", "3/graph.txt", "4/graph.txt"]
    path_grammar = "data/small/"
    name_grammars = ["1/automata.txt", "2/automata.txt", "3/automata.txt", "4/automata.txt"]
    for i in range(4):
        graphGrammar, start, end, _ = parser.parse_grammar(path_grammar + name_grammars[i])
        graph, size = parser.parse_graph(path_graph + name_graphs[i])
        ans = GLL(graph, graphGrammar, start, end, "S", size)
        print(name_grammars[i] + " " + name_graphs[i])
        check_small(ans, i)


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("number of arguments < 3")
        sys.exit()

    graphGrammar, start, end, _ = parser.parse_grammar(sys.argv[1])
    graph, size = parser.parse_graph(sys.argv[2])
    ans = GLL(graph, graphGrammar, start, end, "S", size)
    if len(sys.argv) == 3:
        for edge in ans:
            print(edge) 
    else:
        with open(sys.argv[3],'w') as f:
            for edge in ans:
                f.write('\n' + str(edge))
