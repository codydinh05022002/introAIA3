from iengine import *
from collections import OrderedDict

class ForwardChainingEngine(InferenceEngine):
    def __init__(self, kb, query, symbols):
        super().__init__(kb, query, symbols)
        self.known_facts = OrderedDict()
        self.agenda = []

    def forward_chain(self):
        for symbol in self.symbols:
            if self.evaluate(symbol):
                self.known_facts[symbol] = None
                self.agenda.append(symbol)
                print("Add", symbol)
        
        while self.agenda:
            current = self.agenda.pop(0)
            if current == self.query:
                print("YES:", list(self.known_facts.keys()))
                return True
            if current not in self.known_facts:
                applicable_rules = [rule for rule in self.kb if current in self.antecedents(rule)]
                for rule in applicable_rules:
                    consequent = self.consequent(rule)
                    if all(symbol in self.known_facts for symbol in self.antecedents(rule)):
                        self.known_facts[consequent] = None
                        self.agenda.append(consequent)
                        print("Add", consequent)
        print("NO")
        return False

    def evaluate(self, symbol):
        return any(symbol in rule for rule in self.kb)

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
        self.forward_chain()
