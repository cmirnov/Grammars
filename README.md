# Grammars
- closure.py
- gll.py
- bottom_up.py

## Requirements:
python3

## Input data:
- closure.py - grammar in Chomsky normal form (grammars/*_hom)
- gll.py - grammars in graph representation (grammars/*_automata)
- bottom_up.py - grammars in graph representation (grammars/*_automata)
- terminals are numbers
- nonterminals are letters
- starting nonterminal is 'S'

## How to run:
```
python3 ui.py
```
# Remarks
If you run unit test the answer will be number of triplets with non terminal S.
If you are looking for full solution you should choose certain test

# Output into file
```
python3 closure.py path_to_hom path_to_input file_name
```
```
python3 gll.py path_to_automata path_to_input file_name
```
```
python3 bottom_up.py path_to_automata path_to_input file_name
```
