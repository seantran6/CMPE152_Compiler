class Tokenizer:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.currentCharacter = self.code[self.position]

    def increment(self):
        self.position += 1
        if self.position < len(self.code):
            self.currentCharacter = self.code[self.position]
        else:
            self.currentCharacter = None

    def getNextToken(self):
        while self.currentCharacter is not None:
            if self.currentCharacter == '(':
                self.increment()
                return Tokenizer('LEFT PARENTHESIS', '(')
            elif self.currentCharacter == ')':
                self.increment()
                return Tokenizer('RIGHT PARENTHESIS', ')')
            elif self.currentCharacter == '"':
                self.increment()
                return Tokenizer('QUOTATIONS', '"')
            elif self.currentCharacter.isspace():
                self.increment()
            else:
                self.increment()
                return Tokenizer('ERROR', 'Invalid token')

        return Tokenizer('End of File', None)

def main():
    try:
        print("Starting main function")
        with open('testcode.txt', 'r') as file:
            for line in file:
                print("Line Read:", line.strip())
                lexer = Lexer(line.strip())
                print("Processing Tokens in the Line")
                while True:
                    token = lexer.getNextToken()
                    if token.type == 'End of File':
                        break
                    print("Token:", token.type, token.value)
        print("-------------------------")
    except Exception as e:
        print("An ERROR Occurred:", e)

if __name__ == "__main__":
    main()