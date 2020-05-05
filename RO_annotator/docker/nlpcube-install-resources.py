from cube.api import Cube

cube = Cube(verbose=True)
cube.load(
    'ro', tokenization=True,
    compound_word_expanding=False,
    tagging=True,
    lemmatization=True,
    parsing=True
)
