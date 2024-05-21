from collections import OrderedDict
from iengine import InferenceEngine

class ForwardChainingEngine(InferenceEngine):
    def __init__(self, kb, query, symbols):
        super().__init__(kb, query, symbols)
        self.known_facts = OrderedDict()  # Use OrderedDict instead of set to maintain the order of insertion
        self.agenda = []  # Initialize an agenda to keep track of symbols to be evaluated

    def forward_chain(self):
        # Evaluate each symbol to determine if it's already known
        for symbol in self.symbols:
            if self.evaluate(symbol):
                self.known_facts[symbol] = None  # Add known symbols to the known_facts dictionary
                self.agenda.append(symbol)  # Add known symbols to the agenda
                print("Add", symbol)  # Print the addition of known symbols

        # Process the agenda until it's empty
        while self.agenda:
            current = self.agenda.pop(0)  # Get the next symbol from the agenda
            if current == self.query:  # Check if the current symbol matches the query
                print("YES:", list(self.known_facts.keys()))  # Print the list of known facts if the query is reached
                return True  # Return True to indicate success
            if current not in self.known_facts:  # Check if the current symbol is not already known
                # Find applicable rules for the current symbol
                applicable_rules = [rule for rule in self.kb if current in self.antecedents(rule)]
                for rule in applicable_rules:
                    consequent = self.consequent(rule)  # Get the consequent of the rule
                    if all(symbol in self.known_facts for symbol in self.antecedents(rule)):
                        # If all antecedents of the rule are known, add the consequent to known facts and agenda
                        self.known_facts[consequent] = None
                        self.agenda.append(consequent)
                        print("Add", consequent)  # Print the addition of the consequent

        # If the agenda is empty and the query is not reached, print NO
        print("NO")
        return False

    def evaluate(self, symbol):
        # Check if the symbol is mentioned in any rule of the knowledge base
        return any(symbol in rule for rule in self.kb)

    def antecedents(self, rule):
        # Extract the antecedents of the rule
        if '=>' in rule:
            antecedent, _ = rule.split('=>', 1)
            return [part.strip() for part in antecedent.split('&')]
        return []

    def consequent(self, rule):
        # Extract the consequent of the rule
        if '=>' in rule:
            _, consequent = rule.split('=>', 1)
            return consequent.strip()
        return rule.strip()

    def execute_algorithm(self):
        # Execute the forward chaining algorithm
        self.forward_chain()
