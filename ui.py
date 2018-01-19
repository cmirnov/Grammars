import closure
import gll
import bottom_up

print("input 0 and run all methods\ninput 1 and run certain method\n")
is_certain = int(input())
if is_certain == 0:
    print("input 0 and run all tests\ninput 1 and run big tests\ninput 2 and run small test")
    type_of_tests = int(input())
    if type_of_tests == 0:
        closure.run_all()
        gll.run_all()
        bottom_up.run_all()
    if type_of_tests == 1:
        closure.run_big()
        gll.run_big()
        bottom_up.run_big()
    if type_of_tests == 2:
        closure.run_small()
        gll.run_small()
        bottom_up.run_small()

if is_certain == 1:
    print("input number of algorithm to run:")
    print("\t1 - trans closure")
    print("\t2 - gll")
    print("\t3 - bottom up")
    number = int(input())
    print("to run unit tests input 0 otherwise input 1")
    unit_tests = int(input())
    if unit_tests == 1:
        grammar_path = input("input path to file with grammar: ")
        graph_path = input("input path to file with input: ")
        if number == 1:
            closure.run(grammar_path, graph_path)
        if number == 2:
            nonterminal = input("input first nonterminal: ")
            gll.run(grammar_path, graph_path, nonterminal)
        if number == 3:
            nonterminal = input("input first nonterminal: ")
            bottom_up.run(grammar_path, graph_path, nonterminal)
    else:
        print("input 0 and run all tests\ninput 1 and run big tests\ninput 2 and run small test")
        type_of_tests = int(input())
        if number == 1:
            if type_of_tests == 0:
                closure.run_all()
            if type_of_tests == 1:
                closure.run_big()
            if type_of_tests == 2:
                closure.run_small()
        if number == 2:
            if type_of_tests == 0:
                gll.run_all()
            if type_of_tests == 1:
                gll.run_big()
            if type_of_tests == 2:
                gll.run_small()
        if number == 3:
            if type_of_tests == 0:
                bottom_up.run_all()
            if type_of_tests == 1:
                bottom_up.run_big()
            if type_of_tests == 2:
                bottom_up.run_small()

