from fa import *

automate = DFA()
automate.read_from("dfa2.txt")
# print(automate.transition_table)
# print(automate.nodes)
result1 = automate.minimization()
result2 = automate.minimization(result1)

while result1 != result2:
    result2 = automate.minimization(result1)

