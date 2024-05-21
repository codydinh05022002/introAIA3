from itertools import product
from iengine import *

class TruthTableEngine(InferenceEngine):
    def __init__(self, kb, query, symbols):
        super().__init__(kb, query, symbols)
        self.models = []

    def tt_entails(self):
        symbols = list(self.symbols)
        self.models = []  # Clear models before checking entailment
        self.tt_check_all(symbols)
        true_models = [model for model in self.models if self.pl_true(self.query, symbols, model)]
        return len(true_models), true_models

    def tt_check_all(self, symbols):
        # Generate all combinations of truth values for the symbols
        for model in product([True, False], repeat=len(symbols)):
            model_dict = {symbols[i]: model[i] for i in range(len(symbols))}
            if all(self.pl_true(sentence, symbols, model_dict) for sentence in self.kb):
                self.models.append(model_dict)

    def pl_true(self, sentence, symbols, model):
        if '&' in sentence:
            parts = sentence.split('&')
            return all(self.pl_true(part.strip(), symbols, model) for part in parts)
        elif '=>' in sentence:
            antecedent, consequent = sentence.split('=>', 1)
            result = not self.pl_true(antecedent.strip(), symbols, model) or self.pl_true(consequent.strip(), symbols, model)
            return result
        else:
            if sentence in model: # Evaluate the atomic sentence based on the model
                return model[sentence]
            else:
                return False  # If the sentence is not a recognized symbol, return False

    def execute_algorithm(self):
        count, true_models = self.tt_entails()
        for model in self.models: #Debug 
                print("YES", model)
        if count > 0:
            print("YES:", count)
        else:
            print("NO")


