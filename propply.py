# propply.py
# Tokenizer and parser for propositional logic using PLY
# Andrew Gordon
# June 19, 2015

### Part 1. The tokenizer

import ply.lex as lex
import fileinput 

# Reserved words
reserved = {
    'and'    : 'AND',
    'or'     : 'OR',
    'iff'    : 'IFF',
    'if'     : 'IF',
    'not'    : 'NOT' #,
#    'forall' : 'FORALL', # FOL
#    'exists' : 'EXISTS'  # FOL
}

# List of token names
tokens = [#'COMMENT',
          'OPEN',
          'CLOSE',
#          'NUMBER',
        'NAME'] + list(reserved.values())

# Regular expressions rules for simple tokens
t_OPEN =  r'\('
t_CLOSE = r'\)'

# Regular rules with some action code
def t_NUMBER(t):
    #r'\d+' # ints only
    r'\d*\.?\d+' # floats okay
    t.value = float(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_\']*'
    t.type = reserved.get(t.value, 'NAME') # check for reserved words
    return t

def t_COMMENT(t):
    r'\;.*'
    pass # No return value. Token discarded

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Warning: Skipping illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# build the tokenizer
lexer = lex.lex()

##### Part 2. The parser

import ply.yacc as yacc

def p_list(p):
    '''
    list : list sentence
    list : sentence
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[2])

def p_and(p):
    'sentence : OPEN AND list CLOSE'
    p[0] = ['and'] + p[3]

def p_or(p):
    'sentence : OPEN OR list CLOSE'
    p[0] = ['or'] + p[3]

def p_name(p): 
    'sentence : NAME' #atomic sentence
    p[0] = p[1]

def p_if(p):
    'sentence : OPEN IF sentence sentence CLOSE'
    p[0] = ['if', p[3], p[4]]

def p_iff(p):
    'sentence : OPEN IFF sentence sentence CLOSE'
    p[0] = ['iff', p[3], p[4]]

def p_not(p):
    'sentence : OPEN NOT sentence CLOSE'
    p[0] = ['not', p[3]]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

#parser = yacc.yacc()
parser = yacc.yacc(write_tables=False, debug=False)
#parser.parse(text,lexer=lexer)

# command line interface (for testing)
# > python follex.py < test.lisp
if __name__ == "__main__":
    intext = "".join(fileinput.input())
    outlist = parser.parse(intext)
    #print repr(outtext)
    for l in outlist:
        print repr(l)

