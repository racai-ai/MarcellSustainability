"""Contains all configuration variables for the NLPipe platform."""

import os

# Name of the configuration folder
_configFolderName = '.nlpipe'

# The DiacRestore.py model file
DIACMODELFILE = os.path.expanduser("~") + \
    os.sep + _configFolderName + \
    os.sep + "diac.model.newsty"

# Path to tbl.wordform.ro.v85 lexicon file
# Used by NLP-Cube to do better lemmatization
TBLWORDFORMFILE = os.path.expanduser("~") + \
    os.sep + _configFolderName + \
    os.sep + 'res' + os.sep + 'ro' + \
    os.sep + 'tbl.wordform.ro.v85'

# Used by NLP-Cube to map MSDs to CTAGs
CTAG2MSDMAPFILE = os.path.expanduser("~") + \
    os.sep + _configFolderName + \
    os.sep + 'res' + os.sep + 'ro' + \
    os.sep + 'msdtag.ro.map'

# Used by BioNER NLP-Cube instance
BIONERMODELNAME = os.path.expanduser("~") + \
    os.sep + _configFolderName + \
    os.sep + 'bioner' + os.sep + "ro" + \
    os.sep + 'tagger' + os.sep + 'bioro_skip.200.1.5'

BIONERWORDEMBEDFILE = os.path.expanduser("~") + \
    os.sep + _configFolderName + \
    os.sep + 'bioner' + os.sep + "ro" + \
    os.sep + 'embeddings' + os.sep + 'bioro_skip.200.1.5.vec'

# Provided by Vasile; localhost for the Docker container.
#GENERALNERURL = 'http://127.0.0.1/ner/ner.php'
# Just for testing purposes.
GENERALNERURL = 'http://89.38.230.23/ner/ner.php'
