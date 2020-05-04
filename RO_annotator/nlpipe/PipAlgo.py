# Author: Radu Ion (radu@racai.ro)
class PipAlgo(object):
    """This class will hold the list of available
    NLPipe NLP algorithms (or applications/apps).
    Add new ones here!"""

    # Does space and dash normalization, Romanian diacritic
    # normalization (i.e. using ș/ț instead of ş/ţ)
    algoTNorm = "tnorm-icia"

    # Does sentence splitting, tokenization, POS tagging,
    # lemmatization and chunking.
    algoTTL = "ttl-icia"

    # Does sentence splitting, tokenization, POS tagging,
    # lemmatization and dependency parsing.
    algoCube = "nlp-cube-adobe"
    
    # Does Romanian diacritic restoration.
    algoDiac = "diac-restore-icia"

    # Provides Named Entity Recognition
    algoNER = "ner-icia"

    # Provides biomedical Named Entity Recognition
    algoBNER = "bioner-icia"

    # If there is a new algorithm in town,
    # make sure you add it to the proper lists,
    # according to what it does.
    # list[0] is the default algorithm for the op
    operToAlgo = {}

    # This is a dictionary of operations to
    # another dictionary of selected ops to selected apps.
    # Useful when some operation has preferences over what
    # apps run before it.
    operExcept = {}

    @staticmethod
    def getTextNormOperName() -> str:
        return "text-normalization"

    @staticmethod
    def getDiacRestorationOperName() -> str:
        return "diacritics-restoration"

    @staticmethod
    def getSentenceSplittingOperName() -> str:
        return "sentence-splitting"

    @staticmethod
    def getTokenizationOperName() -> str:
        return "tokenization"

    @staticmethod
    def getPOSTaggingOperName() -> str:
        return "pos-tagging"

    @staticmethod
    def getLemmatizationOperName() -> str:
        return "lemmatization"

    @staticmethod
    def getNamedEntityRecognitionOperName() -> str:
        return "named-entity-recognition"

    @staticmethod
    def getBiomedicalNamedEntityRecognitionOperName() -> str:
        return "biomedical-named-entity-recognition"

    @staticmethod
    def getChunkingOperName() -> str:
        return "chunking"

    @staticmethod
    def getDependencyParsingOperName() -> str:
        return "dependency-parsing"

    @staticmethod
    def getAvailableOperations() -> list:
        """Will return the ordered list of available operations.
        If op i is requested, then all ops 0:i have to be performed as well."""

        return [
            PipAlgo.getTextNormOperName(),
            PipAlgo.getDiacRestorationOperName(),
            PipAlgo.getSentenceSplittingOperName(),
            PipAlgo.getTokenizationOperName(),
            PipAlgo.getPOSTaggingOperName(),
            PipAlgo.getLemmatizationOperName(),
            PipAlgo.getNamedEntityRecognitionOperName(),
            PipAlgo.getBiomedicalNamedEntityRecognitionOperName(),
            PipAlgo.getChunkingOperName(),
            PipAlgo.getDependencyParsingOperName()
        ]

    @staticmethod
    def getAvailableAlgorithms() -> list:
        """Will return a list of recognized NLP apps."""
        
        return [
            PipAlgo.algoCube,
            PipAlgo.algoDiac,
            PipAlgo.algoTNorm,
            PipAlgo.algoTTL,
            PipAlgo.algoNER,
            PipAlgo.algoBNER
        ]

    @staticmethod
    def getAlgorithmsForOper(oper) -> list:
        if oper in PipAlgo.operToAlgo:
            algo4op = []

            for algo in PipAlgo.operToAlgo[oper]:
                algo4op.append(algo)

            return algo4op
        else:
            return []

    @staticmethod
    def getOperationsForAlgo(algo: str) -> list:
        cando = []

        if algo in PipAlgo.getAvailableAlgorithms():
            for op in PipAlgo.getAvailableOperations():
                if PipAlgo.canPerform(algo, op):
                    cando.append(op)

            return cando
        else:
            raise RuntimeError("NLP app '" + algo + "' is not recognized. See class PipAlgo.")

    @staticmethod
    def getMaxOperIndex(algo: str) -> int:
        """Returns the index of the last operation that algo(rithm) can perform.
        The index is in the list returned by getAvailableOperations()."""

        algoCanDo = PipAlgo.getOperationsForAlgo(algo)

        if algoCanDo:
            return PipAlgo.getAvailableOperations().index(algoCanDo[-1])
        else:
            return -1

    @staticmethod
    def getMinOperIndex(algo: str) -> int:
        """Returns the index of the first operation that algo(rithm) can perform.
        The index is in the list returned by getAvailableOperations()."""

        algoCanDo = PipAlgo.getOperationsForAlgo(algo)

        if algoCanDo:
            return PipAlgo.getAvailableOperations().index(algoCanDo[0])
        else:
            return -1

    @staticmethod
    def _assignAlgorithmsToOperations():
        """These are the available algorithms for every operation
        that NLPipe supports. List[0] for each operation is the default
        algorithm for it."""

        PipAlgo.operToAlgo[PipAlgo.getTextNormOperName()] = [PipAlgo.algoTNorm]
        PipAlgo.operToAlgo[PipAlgo.getDiacRestorationOperName()] = [PipAlgo.algoDiac]
        PipAlgo.operToAlgo[PipAlgo.getSentenceSplittingOperName()] = [PipAlgo.algoCube, PipAlgo.algoTTL]
        PipAlgo.operToAlgo[PipAlgo.getTokenizationOperName()] = [PipAlgo.algoCube, PipAlgo.algoTTL]
        PipAlgo.operToAlgo[PipAlgo.getPOSTaggingOperName()] = [PipAlgo.algoCube, PipAlgo.algoTTL]
        PipAlgo.operToAlgo[PipAlgo.getLemmatizationOperName()] = [PipAlgo.algoCube, PipAlgo.algoTTL]
        PipAlgo.operToAlgo[PipAlgo.getNamedEntityRecognitionOperName()] = [PipAlgo.algoNER]
        PipAlgo.operToAlgo[PipAlgo.getBiomedicalNamedEntityRecognitionOperName()] = [PipAlgo.algoBNER]
        PipAlgo.operToAlgo[PipAlgo.getChunkingOperName()] = [PipAlgo.algoTTL]
        PipAlgo.operToAlgo[PipAlgo.getDependencyParsingOperName()] = [PipAlgo.algoCube]

    @staticmethod
    def _fillInExceptionList():
        """For certain operations executed with certain apps, specify a
        configuration dictionary with ops to apps."""

        PipAlgo.operExcept[PipAlgo.getNamedEntityRecognitionOperName() + "#" + PipAlgo.algoNER] = {
            PipAlgo.getSentenceSplittingOperName(): PipAlgo.algoTTL,
            PipAlgo.getTokenizationOperName(): PipAlgo.algoTTL,
            PipAlgo.getPOSTaggingOperName(): PipAlgo.algoTTL,
            PipAlgo.getLemmatizationOperName(): PipAlgo.algoTTL
        }

    @staticmethod
    def canPerform(algo: str, oper: str) -> bool:
        return (oper in PipAlgo.operToAlgo) and (algo in PipAlgo.operToAlgo[oper])

    @staticmethod
    def getConfSpecial(oper: str, algo: str) -> dict:
        oakey = oper + "#" + algo

        if oakey in PipAlgo.operExcept:
            return PipAlgo.operExcept[oakey]
        else:
            return None

PipAlgo._assignAlgorithmsToOperations()
PipAlgo._fillInExceptionList()
