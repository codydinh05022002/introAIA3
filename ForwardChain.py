from iengine import *

class ForwardChainingEngine(InferenceEngine):
    def __init__(self, kb, query, symbols, known_facts):
        self.kb = kb
        self.query = query
        self.symbols = symbols
        self.known_facts = set(known_facts)
        self.inferred_facts = list(known_facts)  # Start with known facts

    def execute_algorithm(self):
        new_inferred = True # Reset the flag for each iteration
        while new_inferred:
            new_inferred = False
            for clause in self.kb:
                if '=>' in clause:
                    antecedent, consequent = clause.split('=>')
                    antecedent = antecedent.strip()
                    consequent = consequent.strip()
                    subgoals = [subgoal.strip() for subgoal in antecedent.split('&')] # Split antecedent into subgoals incase of a&b=>c, etc.
                    if all(subgoal in self.known_facts for subgoal in subgoals) and consequent not in self.known_facts: # check if all antecedents are known and consequent not known
                        self.known_facts.add(consequent)
                        self.inferred_facts.append(consequent)
                        new_inferred = True # indicate new fact was inferred
                        if consequent == self.query: # check if query is inferred, if not keep going, if yes print result
                            print(f"YES: {', '.join(self.inferred_facts)}")
                            return
        print("NO")
