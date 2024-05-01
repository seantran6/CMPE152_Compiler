import re

# Define tokens
TOKENS = [
    ('KEYWORD', r'if|else|while|for|def'),  # Example keywords
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Variable names, function names
    ('PUNCTUATION', r'[\(\)\{\}\[\];:,]'),  # Parentheses, braces, semicolons, colons
    ('OPERATOR', r'[+\-*/%=<>]'),  # Arithmetic, comparison operators
    ('LITERAL', r'\d+'),  # Integer literals
    ('WHITESPACE', r'\s+'),  # Whitespace
    ('UNKNOWN', r'.'),  # Any other character
]

# Lexer
def lexer(code):
    tokens = []
    for token in TOKENS:
        name, pattern = token
        regex = re.compile(pattern)
        match = regex.match(code)
        if match:
            value = match.group(0)
            tokens.append((name, value))
            code = code[len(value):].strip()
    return tokens

# Parser
def parse(tokens):
    instructions = []
    for token in tokens:
        if token[0] == 'LABEL':
            label = token[1][:-1]  # Remove ':' from label
            instructions.append(('LABEL', label))
        elif token[0] == 'INSTRUCTION':
            instruction = token[1]
            operands = []
            while tokens and tokens[0][0] not in ['LABEL', 'INSTRUCTION']:
                operands.append(tokens.pop(0)[1])
            instructions.append((instruction, operands))
    return instructions

# Example assembly code
assembly_code = """
LOOP:
    MOV R1, 10
    MOV R2, 20
    ADD R3, R1, R2
    JMP LOOP
"""

# Tokenize and parse assembly code
tokens = lexer(assembly_code)
instructions = parse(tokens)
print(instructions) 