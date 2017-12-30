import closure
import gll
import bottom_up

print("input number of algorithm to run:")
print("\t1 - trans closure")
print("\t2 - gll")
print("\t3 - bottom up")
number = int(input())
print("to run unit tests input 0 otherwise input 1")
unit_tests = int(input())
if unit_tests == 1:
    grammar_path = input("input path to file with grammar:")
    graph_path = input("input path to file with input:")
    if number == 1:
        closure.run(grammar_path, graph_path)
    if number == 2:
    	nonterminal = input("input first nonterminal:")
        gll.run(grammar_path, graph_path, nonterminal)
    if number == 3:
        bottom_up.run(grammar_path, graph_path)
else:
    if number == 1:
        closure.run_tests()
    if number == 2:
        gll.run_tests()
    if number == 3:
        bottom_up.run_tests()

