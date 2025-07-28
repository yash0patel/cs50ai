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
    # A is either Knight or Knave, but not both
    Biconditional(AKnight, Not(AKnave)),

    # A : "I am both a Knight and a Knave"
    Biconditional(AKnight, And(AKnight, AKnave))
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Each character either Knight or Knave, but not both
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),

    # A : "both Knaves"
    Biconditional(AKnight, And(AKnave, BKnave))
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Each character either Knight or Knave, but not both
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),

    # A : (both Knight or both Knave)
    Biconditional(AKnight,
                  Or(And(AKnight, BKnight), And(AKnave, BKnave))),

    # B : (one Knight, one Knave)
    Biconditional(BKnight,
                  Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
# Extra speech variable
A_said_knave = Symbol("A said 'I am a Knave'")

knowledge3 = And(
    # Exclusivity: each character is exactly one of knight/knave
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),

    # A actually said one statement, we track it with A_said_knave
    # If A_said_knave is true, then A's statement was "I am a Knave"
    # If false, then it was "I am a Knight"
    Or(A_said_knave, Not(A_said_knave)),  # tautology just to include symbol

    # If A said "I am a Knave"
    Implication(A_said_knave, And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),

    # If A said "I am a Knight"
    Implication(Not(A_said_knave),
                And(Implication(AKnight, AKnight), Implication(AKnave, Not(AKnight)))),

    # B says: "A said 'I am a Knave'" → if B is Knight → A_said_knave true
    Biconditional(BKnight, A_said_knave),

    # B says: "C is a Knave"
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # C says: "A is a Knight"
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
