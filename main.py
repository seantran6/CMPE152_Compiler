import re
import ast

class Tokenizer:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.currentCharacter = self.code[self.position]
        print("Lexer Initiated with Code:", self.code)

    def increment(self):
        #print("Position before Increment", self.position)
        self.position += 1

        if self.position < len(self.code):
            self.currentCharacter = self.code[self.position]
        else:
            self.currentCharacter = None
        
        #print("Position After Increment:", self.position)
        #print("Current Character After Increment", self.currentCharacter)
    

    def skipWhitespace(self):
        while self.currentCharacter is not None and self.currentCharacter.isspace():
            self.increment()
        
    def getNextToken(self):
        #print("Current Character:", self.currentCharacter)
        while self.currentCharacter is not None:
            if self.position >= len(self.code):
                return Tokenizer('End of File', None)
            
            elif self.currentCharacter.isspace():
                self.skipWhitespace()
                continue
            
            elif self.currentCharacter.isalpha():
                token = self.tokenizeIdentifier()
                self.increment()
                return token
            
            elif self.currentCharacter.isdigit():
                token = self.tokenizeNumber()
                self.increment()
                return token
            
            elif self.currentCharacter == '+':
                self.increment()
                if self.currentCharacter == '=':
                    self.increment()
                    return Tokenizer('INCREMENT', '+=')
                else:
                    return Tokenizer('ADDITION', '+')
                
            elif self.currentCharacter == '-':
                self.increment()
                if self.currentCharacter == '=':
                    self.increment()
                    return Tokenizer('DECREMENT', '+=')
                else:
                    return Tokenizer('SUBTRACTION', '-')
                
            elif self.currentCharacter == '*':
                self.increment()
                if self.currentCharacter == '*':
                    self.increment()
                    return Tokenizer('EXPONENT', '**')
                else:
                    return Tokenizer('MULTIPLICATION', '*')
                
            elif self.currentCharacter == '=':
                self.increment()
                if self.currentCharacter == '=':
                    self.increment()
                    return Tokenizer('EQUAL', '==')
                else:
                    return Tokenizer('BECOMES', '=')
                
            elif self.currentCharacter == '!':
                self.increment()
                if self.currentCharacter == '=':
                    self.increment()
                    return Tokenizer('INEQUAL', '!=')
                else:
                    return Tokenizer('n/a', '!')
                
            elif self.currentCharacter == '>':
                self.increment()
                if self.currentCharacter == '=':
                    self.increment()
                    return Tokenizer('GREATER THAN OR EQUAL', '>=')
                else:
                    return Tokenizer('GREATER', '>')
                
            elif self.currentCharacter == '<':
                self.increment()
                if self.currentCharacter == '=':
                    self.increment()
                    return Tokenizer('LESS THAN OR EQUAL', '<=')
                else:
                    return Tokenizer('GREATER', '>')

            elif self.currentCharacter == '/':
                self.increment()
                return Tokenizer('DIVIDE', '/')
            
            elif self.currentCharacter == '(':
                self.increment()
                return Tokenizer('LEFT PARENTHESIS', '(')
            
            elif self.currentCharacter == ')':
                self.increment()
                return Tokenizer('RIGHT PARENTHESIS', ')')
            
            elif self.currentCharacter == '"':
                self.increment()
                return Tokenizer('QUOTATIONS', '"')
            
            elif self.currentCharacter == '[':
                self.increment()
                return Tokenizer('LEFT BRACKET', '[')
            
            elif self.currentCharacter == ']':
                self.increment()
                return Tokenizer('RIGHT BRACKET', ']')
            
            elif self.currentCharacter == '{':
                self.increment()
                return Tokenizer('LEFT BRACES', '{')
            
            elif self.currentCharacter == '}':
                self.increment()
                return Tokenizer('RIGHT BRACES', '}')
            
            elif self.currentCharacter == '%':
                self.increment()
                return Tokenizer('MODULO', '%')
            
            elif self.currentCharacter == ':':
                self.increment()
                return Tokenizer('COLON', ':')
            
            elif self.currentCharacter == '#':
                self.increment()
                return Tokenizer('COMMENT', '#')
                    
            else:
                self.increment()
                return Tokenizer('ERROR', 'n/a')
            
            
        
        #print("Current Character After Loop:", self.currentCharacter)
        return Tokenizer('End of File', None)
    
    def tokenizeIdentifier(self):
        result = ''

        while self.currentCharacter is not None and (self.currentCharacter.isalnum() or self.currentCharacter == '_'):
            result += self.currentCharacter
            self.increment()

        if result:
            if result.lower() == 'print':
                return Tokenizer('PRINT', 'print')
            elif result.lower() == 'if':
                return Tokenizer('IF', 'if')
            elif result.lower() == 'and':
                return Tokenizer('AND', 'and')
            elif result.lower() == 'or':
                return Tokenizer('OR', 'or')
            elif result.lower() == 'not':
                return Tokenizer('NOT', 'not')
            else:
                return Tokenizer('IDENTIFIER', result)

        #print("Tokenize Identifier: Result", result)    
        return Tokenizer('IDENTIFIER', result)
    
    def tokenizeNumber(self):
        result = ''

        while self.currentCharacter is not None and self.currentCharacter.isdigit():
            result += self.currentCharacter
            self.increment()
        
        if result:
            #print("Tokenize Number: Result", result)
            return Tokenizer('NUMBER', int(result))
        
        #print("Tokenize Number: Error - Invalid Number Format")
        return Tokenizer('ERROR', 'Invalid Number Format')
    
def extractNumber(text):
        tokens = ''.join(re.findall('[0123456789+-^/*()]', text))
        return tokens

def math(text):
        tokens = extractNumber(text)
        result = calculate(tokens)
        return result
    
def calculate(expression):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

        def applyOperator(operators, values):
            #print("Applying Operator:", operators[-1])
            #print("Current Values:", values)
            #print("Current Operators:", operators)

            operator = operators.pop()
            right = values.pop()
            left = values.pop()

            if operator == '+':
                values.append(left + right)
            
            elif operator == '-':
                values.append(left - right)

            elif operator == '*':
                values.append(left * right)
            
            elif operator == '/':
                values.append(left / right)

            elif operator == '^':
                values.append(left ** right)
            
            
        
        def evaluate(expression):
            values = []
            operators = []

            i = 0

            while i < len(expression):
                if expression[i] == '(':
                    j = i
                    count = 0
                    while j < len(expression):
                        if expression[j] == '(':
                            count += 1
                        elif expression[j] == ')':
                            count -= 1
                            if count == 0:
                                break
                        j += 1
                    
                    values.append(evaluate(expression[i + 1 : j]))
                    i = j
                
                elif expression[i].isdigit():
                    j = i
                    while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                        j += 1
                    values.append(float(expression[i : j]))
                    i = j - 1
                
                elif expression[i] in precedence:
                    #print("Encountered operator:", expression[i])  # Add this line for debugging
                    #print("Pushing operator onto stack:", expression[i])  # Add this line for debugging
                    operators.append(expression[i])

                elif expression[i] == ')':
                    while operators[-1] != '(':
                        #print("Pooping and Applying Operators from Stack:", operators[-1])
                        applyOperator(operators, values)
                    operators.pop()

                i += 1

            while operators:
                #print("Popping and Applying Operator From Stack:", operators[-1])
                applyOperator(operators, values)

            return values[0]
            
        return evaluate(expression)
       


def ifStatement(text):
    print("Inside ifStatement. Text:", text)  # Add this line for debugging
    parts = text.split(':', 1)  # Split into condition and code block
    print("Parts after split:", parts)  # Add this line for debugging

    if len(parts) != 2:
        return 'ERROR: Incorrect If-Statement Format'

    condition = parts[0].strip()  # Extract the condition part
    code_block = parts[1]

    print("Condition:", condition)
    result = compareStatement(condition)
    print("Comparison Result:", result)  # Add debugging output
    if result == 'ERROR':
        return 'ERROR: Incorrect If Statement Format'
    elif not result:
        return ''
    else:
        return code_block
            
def logicalStatement(parts):
            parts2 = ''
            if 'and' in parts[0]:
                parts2 = parts[0].split('and')
                result1 = compareStatement(parts2[0])
                result2 = compareStatement(parts2[1])

                if result1 == True and result2 == False:
                    return parts[1]
                elif result1 == False or result2 == False:
                    return False
                elif result1 == 'ERROR' or result2 == 'ERROR':
                    return 'ERROR'
            elif 'or' in parts[0]:
                parts2 = parts[0].split('or')
                result1 = compareStatement(parts2[0])
                result2 = compareStatement(parts2[1])

                if result1 == True or result2 == True:
                    return parts[1]
                elif result1 == 'ERROR' or result2 == 'ERROR':
                    return 'ERROR'
                
def compareStatement(parts):
            print("Inside compareStatement. Parts:", parts)  # Add this line for debugging
            numbers = 0
            print("Comparing:", parts)

            if '==' in parts:
                numbers = parts.split('==')
                #print("Comparing:", numbers[0], "==", numbers[1])
                if float(numbers[0].strip()) == float(numbers[1].strip()):
                    #print("Result: True")
                    return True
                else:
                    #print("Result: False")
                    return False
                
            if '!=' in parts:
                numbers = parts.split('!=')
                #print("Comparing:", numbers[0], "!=", numbers[1])
                if float(numbers[0].strip()) != float(numbers[1].strip()):
                    #print("Result: True")
                    return True
                else:
                    #print("Result: False")
                    return False
                
            if '>=' in parts:
                numbers = parts.split('>=')
                #print("Comparing:", numbers[0], ">=", numbers[1])
                if float(numbers[0].strip()) >= float(numbers[1].strip()):
                    #print("Result: True")
                    return True
                else:
                    #print("Result: False")
                    return False
                
            if '<=' in parts:
                numbers = parts.split('<=')
                #print("Comparing:", numbers[0], "<=", numbers[1])
                if float(numbers[0].strip()) <= float(numbers[1].strip()):
                    #print("Result: True")
                    return True
                else:
                    #print("Result: False")
                    return False
                
            if '>' in parts:
                numbers = parts.split('>')
                #print("Comparing:", numbers[0], ">", numbers[1])
                if float(numbers[0].strip()) > float(numbers[1].strip()):
                    #print("Result: True")
                    return True
                else:
                    #print("Result: False")
                    return False
                
            if '<' in parts:
                numbers = parts.split('<')
                #print("Comparing:", numbers[0], "<", numbers[1])
                if float(numbers[0].strip()) < float(numbers[1].strip()):
                    #print("Result: True")
                    return True
                else:
                    #print("Result: False")
                    return False
                
            else:
                return 'ERROR'
            
def main():
            error = False
            output = False
            ifState = False
            comment = False
            lineNumber = 0
            text = ''
            num = 0

            try:
                print("Starting main function")
                # Existing code for the main function
                with open('testcode.txt', 'r') as file:
                    for line in file:
                        print("Line Read:", line.strip())
                        lexer = Lexer(line)
                        print("Processing Tokens in the Line")

                        while True:
                            token = lexer.getNextToken()
                            print("Token:", token.type, token.value) #Can Comment Out if You Don't Want to Print Tokens
                            if token.type == 'COMMENT':
                                comment = True
                                break

                            elif token.type == 'ERROR':
                                print('Line', lineNumber, 'Includes an Error. Incorrect Character.')
                                break
                            
                            if error == True:
                                continue

                            if token.type == 'IF':
                                ifState = True
                                text = line.split('if', 1)[1].strip()  # Extract the text after "IF"
                                print("Text after IF:", text)

                            if ifState:
                                result = ifStatement(text)
                                if result == 'ERROR':
                                    print('Line', lineNumber, 'Includes an Error. Incorrect If Statement.')
                                elif not result:
                                    ifState = False  # Reset ifState
                                else:
                                    print("Code Block:", result)
                                    ifState = False  # Reset ifState
                            
                            if token.type == 'PRINT' and token.value == 'print':
                                expression = lexer.code.split('(')[1].split(')')[0].strip()
                                print("Expression to be Calculated:", expression)
                                result = calculate(expression)
                                print("Result of the expression:", result)

                            # Existing code for processing tokens
                            if token.type == "End of File":
                                break
                    
                        print("-------------------------")
                        #lexer.position = 0
                        #lexer.currentCharacter = lexer.code[lexer.position]
            except Exception as e:
                print("An ERROR Occurred:", e)

if __name__ == "__main__":
    main()

            