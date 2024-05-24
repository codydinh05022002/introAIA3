from iengine import *

class BackwardChainingEngine(InferenceEngine):
    def __init__(self, kb, query, symbols, known_facts):
        self.kb = kb
        self.query = query
        self.symbols = symbols
        self.known_facts = set(known_facts)
        self.visited = set()  # Set of visited elements to avoid revisiting, 
        self.inferred_facts = []  # Start empty, list to store the inferred facts as the algorithm executes

    def execute_algorithm(self):
        if self.backward_chain(self.query): #start with goal = query, then work backwards
            print(f"YES: {', '.join(self.inferred_facts)}")
        else:
            print("NO")

    def backward_chain(self, goal):
        # Check if the goal is known fact
        if goal in self.known_facts:
            if goal not in self.inferred_facts:
                self.inferred_facts.append(goal)
            return True

        # Avoid revisiting same goal in recursive methods and enter infinite loop
        if goal in self.visited:
            return False
        self.visited.add(goal)

        # Find rules that conclude  goal
        for clause in self.kb:
            if '=>' in clause:
                antecedent, consequent = clause.split('=>')
                antecedent = antecedent.strip()
                consequent = consequent.strip()
                if consequent == goal:
                    subgoals = [subgoal.strip() for subgoal in antecedent.split('&')] #split subgoals in case of a&b => c, etc.

                    if all(self.backward_chain(subgoal) for subgoal in subgoals): #checks if all the antecedents can be satisfied/proved true
                        self.known_facts.add(goal) #add to known facts to help with looping process
                        if goal not in self.inferred_facts:
                            self.inferred_facts.append(goal)
                        return True

        return False
