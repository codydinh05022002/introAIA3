from abc import ABC, abstractmethod

class InferenceEngine(ABC):
    def __init__(self, kb, query, symbols):
        self.kb = kb
        self.query = query
        self.symbols = symbols

    @abstractmethod
    def execute_algorithm(self):
        pass
