from iengine import *  
from collections import OrderedDict

class BackwardChainingEngine(InferenceEngine):  
    def __init__(self, kb, query, symbols): 
        super().__init__(kb, query, symbols)  
        self.known_facts = OrderedDict()  # Dictionary to store known facts in order
        self.inferred = set()  # Set to keep track of inferred facts

    def backward_chain(self):  
        result = self.bc_or(self.query)  
        if result:
            print("YES:", list(self.known_facts.keys()))  
        else:
            print("NO")  
        return result 

    def bc_or(self, goal):  # handle OR operation in bc
        if goal in self.known_facts:  
            return True

        if goal in self.inferred: 
            return False

        self.inferred.add(goal)  # Add goal to the set of inferred facts

        applicable_rules = [rule for rule in self.kb if self.consequent(rule) == goal]  # Find applicable rules for the goal

        for rule in applicable_rules:  # Iterate over applicable rules
            if self.bc_and(self.antecedents(rule)):  # Check if all antecedents of the rule can be satisfied
                self.known_facts[goal] = None  # If so, add the goal to known facts
                print("Add", goal)  # Print that the goal is added
                return True  # Return True

        return False  # If no applicable rule found, return False

    def bc_and(self, goals):  # Method to handle AND operation in backward chaining
        for goal in goals:  # Iterate over goals
            if not self.bc_or(goal):  # If any goal cannot be satisfied, return False
                return False
        return True  # If all goals can be satisfied, return True

    def antecedents(self, rule):  # Method to extract antecedents from a rule
        if '=>' in rule:  # If the rule is an implication
            antecedent, _ = rule.split('=>', 1)  # Split the rule into antecedent and consequent
            return [part.strip() for part in antecedent.split('&')]  # Split antecedent by '&' and strip whitespaces
        return []  # If not an implication, return an empty list

    def consequent(self, rule):  # Method to extract consequent from a rule
        if '=>' in rule:  # If the rule is an implication
            _, consequent = rule.split('=>', 1)  # Split the rule into antecedent and consequent
            return consequent.strip()  # Return the stripped consequent
        return rule.strip()  # If not an implication, return the stripped rule

    def execute_algorithm(self):  # Method to execute the backward chaining algorithm
        self.backward_chain()  # Call the backward chaining method to start the inference process
