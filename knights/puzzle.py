from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    
    # A is either Knight or Knave but not both
    Biconditional(AKnight, Not(AKnave)),
    
    # If A is knight/knave
    Implication(AKnight, And(AKnight, AKnave)),  
    Implication(AKnave, Not(And(AKnight, AKnave))) 
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    
    # A is either Knight or Knave but not both
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    
    # If A is knight/knave
    Implication(AKnight, And(AKnave, BKnave)), 
    Implication(AKnave, Not(And(AKnave, BKnave))) 
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
     
    # A/B is either Knight or Knave but not both
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    
    # If A is knight/knave
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), 
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),  
    
    # If B is knight/knave
    Implication(BKnight, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),  
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave))),   
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
     
    # A/B/C is either Knight or Knave but not both
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),
    
    # Either of the 2 implications is true
    Or(
        And(Implication(AKnight, AKnight), Implication(AKnave, Not(AKnight))),
        And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))
    ), 
    
    # If B is knight/knave
    Implication(
        BKnight, And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))
    ),  
    Implication(
        BKnave, Not(And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave))))
    ),  
    
    # If B is knight/knave
    Implication(BKnight, CKnave),   
    Implication(BKnave, Not(CKnave)),  
    
    # If C is knight/knave
    Implication(CKnight, AKnight),  
    Implication(CKnave, Not(AKnight))  
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
