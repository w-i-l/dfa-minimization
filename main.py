from fa import *

automate = DFA()
automate.read_from("dfa2.txt")
# print(automate.transition_table)
# print(automate.nodes)
result1 = automate.minimization()
print(result1)
# # result2 = automate.minimization(result1)

# for x in range(len(automate.nodes)):
#     copy = automate.minimization(result1)
#     # if result1 == copy:
#     #     break

# print(copy)

# x = [[node for node in automate.nodes if not node.final]]
# x.append([node for node in automate.nodes if node.final])

# result1 = automate.minimization(x)
# # result2 = automate.minimization(result1)

# for x in range(len(automate.nodes)):
#     copy = automate.minimization(result1)
#     if result1 == copy:
#         break

# while result1 != result2:
#     result2 = automate.minimization(result1)

