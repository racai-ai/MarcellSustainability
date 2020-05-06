from tests import nlpipe
from PipAlgo import PipAlgo

text = "La 7      minute de centrul Brasovului,  imobilul\tpropus \
    spre vanzare se adreseaza\t\tcelor care isi doresc un spatiu \
    generos de locuit.\n\nAmplasarea constructiei  si\t\tgarajul reusesc sa exploateze \
    la maxim lotul de teren de 670 mp, ce are o deschidere de 15 metri liniari.\n"
text2 = "Stia ca demonstratia o sa fie un succes."
text3 = "Instanta suprema reia astazi judecarea."
text4 = "Diabetul zaharat este un sindrom caracterizat prin valori crescute ale concentrației glucozei în sânge (hiperglicemie) și dezechilibrarea metabolismului."

def test_TextNorm():
    dto = nlpipe.pcExec(text, [PipAlgo.getTextNormOperName()])
    
    # Spaces have been removed...
    assert dto.getText()[5] == 'm'
    assert dto.getText()[35] == 'i'

    # Tab has been removed...
    assert dto.getText()[43] == ' '
    assert dto.getText()[76] == ' '
    assert dto.getText()[77] == 'c'

    # Newlines are preserved...
    assert dto.getText()[127] == '\n'
    assert dto.getText()[128] == '\n'
   
def test_DiacRestore():
    dto = nlpipe.pcExec(text, [PipAlgo.getDiacRestorationOperName()])

    # Diacs have been inserted at the
    # proper places...
    # Brașovului
    assert dto.getText()[26] == 'ș'
    # vânzare
    assert dto.getText()[57] == 'â'
    # adresează
    assert dto.getText()[75] == 'ă'
    # își
    assert dto.getText()[88] == 'î'
    assert dto.getText()[89] == 'ș'
    # spațiu
    assert dto.getText()[105] == 'ț'

def test_DiacRestore2():
    dto = nlpipe.pcExec(text2, [PipAlgo.getDiacRestorationOperName()])

    assert dto.getText()[0] == 'Ș'
    assert dto.getText()[6] == 'ă'
    assert dto.getText()[17] == 'ț'
    assert dto.getText()[24] == 'ă'

def test_DiacRestore3():
    dto = nlpipe.pcExec(text3, [PipAlgo.getDiacRestorationOperName()])

    assert dto.getText()[6] == 'ț'
    assert dto.getText()[15] == 'ă'
    assert dto.getText()[25] == 'ă'

def test_TTL():
    nlpipe.configure(PipAlgo.getSentenceSplittingOperName(), PipAlgo.algoTTL)
    nlpipe.configure(PipAlgo.getTokenizationOperName(), PipAlgo.algoTTL)
    nlpipe.configure(PipAlgo.getPOSTaggingOperName(), PipAlgo.algoTTL)
    nlpipe.configure(PipAlgo.getLemmatizationOperName(), PipAlgo.algoTTL)

    dto = nlpipe.pcExec(text, [PipAlgo.getChunkingOperName()])
    
    # Processed two sentences...
    assert dto.getNumberOfSentences() == 2

    # For the first sentence:
    assert dto.getSentenceTokens(0)[0].getWordForm() == 'La'
    assert dto.getSentenceTokens(0)[0].getMSD() == 'Spsa'
    assert dto.getSentenceTokens(0)[0].getLemma() == 'la'
    assert dto.getSentenceTokens(0)[1].getWordForm() == '7'
    assert dto.getSentenceTokens(0)[5].getWordForm() == 'Brașovului'
    assert dto.getSentenceTokens(0)[5].getLemma() == 'Brașov'
    assert dto.getSentenceTokens(0)[5].getMSD() == 'Npmsoy'
    assert dto.getSentenceTokens(0)[5].getChunk() == 'Pp#2,Np#2'
    assert dto.getSentenceTokens(0)[22].getWordForm() == '.'
    assert dto.getSentenceTokens(0)[22].getCTAG() == 'PERIOD'

    # For the second sentence:
    assert dto.getSentenceTokens(1)[0].getWordForm() == 'Amplasarea'
    assert dto.getSentenceTokens(1)[22].getWordForm() == 'metri'
    assert dto.getSentenceTokens(1)[22].getCTAG() == 'NPN'

def test_MWEsAndDepTransfer():
    nlpipe.configure(
        PipAlgo.getSentenceSplittingOperName(), PipAlgo.algoTTL)
    nlpipe.configure(PipAlgo.getTokenizationOperName(), PipAlgo.algoTTL)
    nlpipe.configure(PipAlgo.getPOSTaggingOperName(), PipAlgo.algoTTL)
    nlpipe.configure(PipAlgo.getLemmatizationOperName(), PipAlgo.algoTTL)

    dto = nlpipe.pcFull(text2)

    assert dto.getSentenceTokens(0)[3].getWordForm() == 'o_să'
    assert dto.getSentenceTokens(0)[3].getMSD() == 'Qf'
    assert dto.getSentenceTokens(0)[3].getHead() == 7
    assert dto.getSentenceTokens(0)[3].getDepRel() == 'mark'

def test_NLPCube():
    nlpipe.configure(
        PipAlgo.getSentenceSplittingOperName(), PipAlgo.algoCube)
    nlpipe.configure(PipAlgo.getTokenizationOperName(), PipAlgo.algoCube)
    nlpipe.configure(PipAlgo.getPOSTaggingOperName(), PipAlgo.algoCube)
    nlpipe.configure(PipAlgo.getLemmatizationOperName(), PipAlgo.algoCube)

    dto = nlpipe.pcExec(text, [PipAlgo.getDependencyParsingOperName()])
    
    # Processed two sentences...
    assert dto.getNumberOfSentences() == 2

    # Check some dependency structure...
    assert dto.getSentenceTokens(0)[7].getWordForm() == 'imobilul'
    assert dto.getSentenceTokens(0)[7].getHead() == 13
    assert dto.getSentenceTokens(0)[7].getDepRel() == 'nsubj'
    assert dto.getSentenceTokens(0)[13].getWordForm() == 'celor'
    assert dto.getSentenceTokens(0)[13].getHead() == 13
    assert dto.getSentenceTokens(0)[13].getDepRel() == 'iobj'

    assert dto.getSentenceTokens(1)[0].getWordForm() == 'Amplasarea'
    assert dto.getSentenceTokens(1)[0].getHead() == 5
    assert dto.getSentenceTokens(1)[0].getDepRel() == 'nsubj'
    assert dto.getSentenceTokens(1)[1].getWordForm() == 'construcției'
    assert dto.getSentenceTokens(1)[1].getHead() == 1
    assert dto.getSentenceTokens(1)[1].getDepRel() == 'nmod'

def test_NEROps():
    dto = nlpipe.pcExec(text3, [PipAlgo.getNamedEntityRecognitionOperName()])

    # Check NER annotations
    assert dto.getSentenceTokens(0)[0].getNER() == 'ORG'
    assert dto.getSentenceTokens(0)[1].getNER() == 'ORG'
    assert dto.getSentenceTokens(0)[3].getNER() == 'TIME'

def test_BioNEROps():
    dto = nlpipe.pcExec(
        text4, [PipAlgo.getBiomedicalNamedEntityRecognitionOperName()])

    # Check BioNER annotations
    assert dto.getSentenceTokens(0)[0].getBioNER() == 'B-DISO'
    assert dto.getSentenceTokens(0)[1].getBioNER() == 'I-DISO'
    assert dto.getSentenceTokens(0)[4].getBioNER() == 'B-DISO'
    assert dto.getSentenceTokens(0)[11].getBioNER() == 'B-CHEM'
    assert dto.getSentenceTokens(0)[13].getBioNER() == 'B-ANAT'
