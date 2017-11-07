#include <bits/stdc++.h>

using namespace std;

//Chomsky normal form
struct Rule {
  char left;
  char rightFirst;
  char rightSecond;
  bool terminal;
  Rule(char l, char rf) {
    left = l;
    rightFirst = rf;
    terminal = true;
  }
  Rule(char l, char rf, char rs) {
    left = l;
    rightFirst = rf;
    rightSecond = rs;
    terminal = false;
  }
  bool isTerminal() {
    return this->terminal;
  }
};

// it is dummy for now
void parseGraph(vector<vector<char>> &m, string const fileName) {
  m = {{0, 'n', 0}, {0, 0, '+'}, {0, 'n', 0}};
}

void parseGrammar(vector<Rule*> &grammar) {
  grammar.push_back(new Rule('E', 'n'));
  grammar.push_back(new Rule('E', 'E', 'R'));
  grammar.push_back(new Rule('R', 'P', 'E'));
  grammar.push_back(new Rule('P', '+'));
}

void initNewAdjMatrix(vector<vector<char>> const &m, vector<vector<vector<char>>> &adjM, vector<Rule*> &grammar) {
  for (size_t i = 0; i < grammar.size(); ++i) {
    if (grammar[i]->isTerminal()) {
      char terminal = grammar[i]->rightFirst;
      for (size_t j = 0; j < m.size(); ++j) {
        for (size_t k = 0; k < m.size(); ++k) {
          if (m[j][k] == terminal) {
            adjM[j][k].push_back(grammar[i]->left);
          }
        }
      }
    }
  }
}


void calcTransRed(vector<vector<vector<char>>> &adjM, vector<Rule*>  &grammar) {
  size_t size = adjM.size();
  for (size_t i1 = 0; i1 < size; ++i1) {
    for (size_t j1 = 0; j1 < size; ++j1) {
      if (adjM[i1][j1].size()) {
        for (size_t j2 = 0; j2 < size; ++j2) {
          if (adjM[j1][j2].size()) {
            for (size_t i = 0; i < grammar.size(); ++i) {
              if (!grammar[i]->isTerminal()) {
                for (size_t k1 = 0; k1 < adjM[i1][j1].size(); ++k1) {
                  for (size_t k2 = 0; k2 < adjM[j1][j2].size(); ++k2) {
                    if (grammar[i]->rightFirst == adjM[i1][j1][k1] && grammar[i]->rightSecond == adjM[j1][j2][k2]) {
                      bool exists = false;
                      for (size_t j = 0; j < adjM[i1][j2].size(); ++j) {
                        if (adjM[i1][j2][j] == grammar[i]->left) {
                          exists = true;
                          break;
                        }
                      }
                      if (!exists) {
                        adjM[i1][j2].push_back(grammar[i]->left);
                      }
                    }       
                  }
                }  
              }
            }
          }
        } 
      }
    }
  }
}

void print(vector<vector<vector<char>>> const &adjM) {
  size_t size = adjM.size();
  for (size_t i = 0; i < size; ++i) {
    for (size_t j = 0; j < size; ++j) {
      for (int k = 0; k < adjM[i][j].size(); ++k) {
        cout << i << " " << adjM[i][j][k] << " " << j << endl;
      }
    }
  }
}

int main() {
  vector<vector<char>> m;
  parseGraph(m, "");
  vector<Rule*> grammar;
  parseGrammar(grammar);
  vector<vector<vector<char>>> adjM(m.size());
  for (int i = 0; i < m.size(); ++i) {
    adjM[i].resize(m.size());
  }
  initNewAdjMatrix(m, adjM, grammar);
  calcTransRed(adjM, grammar);
  print(adjM);
}
