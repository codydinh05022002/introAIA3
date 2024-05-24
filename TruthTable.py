from itertools import product
from iengine import *

class TruthTableEngine(InferenceEngine):
    def __init__(self, kb, query, symbols):
        self.kb = kb
        self.query = query
        self.symbols = list(symbols)

    def execute_algorithm(self):
        models = self.generate_all_models()
        valid_models = 0
        total_models = 0
        valid_model_list = []

        for model in models:
            # Evaluate KB for the current model
            kb_result = self.evaluate_kb(model)
            query_result = self.evaluate_query(model) if kb_result else False

            if kb_result:
                total_models += 1  # Count models where KB is true
                if query_result:
                    valid_models += 1  # Count models where KB and query are true
                    valid_model_list.append(model)

        if valid_models > 0:
            print(f"YES: {valid_models}")
        else:
            print("NO")

    def generate_all_models(self):
        all_models = []
        for values in product([True, False], repeat=len(self.symbols)):
            model = dict(zip(self.symbols, values))
            all_models.append(model)
        return all_models

    def evaluate_kb(self, model):
        for clause in self.kb:
            clause_result = self.evaluate_clause(clause, model)
            if not clause_result:
                return False
        return True

    def evaluate_query(self, model):
        query_result = model[self.query]
        return query_result

    def evaluate_clause(self, clause, model):
        if '=>' in clause:
            antecedent, consequent = clause.split('=>')
            antecedent = antecedent.strip()
            consequent = consequent.strip()
            return not self.evaluate_expression(antecedent, model) or self.evaluate_expression(consequent, model)
        else:
            return self.evaluate_expression(clause, model)

    def evaluate_expression(self, expression, model):
        if '&' in expression:
            symbols = [symbol.strip() for symbol in expression.split('&')]
            return all(model[symbol] for symbol in symbols)
        else:
            return model[expression.strip()]