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
    
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.number == other.number
                    and self.final == other.final
                    and self.paths == other.paths)
        return False
    
    
    def __hash__(self):
        return hash(self.number)


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
    
    
    # checks to see if two nodes
    # are in the same subset
    # returns None if both of them are
    def _same_subset(self, equivalnce, node1, node2):

        for letter in self.alphabet:

            # check to see if both of them are abort state
            if node1.next(letter)[0] == -1 and node2.next(letter)[0] != -1:
                return node1
            elif node2.next(letter)[0] == -1 and node1.next(letter)[0] != -1:
                return  node2

            # next nodes based on letter
            next1 = self.nodes[node1.next(letter)[0]]
            next2 = self.nodes[node2.next(letter)[0]]

            for subset in equivalnce:

                # if one of them is in the subset
                # and the other not
                if (next1 not in subset and next2 in subset):
                    return node1
                
                elif (next1 in subset and next2 not in subset):
                    return node2
    
        return None
    

    
    def _add_to_equivalence(self, equivalance, coppy, node):

        for subset in equivalance:
            
            # we only have to check with the one
            # because if it doesn't fit with one
            # it won't fit with any
            other = subset[0]

            if self._same_subset(coppy, node, other) == None and node.final == other.final:
                subset.append(node)
                return
            
        # if we couldn't add to any subset
        equivalance.append([node])


    
    def _compute_equivalence(self, equivalence=None):

        from copy import deepcopy
        
        if equivalence == None:
            # initialization with the non final states
            equivalence = [[x for x in self.nodes if x.final == False]]
            # adding final states
            equivalence.append([x for x in self.nodes if x.final])

        coppy = deepcopy(equivalence)

        for subset in equivalence:      
            if len(subset) > 1:
                
                # we take pairs of nodes
                for index, node1 in enumerate(subset):
                    for node2 in subset[min(index + 1, len(subset)-1):]:

                        # check to see if they are related
                        result = self._same_subset(coppy, node1, node2)
                        
                        if result == None:
                            continue

                        else:

                            # we remove the node
                            node = result
                            try:
                                subset.remove(node)
                            except Exception:
                                pass
                            
                            # and try to find a place
                            self._add_to_equivalence(equivalence, coppy, node)

        return sorted(list(map(lambda x: list(set(x)), equivalence)), reverse=True)

    

    def minimization(self):

        result = self._compute_equivalence()

        for _ in range(len(self.nodes)):

            copy = self._compute_equivalence(result)

            if copy == result:
                break
        
        return sorted(copy)
    

    # we reindex the nodes based on the position
    # in equivalence
    def write_to_file(self, filename, equivalence):
        
        f = open(filename, "w")

        for index, subset in enumerate(equivalence):
            
            f.write(f"{index} {'f' if subset[0].final else 'n'}")
            
            for letter in self.alphabet:

                # check for the abort state                
                if subset[0].next(letter)[0] != -1:

                    # next node
                    next = self.nodes[subset[0].next(letter)[0]]

                    # next subset 
                    sub = [x for x in equivalence if next in x][0]
                    # the index of the next subset that
                    # we go to with the letter
                    id = equivalence.index(sub)

                    f.write(f" {id} {letter}")

            f.write("\n")
        
        f.close()
