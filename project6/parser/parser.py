import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S

NP -> N
NP -> Det N
NP -> Det AP N
NP -> NP PP

AP -> Adj
AP -> Adj AP

VP -> V
VP -> V NP
VP -> V PP
VP -> V Adv
VP -> Adv VP
VP -> V NP PP

PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # split sentence into words/tokens
    words = nltk.word_tokenize(sentence)

    result = []

    for word in words:

        # convert word to lowercase
        word = word.lower()

        # keep word only if it contains a letter
        if any(char.isalpha() for char in word):
            result.append(word)

    return result


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    # check every subtree
    for subtree in tree.subtrees():

        # only look at noun phrases
        if subtree.label() == "NP":

            has_inner_np = False

            # look for nested noun phrases
            for child in subtree.subtrees():

                if child != subtree and child.label() == "NP":
                    has_inner_np = True
                    break

            # add NP if no smaller NP exists inside it
            if not has_inner_np:
                chunks.append(subtree)

    return chunks


if __name__ == "__main__":
    main()
