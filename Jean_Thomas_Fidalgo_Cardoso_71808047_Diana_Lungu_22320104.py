#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Timothée Bernard (timothee.bernard@u-paris.fr)

import random


class CFGRule:
    # lhs: str
    # rhs: list[str]
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    # Returns a string representation of the object. Used to print the object in a nice way.
    # Output: str
    def __str__(self):
        return f"{self.lhs} -> {self.rhs}"

    # Returns a string representation of the object. Used to print the object in a nice way.
    # Output: str
    def __repr__(self):
        return self.__str__()


class CFG:
    # rules: list[CFGRule]
    # axiom: str
    def __init__(self, rules, axiom):
        self.rules = rules
        self.axiom = axiom

        # Determine the set of terminal and the set of non-terminal symbols in the grammar.
        # A symbol is considered to be a non-terminal symbol if it appears in the left-hand side of a rule, otherwise it is a non-terminal symbol
        self.lhs_to_rules = {}  # dict[str, list[CFGRule]]
        self.non_terminals = set()  # set[str]

        """ TODO 2.1 and 2.2 """
        for rule in rules:
            self.non_terminals.add(rule.lhs)
            # get the value of the non_terminal symbol key and append the rule to it,
            # if the non_terminal symbol is not in the dict, set: key = non terminal symbol and value = empty list
            self.lhs_to_rules.setdefault(rule.lhs, []).append(rule)

        self.terminals = set()  # set[str]
        for rule in rules:
            # s: symbol in right hand side
            for s in rule.rhs:
                if s not in self.non_terminals:
                    self.terminals.add(s)

    # sym: bool
    # Output: bool
    def isTerminal(self, sym):
        return (sym in self.terminals)

    # sym: bool
    # Output: bool
    def isNonTerminal(self, sym):
        return (sym in self.non_terminals)

    # Generates a tree obtained by starting from a single node labelled with the axiom, and then expanding all leaves labelled with a non-terminal symbol using a rule of the grammar, until all leaves are labelled with a terminal symbol.
    # Output: Tree
    def generate(self):
        tree = Tree(label=self.axiom)  # Modified below.

        stack = [tree]  # A list of nodes that might need rewritting. Is used below in a last in, first out (LIFO) way.
        while (len(stack) > 0):
            node = stack.pop()  # Removes and returns the last node of the stack.

            if (self.isTerminal(node.label)): continue  # Terminal nodes do not need rewritting.
            assert self.isNonTerminal(node.label), f"Unknown symbol: {node.label}"

            # Selects a rule.
            rules = self.lhs_to_rules[node.label]  # list[CFGRule]
            rule = random.choice(rules)  # CFGRule

            # Applies the rule.
            node.children = [Tree(label=sym) for sym in rule.rhs]
            stack.extend(reversed(
                node.children))  # `reversed` is optional, but it ensures that the tree is generated from left to right (given that `stack` is used in a LIFO way).

            """ TODO 2.4 """
            # print the current state of the text
            tokens = tree.get_yield()
            print("processing ...", join_tokens(tokens))

        # input(tree) # Useful to observe how the tree is generated.

        return tree

    # Returns a string representation of the object. Used to print the object in a nice way.
    # Output: str
    def __str__(self):
        return f"CFG({self.terminals}, {self.non_terminals}, {self.rules}, {self.axiom})"

    # Returns a string representation of the object. Used to print the object in a nice way.
    # Output: str
    def __repr__(self):
        return self.__str__()


class Tree:
    # label: str
    # children: list[Tree]
    def __init__(self, label, children=[]):
        self.label = label
        self.children = children

    # Output: list[str]
    def get_yield(self):
        l = []  # list[str]
        self.get_yield_aux(prefix=l)  # Modifies l.

        return l

    # This function returns None but modifies `prefix`.
    # prefix: list[str]
    def get_yield_aux(self, prefix):
        if (len(self.children) == 0):  # The node is a leaf, its label is a token.
            prefix.append(self.label)
        else:  # The node is an internal node, its label is a syntactic category.
            for child in self.children: child.get_yield_aux(prefix)

    # Returns a string representation of the object. Used to print the object in a nice way.
    # Output: str
    def __str__(self):
        l = []  # list[str]
        self.str_aux(l)

        return " ".join(l)

    # Returns None but modifies `l`.
    # l: list[str]
    def str_aux(self, l):
        if (len(self.children) == 0):  # The node is a leaf.
            l.append(self.label)
        else:  # The node is an internal node.
            l.extend(["[", self.label])
            for child in self.children: child.str_aux(l)
            l.append("]")


# Turns pieces of text into a single text.
# tokens: list[str]
# Output: str
def join_tokens(tokens):
    l = []  # list["str"]

    for i, token in enumerate(tokens):
        if (token == ""): continue

        if ((i > 0) and (token[0] not in set([".", "?", ",", ":", " "]))): l.append(" ")
        l.append(token)

    return "".join(l)


tokens = ["My", "name", "is", "Bond", ",", "James", "Bond", "."]
print(tokens)
print(join_tokens(tokens))
print()

""" TODO 2.3 """
# A toy grammar for simple sentences.
# Terminal symbols are words.
# Non-terminal symbols are syntactic categories and part-of-speeches.
toy_grammar_rules = [
    # Minimal set of rules.
    CFGRule(lhs="S", rhs=["AFFIRMATION", "."]),
    CFGRule(lhs="AFFIRMATION", rhs=["NP", "VP"]),
    CFGRule(lhs="AFFIRMATION", rhs=["NP", "VP", "NP"]),
    CFGRule(lhs="AFFIRMATION", rhs=["THATP", "THATP", "NP", "VP"]),

    CFGRule(lhs="S", rhs=["QUESTION", " ?"]),
    CFGRule(lhs="QUESTION", rhs=["AUX", "NP", "VP", "NP"]),
    CFGRule(lhs="QUESTION", rhs=["AUX", "THATP", "NP", "VP", "NP"]),
    CFGRule(lhs="AUX", rhs=["Does"]),

    CFGRule(lhs="THATP", rhs=["NP", "VP", "Ti"]),
    CFGRule(lhs="Ti", rhs=["that"]),

    CFGRule(lhs="NP", rhs=["Jamy"]),
    CFGRule(lhs="NP", rhs=["Sabine"]),

    CFGRule(lhs="VP", rhs=["Vi"]),
    CFGRule(lhs="Vi", rhs=["reads"]),
    CFGRule(lhs="Vi", rhs=["hears"]),
    CFGRule(lhs="Vi", rhs=["hear"]),
    CFGRule(lhs="Vi", rhs=["believes"]),
    CFGRule(lhs="Vi", rhs=["think"]),
    CFGRule(lhs="Vi", rhs=["writes"]),
]

g = CFG(rules=toy_grammar_rules, axiom="S")
print("grammar:", g)

print()
for _ in range(3):
    tree = g.generate()
    print("sampled tree:", tree)
    tokens = tree.get_yield()
    print("yield:", tokens)
    text = join_tokens(tokens)
    print("text:", text)
    print()

print()

# A grammar for weather reports.
# Terminal symbols are parts of sentences.
# Non-terminal symbols are syntactico-semantic labels.
# There is a bit of recursion due to "L2-PLACE".
# For inspiration, see https://www.meteoblue.com/en/weather/week/paris_france_2988507
""" TODO 2.5 """
weather_grammar_rules = [
    CFGRule(lhs="FORECAST", rhs=["INTRO", "WEATHER_S", "AIR_S", "WIND_S", "FAREWELL"]),


    # INTRO: Sentence to introduce the forecast
    CFGRule(lhs="INTRO", rhs=["Weather forecast for", "DATE_P", "."]),

    CFGRule(lhs="DATE_P", rhs=["DATE"]),
    CFGRule(lhs="DATE_P", rhs=["next", "DAY_OF_WEEK"]),
    CFGRule(lhs="DATE_P", rhs=["next", "TIME_WORD"]),

    CFGRule(lhs="DATE", rhs=["today"]),
    CFGRule(lhs="DATE", rhs=["tomorrow"]),

    CFGRule(lhs="DAY_OF_WEEK", rhs=["Monday"]),
    CFGRule(lhs="DAY_OF_WEEK", rhs=["Tuesday"]),
    CFGRule(lhs="DAY_OF_WEEK", rhs=["Wednesday"]),
    CFGRule(lhs="DAY_OF_WEEK", rhs=["Thursday"]),
    CFGRule(lhs="DAY_OF_WEEK", rhs=["Friday"]),
    CFGRule(lhs="DAY_OF_WEEK", rhs=["Saturday"]),
    CFGRule(lhs="DAY_OF_WEEK", rhs=["Sunday"]),

    CFGRule(lhs="TIME_WORD", rhs=["month"]),
    CFGRule(lhs="TIME_WORD", rhs=["year"]),
    CFGRule(lhs="TIME_WORD", rhs=["summer"]),
    CFGRule(lhs="TIME_WORD", rhs=["winter"]),
    CFGRule(lhs="TIME_WORD", rhs=["autumn"]),
    CFGRule(lhs="TIME_WORD", rhs=["spring"]),
    CFGRule(lhs="TIME_WORD", rhs=["Christmas"]),
    CFGRule(lhs="TIME_WORD", rhs=["Easter"]),


    # WEATHER_S: sentence describing the conditions of the weather and mentioning the city
    CFGRule(lhs="WEATHER_S", rhs=["TIME", ",", "EXPECTED_WEATHER_1", "."]),
    CFGRule(lhs="WEATHER_S", rhs=["TIME",",", "in", "CITY", "and", "CITY", "," , "EXPECTED_WEATHER_2", "."]),

    CFGRule(lhs="TIME", rhs=["In the morning"]),
    CFGRule(lhs="TIME", rhs=["In the afternoon"]),
    CFGRule(lhs="TIME", rhs=["During the night"]),

    # WEATHER_TYPE_IS and WEATHER_TYPE_ARE created to have the right conjugation of the verb "to be"
    CFGRule(lhs="EXPECTED_WEATHER_1", rhs=["WEATHER_TYPE_IS", "is expected in", "CITY"]),
    CFGRule(lhs="EXPECTED_WEATHER_1", rhs=["WEATHER_TYPE_ARE", "are expected in", "CITY"]),

    # 2 different types of EXPECTED_WEATHER to handle 2 different phrase constructions
    CFGRule(lhs="EXPECTED_WEATHER_2", rhs=["WEATHER_TYPE_IS", "is expected but the weather will be", "WEATHER_ADJ"]),
    CFGRule(lhs="EXPECTED_WEATHER_2", rhs=["WEATHER_TYPE_ARE", "are expected but the weather will be", "WEATHER_ADJ"]),

    CFGRule(lhs="WEATHER_TYPE_IS", rhs=["light rain"]),
    CFGRule(lhs="WEATHER_TYPE_IS", rhs=["heavy rain"]),
    CFGRule(lhs="WEATHER_TYPE_IS", rhs=["light snow"]),
    CFGRule(lhs="WEATHER_TYPE_IS", rhs=["heavy snow"]),

    CFGRule(lhs="WEATHER_TYPE_ARE", rhs=["a fair bit of clouds"]),
    CFGRule(lhs="WEATHER_TYPE_ARE", rhs=["a lot of clouds"]),

    CFGRule(lhs="CITY", rhs=["Toulouse"]),
    CFGRule(lhs="CITY", rhs=["Paris"]),
    CFGRule(lhs="CITY", rhs=["Marseille"]),
    CFGRule(lhs="CITY", rhs=["Montpellier"]),
    CFGRule(lhs="CITY", rhs=["Lyon"]),
    CFGRule(lhs="CITY", rhs=["Lisbon"]),   
    CFGRule(lhs="CITY", rhs=["Mumbai"]),
    CFGRule(lhs="CITY", rhs=["Atlanta"]),
    CFGRule(lhs="CITY", rhs=["Carcavelos"]), 
    CFGRule(lhs="CITY", rhs=["Barcelona"]), 
    CFGRule(lhs="CITY", rhs=["Seoul"]), 
    CFGRule(lhs="CITY", rhs=["Moscow"]),
    CFGRule(lhs="CITY", rhs=["Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch"]),  
    CFGRule(lhs="CITY", rhs=["Maputo"]),  
    CFGRule(lhs="CITY", rhs=["Luanda"]),  
    CFGRule(lhs="CITY", rhs=["Gincho"]),  
    CFGRule(lhs="CITY", rhs=["Algarve"]),

    CFGRule(lhs="WEATHER_ADJ", rhs=["sunny"]),
    CFGRule(lhs="WEATHER_ADJ", rhs=["cloudy"]),  
    CFGRule(lhs="WEATHER_ADJ", rhs=["rainy"]),  
    CFGRule(lhs="WEATHER_ADJ", rhs=["nice"]),  
    CFGRule(lhs="WEATHER_ADJ", rhs=["stable"]),  
    CFGRule(lhs="WEATHER_ADJ", rhs=["cold"]),
    CFGRule(lhs="WEATHER_ADJ", rhs=["warm"]),   
    CFGRule(lhs="WEATHER_ADJ", rhs=["good"]),
    CFGRule(lhs="WEATHER_ADJ", rhs=["dry"]), 
    CFGRule(lhs="WEATHER_ADJ", rhs=["humid"]),


    # AIR_S: sentence describing the conditions of the air
    CFGRule(lhs="AIR_S", rhs=["AIR", "is noticeable", "AIR_SPEED", "."]),

    CFGRule(lhs="AIR", rhs=["Light air"]),
    CFGRule(lhs="AIR", rhs=["A gentle breeze"]),
    CFGRule(lhs="AIR", rhs=["Polluted air"]),
    CFGRule(lhs="AIR", rhs=["Contaminated air"]),

    CFGRule(lhs="AIR_SPEED", rhs=["(1 to 7 km/h)"]),
    CFGRule(lhs="AIR_SPEED", rhs=["(12 to 20 km/h)"]),
    CFGRule(lhs="AIR_SPEED", rhs=["(20 to 30 km/h)"]),


    # WIND_S: sentence describing the conditions of the wind
    CFGRule(lhs="WIND_S", rhs=["Winds blowing from", "WIND_DIRECTION", "."]),

    CFGRule(lhs="WIND_DIRECTION", rhs=["North"]),
    CFGRule(lhs="WIND_DIRECTION", rhs=["South"]),
    CFGRule(lhs="WIND_DIRECTION", rhs=["East"]),
    CFGRule(lhs="WIND_DIRECTION", rhs=["West"]),
    CFGRule(lhs="WIND_DIRECTION", rhs=["Southwest"]),
    CFGRule(lhs="WIND_DIRECTION", rhs=["Southeast"]),
    CFGRule(lhs="WIND_DIRECTION", rhs=["Northeast"]),
    CFGRule(lhs="WIND_DIRECTION", rhs=["Northwest"]),


    # FAREWELL: sentence to bid farewell
    CFGRule(lhs="FAREWELL", rhs=["Have a", "DAY_ADJ", "DAY", "!"]),

    CFGRule(lhs="DAY_ADJ", rhs=["nice"]),
    CFGRule(lhs="DAY_ADJ", rhs=["lovely"]),
    CFGRule(lhs="DAY_ADJ", rhs=["terrific"]),
    CFGRule(lhs="DAY_ADJ", rhs=["superb"]),
    CFGRule(lhs="DAY_ADJ", rhs=["wonderful"]),

    CFGRule(lhs="DAY", rhs=["day"]),
    CFGRule(lhs="DAY", rhs=["evening"]),
    CFGRule(lhs="DAY", rhs=["afternoon"]),
    CFGRule(lhs="DAY", rhs=["morning"]),            
]

g = CFG(rules=weather_grammar_rules, axiom="FORECAST")
print("grammar:", g)

print()
for _ in range(3):
    tree = g.generate()
    print("sampled tree:", tree)
    tokens = tree.get_yield()
    print("yield:", tokens)
    text = join_tokens(tokens)
    print("text:", text)
    print()

print()