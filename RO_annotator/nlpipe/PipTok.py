from PipAlgo import PipAlgo

# Author: Radu Ion (radu@racai.ro)
class PipTok(object):
    """This is the abstraction of a token, with
    all attributes that are supported. If you add
    other NLP apps that add more attributes, please make
    sure you add them here as well."""

    defaultValue = "_"

    def __init__(self):
        # Holds the position of the token
        # in the sentence (1-based numbering).
        self._id = 0
        # Has the word form of the token
        # as it appears in the sentence
        self._wordform = ""
        # Has the lemma of the word form
        self._lemma = ""
        # Has the MSD of the token disambiguated
        # in its sentence context
        self._msd = ""
        # Has the Corpus TAG of the token disambiguated
        # in its sentence context
        self._ctg = ""
        # 1-based token head of this token in
        # the sentence
        self._head = 0
        self._deprel = ""
        # Set this to the TTL's chunking information
        self._chunk = ""
        # Set this to PER/LOC and friends for NER
        self._ner = ""
        # Set this to B- and I- biomedical NER labels
        self._bner = ""
    
    def getId(self) -> int:
        """Get the ID of this token."""

        if self._id:
            return self._id
        
        return 0

    def setId(self, id: int):
        """Sets the ID of this token. Has to be >= 1."""

        if isinstance(id, int) and id >= 1:
            self._id = id
        else:
            raise RuntimeError("PipTok ID should be an int >= 1.")

    def getWordForm(self) -> str:
        """Gets the word form of this token."""

        if self._wordform:
            return self._wordform

        return PipTok.defaultValue

    def setWordForm(self, wordform: str):
        """Sets the word form of this token to the wordform."""
        if isinstance(wordform, str):
            self._wordform = wordform
        else:
            raise RuntimeError("PipTok WORDFORM should be a str.")

    def getNER(self) -> str:
        """Gets the named entity annotation of this token."""

        if self._ner:
            return self._ner

        return PipTok.defaultValue

    def setNER(self, ner: str):
        """Sets the named entity annotation of this token to the ner."""
        
        if isinstance(ner, str):
            self._ner = ner
        else:
            raise RuntimeError("PipTok NER should be a str.")

    def getBioNER(self) -> str:
        """Gets the biomedical named entity annotation of this token."""

        if self._bner:
            return self._bner

        return PipTok.defaultValue

    def setBioNER(self, bner: str):
        """Sets the biomedical named entity annotation of this token to the ner."""
        
        if isinstance(bner, str):
            self._bner = bner
        else:
            raise RuntimeError("PipTok BioNER should be a str.")

    def getLemma(self) -> str:
        if self._lemma:
            return self._lemma

        return PipTok.defaultValue

    def setLemma(self, lemma: str):
        if isinstance(lemma, str):
            self._lemma = lemma
        else:
            raise RuntimeError("PipTok LEMMA should be a str.")

    def getMSD(self) -> str:
        if self._msd:
            return self._msd

        return PipTok.defaultValue

    def setMSD(self, msd: str):
        if isinstance(msd, str):
            self._msd = msd
        else:
            raise RuntimeError("PipTok MSD should be a str.")

    def getCTAG(self) -> str:
        if self._ctg:
            return self._ctg

        return PipTok.defaultValue

    def setCTAG(self, ctg: str):
        if isinstance(ctg, str):
            self._ctg = ctg
        else:
            raise RuntimeError("PipTok CTAG should be a str.")

    def getHead(self) -> int:
        if self._head:
            return self._head

        return 0

    def setHead(self, head: int):
        if isinstance(head, int) and head >= 0:
            self._head = head
        else:
            raise RuntimeError("PipTok HEAD should be an int >= 0.")

    def getDepRel(self) -> str:
        if self._deprel:
            return self._deprel

        return PipTok.defaultValue
    
    def setDepRel(self, dprel: str):
        if isinstance(dprel, str):
            self._deprel = dprel
        else:
            raise RuntimeError("PipTok DEPREL should be a str.")

    def getChunk(self) -> str:
        if self._chunk:
            return self._chunk

        return PipTok.defaultValue

    def setChunk(self, chunk: str):
        if isinstance(chunk, str):
            self._chunk = chunk
        else:
            raise RuntimeError("PipTok CHUNK should be a str.")

    def __eq__(self, value):
        if isinstance(value, PipTok):
            if self._wordform == value.getWordForm():
                return True

        return False

    def __ne__(self, value):
        return not self.__eq__(value)

    def copyFrom(self, fromTok, align: list, oper: str):
        """Copy the value corresponding to 'oper' into
        the right field.
        align is 0-based and represents the 2-place tuples
        of indexes, i from the source and j from the target."""

        if oper == PipAlgo.getPOSTaggingOperName():
            self.setMSD(fromTok.getMSD())
            self.setCTAG(fromTok.getCTAG())
        elif oper == PipAlgo.getLemmatizationOperName():
            self.setLemma(fromTok.getLemma())
        elif oper == PipAlgo.getChunkingOperName():
            self.setChunk(fromTok.getChunk())
        elif oper == PipAlgo.getDependencyParsingOperName():
            self.setDepRel(fromTok.getDepRel())
            fh = fromTok.getHead()

            if fh == 0:
                self.setHead(0)
            else:
                th = 0

                for (i, j) in align:
                    if i + 1 == fh:
                        th = j + 1
                        break

                if th != self._id:
                    # Do not introduce a cycle here.
                    self.setHead(th)
        elif oper == PipAlgo.getNamedEntityRecognitionOperName():
            self.setNER(fromTok.getNER())
        elif oper == PipAlgo.getBiomedicalNamedEntityRecognitionOperName():
            self.setBioNER(fromTok.getBioNER())

    def getConllXRecord(self) -> str:
        feats = "_"

        if self._chunk and self._chunk != PipTok.defaultValue:
            if feats == "_":
                feats = "Chnk=" + self._chunk
            else:
                feats += "|" + "Chnk=" + self._chunk

        if self._ner and self._ner != PipTok.defaultValue:
            if feats == "_":
                feats = "NEnt=" + self._ner
            else:
                feats += "|" + "NEnt=" + self._ner

        if self._bner and self._bner != PipTok.defaultValue:
            if feats == "_":
                feats = "BioMed=" + self._bner
            else:
                feats += "|" + "BioMed=" + self._bner

        return \
            str(self.getId()) + "\t" + \
            self.getWordForm() + "\t" + \
            self.getLemma() + "\t" + \
            self.getCTAG() + "\t" + \
            self.getMSD() + "\t" + \
            feats + "\t" + \
            str(self.getHead()) + "\t" + \
            str(self.getDepRel()) + "\t" + \
            "_" + "\t" + "_"
