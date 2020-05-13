import random
from enum import Enum
from itertools import chain, combinations

"""
This file contains code for solving the satisfiability problem for the following
fragment of propositional logic.

A ::= p | p and A | -p and A | p or A | -p or A

where - denotes negation and p is a propositional symbol. Below we will
use the notation '&' for 'and' and '|' for 'or'.

For this fragment the satisfiability problem can be solved in linear time.
"""

class PropositionalType(Enum):
	PROPOSITION = 0
	NEGATEDPROPOSITION = 1
	CONJUNCTION = 2
	DISJUNCTION = 3

class Sentence(object):
	def __init__(self, type, subformulas):
		self.type = type
		self.subformulas = subformulas

	def __str__(self):
		if self.type is PropositionalType.PROPOSITION:
			return self.subformulas[0]
		elif self.type is PropositionalType.NEGATEDPROPOSITION:
			return '-' + self.subformulas[0]
		elif self.type is PropositionalType.CONJUNCTION:
			return '(' + str(self.subformulas[0]) + '&' + str(self.subformulas[1]) + ')'
		else:
			return '(' + str(self.subformulas[0]) + '|' + str(self.subformulas[1]) + ')'

def randomSentence(vocabulary, depth):
	if depth == 0:
		type = random.choice([0,1])
		if type == 0:
			return Sentence(PropositionalType.PROPOSITION, random.choice(vocabulary))
		else:
			return Sentence(PropositionalType.NEGATEDPROPOSITION, random.choice(vocabulary))
	else:
		type = random.choice([0,1])
		if type == 0:
			return Sentence(PropositionalType.CONJUNCTION, [randomSentence(vocabulary, 0), randomSentence(vocabulary, depth - 1)])
		else:
			return Sentence(PropositionalType.DISJUNCTION, [randomSentence(vocabulary, 0), randomSentence(vocabulary, depth - 1)])

def SAT(sentence, constraints):
	if sentence.type == PropositionalType.PROPOSITION:
		if not sentence.subformulas[0] in constraints[1]:
			return set(sentence.subformulas[0])
		else:
			return None
	
	if sentence.type == PropositionalType.NEGATEDPROPOSITION:
		if sentence.subformulas[0] in constraints[0]:
			return None
		else:
			return set()

	if sentence.type == PropositionalType.CONJUNCTION:
		constraint = sentence.subformulas[0]
		if SAT(constraint, constraints) is None:
			return None
		
		if constraint.type == PropositionalType.PROPOSITION:
			constraints[0] = constraints[0] | set(constraint.subformulas[0])
			result = SAT(sentence.subformulas[1], constraints)
			if result is None:
				return None
			else:
				return result | set(constraint.subformulas[0])
		else:
			constraints[1] = constraints[1] | set(constraint.subformulas[0])
			return SAT(sentence.subformulas[1], constraints)

	if sentence.type == PropositionalType.DISJUNCTION:
		constraint = sentence.subformulas[0]
		result = SAT(constraint, constraints)
		if not result is None:
			return result
		
		if constraint.type == PropositionalType.PROPOSITION:
			constraints[1] = constraints[1] | set(constraint.subformulas[0])
		else:
			constraints[0] = constraints[0] | set(constraint.subformulas[0])

		return SAT(sentence.subformulas[1], constraints)


def evaluate(sentence, valuation):
	if sentence.type == PropositionalType.PROPOSITION:
		if sentence.subformulas[0] in valuation:
			return 1
		else:
			return 0
	elif sentence.type == PropositionalType.NEGATEDPROPOSITION:
		if sentence.subformulas[0] in valuation:
			return 0
		else:
			return 1
	elif sentence.type == PropositionalType.CONJUNCTION:
		return (evaluate(sentence.subformulas[0], valuation) * evaluate(sentence.subformulas[1],valuation))
	else:
		return max((evaluate(sentence.subformulas[0], valuation), (evaluate(sentence.subformulas[1], valuation))))

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def satisfiable(sentence, vocabulary):
	valuations = powerset(vocabulary)
	for v in valuations:
		if evaluate(sentence, set(v)) == 1:
			return set(v)
	return None

# For applying the algorithm for random sentences.
for i in range(1000):
	depth = random.randint(0,10)
	rndSentence = randomSentence(['o','p','q','r','s','t','u','v','w','x','y','z'], depth)
	valuation = SAT(rndSentence, [set(), set()])
	
	print(rndSentence)
	print(f'Result for the algorithm {valuation}')

	# FOR DEBUGGING.
	#if not valuation is None:
	#	evaluation = evaluate(rndSentence, valuation)
	#
	#result = satisfiable(rndSentence, ['o','p','q','r','s','t','u','v','w','x','y','z'])
	#if not valuation is None:
	#	print(f'Was the given assignment satisfying: {evaluation}')
	#print(f'Correct answer: {result}')
	
	print()
