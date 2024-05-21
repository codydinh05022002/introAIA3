from iengine import *
from collections import OrderedDict


class BackwardChainingEngine(InferenceEngine):
    def __init__(self, kb, query, symbols):
        super().__init__(kb, query, symbols)
        self.known_facts = OrderedDict()  
        self.inferred = set()

    def backward_chain(self):
        result = self.bc_or(self.query)
        if result:
            print("YES:", list(self.known_facts.keys()))
        else:
            print("NO")
        return result

    def bc_or(self, goal):
        if goal in self.known_facts:
            return True

        if goal in self.inferred:
            return False

        self.inferred.add(goal)

        applicable_rules = [rule for rule in self.kb if self.consequent(rule) == goal]

        for rule in applicable_rules:
            if self.bc_and(self.antecedents(rule)):
                self.known_facts[goal] = None
                print("Add", goal)
                return True

        return False

    def bc_and(self, goals):
        for goal in goals:
            if not self.bc_or(goal):
                return False
        return True

    def antecedents(self, rule):
        if '=>' in rule:
            antecedent, _ = rule.split('=>', 1)
            return [part.strip() for part in antecedent.split('&')]
        return []

    def consequent(self, rule):
        if '=>' in rule:
            _, consequent = rule.split('=>', 1)
            return consequent.strip()
        return rule.strip()

    def execute_algorithm(self):
        self.backward_chain()

