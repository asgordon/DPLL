# propparse.py
# Tokenizer and parser for propositional logic
# Adapted from Peter Norvig's lisp parser 
# Andrew S. Gordon
# September 10, 2015

import fileinput

def decomment(src):
    lines = src.split('\n')
    lines = [l.partition(';')[0] for l in lines]
    return " ".join(lines)

def tokenize(chars):
    return decomment(chars).replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program):
    return parse_multiple("(" + program + ")")

def parse_multiple(program):
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return token
    
# command line interface (for testing)
# > python propparse.py < tests.lisp
if __name__ == "__main__":
    intext = "".join(fileinput.input())
    outlist = parse(intext)
    #print repr(outtext)
    for l in outlist:
        print(repr(l))
