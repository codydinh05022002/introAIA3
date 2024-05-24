class fileReader:
    def __init__(self, filename):
        self.filename = filename
        self.kb = []
        self.query = None
        self.symbols = set()
        self.known_facts = []

    def read_input(self):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                tell_index = lines.index('TELL\n')
                ask_index = lines.index('ASK\n')

                # Process the TELL section
                for i in range(tell_index + 1, ask_index):
                    line = lines[i].strip()
                    if line:  # Ignore empty lines
                        clauses = [clause.strip() for clause in line.split(';') if clause.strip()]
                        for clause in clauses:
                            if '=>' in clause:
                                self.kb.append(clause)
                            else:
                                self.known_facts.append(clause)
                                self.symbols.add(clause)

                self.query = lines[ask_index + 1].strip()

                # Debug
                print(f"KB: {self.kb}")
                print(f"Query: {self.query}")
                print(f"Known Facts: {self.known_facts}")

                # Extract symbols from KB and query
                for sentence in self.kb:
                    self.symbols.update(self.extract_symbols(sentence))
                self.symbols.update(self.extract_symbols(self.query))

                # Debug
                print(f"Symbols extracted: {self.symbols}")

        except FileNotFoundError:
            print("File not found!")
            raise

        return self.kb, self.query, self.symbols, self.known_facts

    def extract_symbols(self, sentence):
        symbols = set()
        parts = sentence.split('=>')
        for part in parts:
            symbols.update([symbol.strip() for symbol in part.strip().split('&') if symbol.strip()])
        return symbols
