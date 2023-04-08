class Node:

    # Object methods
    def __init__(self, number, final, paths):

        # naming convetion q{number}
        self.number = number
        # if the node is final
        self.final = final
        # the node that are adjacent
        self.paths = {}

        # creating the dict with key a letter
        # and the value a list with all nodes
        for elem in paths:
            try:
                self.paths[elem[0]].append(elem[1])
            except Exception:
                self.paths[elem[0]] = [elem[1]]

    def display(self):
        print(self.number, self.final, self.paths)

    # next node from a given letter
    def next(self, letter):
        # we try to get the next node
        try:
            return self.paths[letter]
        # if we receive an invalid letter
        # we are out of transitions
        except Exception:
            return [-1]

    def __str__(self):
        return f"q{self.number}"

    def __repr__(self):
        return f"q{self.number}"

    def __lt__(self, other):
        return self.number < other.number

class FA:

    def __init__(self):
        # f for final n for non-final
        self.current_state = 0
        # all the component nodes
        self.nodes = []
        # a list with the nodes visited for a result
        self.result = [0]
        self.alphabet = set()
        self.transition_table = {}

    # reads the FA from filename
    def read_from(self, filename):
        with open(filename, 'r') as f:
            for line in f.readlines():

                data = line.strip().split()
                paths = [(data[i+1], int(data[i])) for i in range(2,len(data),2)]
                final = True if data[1] == 'f' else False

                for path in paths:
                    self.alphabet.add(path[0])

                self.nodes.append(Node(data[0], final, paths))
        
        self._generate_transition_table()

    # deletes the read nodes
    def empty(self):

        self.nodes = []
    
    def _generate_transition_table(self):

        for node in self.nodes:
            for letter in self.alphabet:
                try:
                    self.transition_table[node][letter] = node.next(letter)
                except:
                    self.transition_table[node] = {}
                    self.transition_table[node][letter] = node.next(letter)

class DFA(FA):
    
    def __init__(self):
        super().__init__()

    def validate_word(self, word):

        # we use a mutable object
        word = list(word)

        # iterating until we have lambda or we are in
        # an invalid state
        while len(word) and self.current_state != -1:

            # get the current letter to be processed
            current_letter = word.pop(0)

            # get the next node
            try:
                self.current_state = self.nodes[self.current_state].next(current_letter)[0]
            except Exception:
                print(self.current_state)


            # check to see if we have an invalid state
            if self.current_state == -1:
                print('not accepted')
                return
            
            # save the path
            self.result.append(self.current_state)

        # check if we proceed all letters
        # and we are in a final state
        if len(word) == 0 and self.nodes[self.current_state].final:
            # print('accepted')
            print("Path: ", *self.result, end=' ')
            print()
            return 'accepted'
        else:
            print("not accepted")
            print(word, self.current_state)
            return 'not accepted'
    
    def _same_subset(self, equivalnce, node1, node2):

        for letter in self.alphabet:

            if node1.next(letter)[0] == -1 and node2.next(letter)[0] != -1:
                return node1
            elif node2.next(letter)[0] == -1 and node1.next(letter)[0] != -1:
                return  node2
            
            # print("Nodes: ", node1, node2)
            # print("Next:  ",node1.next(letter)[0], " ", node2.next(letter)[0])

            next1 = self.nodes[node1.next(letter)[0]]
            next2 = self.nodes[node2.next(letter)[0]]

            for subset in equivalnce:
                if (next1 not in subset and next2 in subset):
                    print("letter", letter, "node", node1, node2, "next", next1, next2)
                    # print("Leter: ", letter)
                    return node1
                
                elif (next1 in subset and next2 not in subset):
                    print("letter", letter, "node", node1, node2, "next", next1, next2)
                    # print("Leter: ", letter)
                    return node2

                    # return node1 if next1 not in subset else node2
                    # return False
        
        return None
    

    def _add_to_equivalence(self, equivalance, node):

        for subset in equivalance:
            
            # we only have to check with the one
            # because if it doesn't fit with one
            # it won't fit with any
            other = subset[0]

            if self._same_subset(equivalance, node, other) == None and node.final == other.final:
                subset.append(node)
                return
            
        # if we couldn't add to any subset
        equivalance.append([node])


    def minimization(self, equivalence=None):

        from copy import deepcopy

        
        if equivalence == None:
            # initialization with the non final states
            equivalence = [[x for x in self.nodes if x.final == False]]
            # adding final states
            equivalence.append([x for x in self.nodes if x.final])

        print(equivalence)


        for subset in equivalence:      
            if len(subset) > 1:
                for index, node1 in enumerate(subset):
                    for node2 in subset[min(index + 1, len(subset)-1):]:

                        # print(node1, node2)
                        result = self._same_subset(equivalence, node1, node2)
                        if result == None:
                            continue

                        else:
                            # node = node1 if node1 not in subset else node2
                            node = result
                            try:
                                subset.remove(node)
                            except Exception:
                                # print("ERROR!",subset, node)
                                pass
                            self._add_to_equivalence(equivalence, node)
                            
                            # print(node, equivalence)
        print(equivalence)
                            
        # print(equivalence)
        # return list(map(lambda x: sorted(x), equivalence))
        return list(map(lambda x: list(set(x)), equivalence))

    def write_to_file(self, filename, equivalence):
        
        dict = {}

        for subset in equivalence:
            for letter in self.alphabet:
                try:
                    dict["".join(map(lambda x: str(x),subset))][letter].add(self.transition_table[node])
                except Exception:
                    dict["".join(map(lambda x: str(x),subset))] = {letter : set() for letter in self.alphabet}

        for node in self.transition_table:
            for letter in self.alphabet:
                n = [key for key in dict if str(node) in key][0]
                dict[n][letter].add(self.transition_table[node][letter][0])
        
        print(dict)

        # with open(filename, 'w') as f:
        #     for node in dict:

        #         final = False
        #         for letter in node.replace('q', ''):
        #             if self.nodes[int(letter)].final:
        #                 final = True

        #         f.write(f"{node.replace('q', '')} {'f' if final else 'n'} ")
        #         for letter in self.alphabet:
        #                 try:
        #                     n = str(list(dict[node][letter])[0])
        #                     # print(n, [key for key in dict])
        #                     n = [key for key in dict if n in key][0]
        #                     f.write(f"{n.replace('q', '')} {letter} ")
        #                 except:
        #                     f.write(f"{-1} {letter} ")
        #         f.write("\n")

