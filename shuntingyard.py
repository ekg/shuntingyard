#!/usr/bin/python

import sys

boolean_true = "T"
boolean_false = "F"

operator_gt = "+"
operator_lt = "-"
operator_eq = "="
operator_and = "&"
operator_or = "|"
operator_not = "!"
operator_left_paran = "("
operator_right_paran = ")"

operator_association = {
    operator_gt: "left",
    operator_lt: "left",
    operator_eq: "left",
    operator_and: "left",
    operator_or: "left",
    operator_not: "right"
}

operator_precedence = {
    operator_not: 4,
    operator_gt: 3,
    operator_lt: 3,
    operator_eq: 2,
    operator_and: 1,
    operator_or: 0,
    operator_left_paran: -1,
    operator_right_paran: -1
}

def precedence(op):
    return operator_precedence[op]

def associativity(op):
    return operator_association[op]

def is_boolean(c):
    return c == boolean_true or c == boolean_false

def is_op(c):
    return operator_precedence.has_key(c) and not (is_left_paran(c) or is_right_paran(c))

def is_left_paran(c):
    return c == operator_left_paran

def is_right_paran(c):
    return c == operator_right_paran

def append_token(token, l):
    if token != "":
        l.append(token)
    return ""

def tokenize(expr):
    tokens = []
    last_token = ""
    in_token = False
    for c in expr:
        if c == " ":
            in_token = False
            last_token = append_token(last_token, tokens)
            continue
        elif is_op(c) or is_right_paran(c) or is_left_paran(c):
            in_token = False
            last_token = append_token(last_token, tokens)
            tokens.append(c)
        else:
            in_token = True
            last_token += c
        if not in_token and last_token != "":
            last_token = append_token(last_token, tokens)
    if in_token:
        append_token(last_token, tokens)
    return tokens

# notes are taken from http://en.wikipedia.org/wiki/Shunting_yard_algorithm
def infix_to_prefix(expr):
    """converts the infix expression to prefix using the shunting yard algorithm"""
    ops = []
    results = []
    for token in tokenize(expr):
        #print ops, results
        if is_op(token):
            #If the token is an operator, o1, then:
            #while there is an operator token, o2, at the top of the stack, and
            #either o1 is left-associative and its precedence is less than or equal to that of o2,
            #or o1 is right-associative and its precedence is less than that of o2,
            #pop o2 off the stack, onto the output queue;
            #push o1 onto the stack.
            while len(ops) > 0 and is_op(ops[-1]) and \
                    ( (associativity(token) == 'left' and precedence(token) <= precedence(ops[-1])) \
                 or   (associativity(token) == 'right' and precedence(token) < precedence(ops[-1])) ):
                results.append(ops.pop())
            ops.append(token)
        #If the token is a left parenthesis, then push it onto the stack.
        elif is_left_paran(token):
            ops.append(token)
        #If the token is a right parenthesis:
        elif is_right_paran(token):
            #Until the token at the top of the stack is a left parenthesis, pop operators off the stack onto the output queue.
            while len(ops) > 0 and not is_left_paran(ops[-1]):
                results.append(ops.pop())
            #Pop the left parenthesis from the stack, but not onto the output queue.
            #If the stack runs out without finding a left parenthesis, then there are mismatched parentheses.
            if len(ops) == 0:
                print "error: mismatched parentheses"
                exit()
            if is_left_paran(ops[-1]):
                ops.pop()
        else:
        #If the token is a number, then add it to the output queue.
            results.append(token)
    #When there are no more tokens to read:
    #While there are still operator tokens in the stack:
    while len(ops) > 0:
        #If the operator token on the top of the stack is a parenthesis, then there are mismatched parentheses.
        if is_right_paran(ops[-1]) or is_left_paran(ops[-1]):
            print "error: mismatched parentheses"
            exit()
        #Pop the operator onto the output queue.
        results.append(ops.pop())

    return results

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "usage", sys.argv[0], "\"infix boolean expression\""
        print "e.g. \"( true & false | ( true & ! true ) )\""
        exit()
    print ' '.join(infix_to_prefix(sys.argv[1]))
