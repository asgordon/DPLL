# DPLL : Boolean satisfiability for propositional logic in Python
Andrew S. Gordon
June & September 2015 

I was the co-instructor of the big masters-level Artificial Intelligence course in the Spring of 2015 at the University of Southern California, for eight lectures on formal logic. For their logic programming assignment, I had all 352 students convert propositional logic sentences into conjunctive normal form, then determine their satisfiability using the DPLL algorithm. In order to make sure the programming assignment was feasible, I wrote my own solution in Python. My solution was certainly not the best among those that were submitted, but I have a certain sympathy for the code I wrote. 

After the course was over, I wrote a simple parser so that I could apply my code to the LISP-style notation that I preferred. It was a great learning exercise for me, as I had never worked with LEX and YACC before, and needed to learn it for another project I was working on. With the parser in front, I then had a handy tool that I could use to quickly check the satisfiability of any propositional formula. Later that year, I realized that constructing parser compilers was overkill for what needed, and replaced the parser with a much simpler version.

Example 1:

    > echo "(and (if P Q) P (not Q))" | python propparse.py | python cnf.py | python dpll.py
    False

Example 2:

    cat tests.lisp | python propparse.py | python cnf.py | python dpll.py

    cat tests.lisp |   	# lisp style, multiple sentences, ;;; comments
    python propparse.py | 	# construct list of sentences in list format
    python cnf.py |    	# convert sentences into conjunctive normal form
    python dpll.py      	# find satisfying truth values for each sentence


## Representing propositional logic as nested lists in Python:

The standard notation for propositional logic is not the easiest for computers to process. Sure, we can find the unicode characters for all of the special symbols, but we probably do not want to operate directly on unicode-encoded strings for automated reasoning. Instead, we can represent sentences in propositional logic using nested lists.

Traditional notation:

     ¬R ⋀ B ⇒ W

List representation (Python-style):

     ["if", ["and", ["not", "R"], "B"], "W"]

This is convenient, especially if your program is reading strings from stdin or from a file. In Python, you can convert a string that is formatted to look like a list into an actual list by calling the eval function on it.

    >>> mystring = '["if", ["and", ["not", "R"], "B"], "W"]'
    >>> mylist = eval(mystring)
    >>> mylist
    ['if', ['and', ['not', 'R'], 'B'], 'W']
    >>> len(mystring)
    39
    >>> len(mylist)
    3

An atomic sentence can be represented as a string.

     "R"

A complex sentence is a list, where the element in the first position is string that denotes a logical connective, and all remaining elements are either atomic sentences or complex sentences.

     ["not", "R"]

     ["and", ["or", "P", "Q", "R"], ["not", "S"]]

     ["iff", "S", ["and", "Q", "R"]]

In this format, let's write propositional symbols as strings beginning with an uppercase letter, and connectives in lowercase. There are only five connectives, so the first element of EVERY list must be one of these strings:

* "not"		negation
* "and"		conjunction
* "or"		disjunction
* "if"		implication
* "iff"		biconditional implication




