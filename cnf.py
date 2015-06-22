# Homework 2 solution, part 1: cnf.py
# Andrew Gordon
# Feb 18, 2015
# Revised June 19, 2015 for better input/output and implies->if

import sys
import fileinput

def biconditionalElimination(s):
    if type(s) is str:
        return s
    elif type(s) is list and s[0] == "iff":
        return(["and",
                ["if",
                 biconditionalElimination(s[1]),
                 biconditionalElimination(s[2])],
                ["if",
                 biconditionalElimination(s[2]),
                 biconditionalElimination(s[1])]])
    else:
        return([s[0]] + [biconditionalElimination(i) for i in s[1:]])

def implicationElimination(s):
    if type(s) is str:
        return s
    elif type(s) is list and s[0] == "if":
        return(["or",
                ["not",
                 implicationElimination(s[1])],
                implicationElimination(s[2])])
    else:
        return([s[0]] + [implicationElimination(i) for i in s[1:]])

def doubleNegationElimination(s):
    if type(s) is str:
        return s
    elif type(s) is list and s[0] == "not" and type(s[1]) is list and s[1][0] == "not":
        return(doubleNegationElimination(s[1][1]))
    else:
        return([s[0]] + [doubleNegationElimination(i) for i in s[1:]])

def demorgan(s):
    revision = demorgan1(s)
    if revision == s:
        return s
    else:
        return demorgan(revision)
    
def demorgan1(s):
    if type(s) is str:
        return s
    elif type(s) is list and s[0] == "not" and type(s[1]) is list and s[1][0] == "and":
        return(["or"] + [demorgan(["not", i]) for i in s[1][1:]])
    elif type(s) is list and s[0] == "not" and type(s[1]) is list and s[1][0] == "or":
        return(["and"] + [demorgan(["not", i]) for i in s[1][1:]])
    else:
        return ([s[0]] + [demorgan(i) for i in s[1:]])

def binaryize(s): # ensures all connectives are binary (and / or)
    if type(s) is str:
        return s
    elif type(s) is list and s[0] == "and" and len(s) > 3: # too long
        return(["and", s[1], binaryize(["and"] + s[2:])])
    elif type(s) is list and s[0] == "or" and len(s) > 3: # too long
        return(["or", s[1], binaryize(["or"] + s[2:])])
    else:
        return([s[0]] + [binaryize(i) for i in s[1:]])
    
def distributivity(s):
    revision = distributivity1(s)
    if revision == s:
        return s
    else:
        return distributivity(revision)
    
def distributivity1(s): # only works on binary connectives
    if type(s) is str:
        return s
    elif type(s) is list and s[0] == "or" and type(s[1]) is list and s[1][0] == "and":
        # distribute s[2] over s[1]
        return(["and"] + [distributivity(["or", i, s[2]]) for i in s[1][1:]])
    elif type(s) is list and s[0] == "or" and type(s[2]) is list and s[2][0] == "and":
        # distribute s[1] over s[2]
        return(["and"] + [distributivity(["or", i, s[1]]) for i in s[2][1:]])
    else:
        return ([s[0]] + [distributivity(i) for i in s[1:]])

def andAssociativity(s):
    revision = andAssociativity1(s)
    if revision == s:
        return s
    else:
        return andAssociativity(revision)
    
def andAssociativity1(s):
    if type(s) is str:
        return s
    elif type(s) is list and s[0] == "and":
        result = ["and"]
        # iterate through conjuncts looking for "and" lists
        for i in s[1:]:
            if type(i) is list and i[0] == "and":
                result = result + i[1:]
            else:
                result.append(i)
        return result
    else:
        return([s[0]] + [andAssociativity1(i) for i in s[1:]])

def orAssociativity(s):
    revision = orAssociativity1(s)
    if revision == s:
        return s
    else:
        return orAssociativity(revision)

def orAssociativity1(s):
    if type(s) is str:
        return s
    elif type(s) is list and s[0] == "or":
        result = ["or"]
        # iterate through disjuncts looking for "or" lists
        for i in s[1:]:
            if type(i) is list and i[0] == "or":
                result = result + i[1:]
            else:
                result.append(i)
        return result
    else:
        return([s[0]] + [orAssociativity1(i) for i in s[1:]])


def removeDuplicateLiterals(s):
    if type(s) is str:
        return s
    if s[0] == "not":
        return s
    if s[0] == "and":
        return(["and"] + [removeDuplicateLiterals(i) for i in s[1:]])
    if s[0] == "or":
        remains = []
        for l in s[1:]:
            if l not in remains:
                remains.append(l)
        if len(remains) == 1:
            return remains[0]
        else:
            return(["or"] + remains)

def removeDuplicateClauses(s):
    if type(s) is str:
        return s
    if s[0] == "not":
        return s
    if s[0] == "or":
        return s
    if s[0] == "and": #conjunction of clauses
        remains = []
        for c in s[1:]:
            if unique(c, remains):
                remains.append(c)
        if len(remains) == 1:
            return remains[0]
        else:
            return(["and"] + remains)

def unique(c, remains):
    for p in remains:
        if type(c) is str or type(p) is str:
            if c == p:
                return False
        elif len(c) == len(p):
            if len([i for i in c[1:] if i not in p[1:]]) == 0:
                return False
    return True
        

def cnf(s):
    s = biconditionalElimination(s)
    s = implicationElimination(s)
    s = demorgan(s)
    s = doubleNegationElimination(s)
    s = binaryize(s)
    s = distributivity(s)
    s = andAssociativity(s)
    s = orAssociativity(s)
    s = removeDuplicateLiterals(s)
    s = removeDuplicateClauses(s)
    return s

if __name__ == "__main__":

    sentences = fileinput.input()
    for l in sentences:
        print repr(cnf(eval(l.strip())))

