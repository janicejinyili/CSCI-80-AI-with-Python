import nltk
#nltk.download('punkt')
import sys
import string 

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
S -> SS | SS Conj SS
SS -> CNP CVP | PP CNP CVP
CNP -> NP Conj NP | NP
AdjP -> Adj | Adj Adj | Adj Adj Adj
NP -> N | Det N | AdjP N | Det AdjP N | N Adv | Det N Adv | AdjP N Adv| Det AdjP N Adv
AVP -> Adv V | V Adv | V
VP -> AVP | AVP CNP | AVP P | AVP PP
CVP -> VP | VP Conj VP | VP PP | VP PP Conj VP PP | VP Conj VP PP | VP PP Conj VP
PP -> P CNP | P CNP P CNP
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

    #Tokenize the sentence, remove punctuation & non-letter words and convert all to lowercase
    tokens = nltk.tokenize.word_tokenize(sentence)
    tokens_list = [t.lower().translate(str.maketrans('', '', string.punctuation)) for t in tokens if any(l.isalpha() for l in t)]
    return tokens_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.

    search nltk tree and find subtree
    only have to look for one level down, nothing recursive
    """

    # Return the subtree with label == NP while not containing other NPs
    np = [t for t in tree.subtrees() if t.label() == 'NP' and not any(p.label() == 'NP' and p != t for p in t.subtrees())]
    return np


if __name__ == "__main__":
    main()
