from functools import cmp_to_key
import atexit
import inspect
import sys
import platform
import os
from pathlib import Path

from PipAlgo import PipAlgo
from PipApi import PipApi
from PipDTO import PipDTO

# Import all NLP apps that are implemented
from tnorm.TextNorm import TextNorm
from diac.DiacRestore import DiacRestore
from cubenlp.CubeNLP import CubeNLP
from ttl.TTLOps import TTLOps
from ner.NEROps import NEROps
from bioner.BioNEROps import BioNEROps

# Author: Radu Ion (radu@racai.ro)
class NLPipe(object):
    """This is the NLPipe platform that integrates all of the exposed
    NLP apps and provides them as PipApi objects.
    The user only has to specify what operations he/she wants and, with each
    NLP op, the algorithm to perform the op."""

    def _startApps(self):
        """When you add a new NLP app, don't forget to add it here as well!"""

        tn = TextNorm()
        dr = DiacRestore()
        dr.loadResources()
        cb = CubeNLP()
        cb.createApp()
        cb.loadResources()
        ttl = TTLOps()
        ttl.createApp()
        ner = NEROps()
        bner = BioNEROps()
        bner.createApp()

        return [tn, dr, cb, ttl, ner, bner]

    def _indexOfAlgo(self, algo: str) -> int:
        """Given an algorithm name from PipAlgo.getAvailableAlgorithms(),
        get the index of the corresponding PipApi object from self._apps."""

        appi = -1

        for i in range(len(self._apps)):
            app = self._apps[i]

            if app.getAlgoName() == algo:
                appi = i
                break

        return appi

    def _checkApiUniqueNames(self):
        """Each PipApi object must have a unique algorithm name."""

        for i in range(len(self._apps)):
            ain = self._apps[i].getAlgoName()

            for j in range(i + 1, len(self._apps)):
                ajn = self._apps[j].getAlgoName()

                if ain == ajn:
                    raise RuntimeError("NLP app '" + ain + \
                        "' found twice in self._apps. Each PipApi object must have a unique name!")
    
    def defaultConfiguration(self):
        # Dictionary of operations to implementing algorithms (NLP app).
        self._conf = {}

        for op in PipAlgo.getAvailableOperations():
            al4op = PipAlgo.getAlgorithmsForOper(op)

            if al4op:
                self._conf[op] = al4op[0]
                print("{0}.{1}[{2}]: configuring operation '{3}' with algorithm '{4}'".\
                    format(
                        Path(inspect.stack()[0].filename).stem,
                        inspect.stack()[0].function,
                        inspect.stack()[0].lineno,
                        op,
                        al4op[0]
                    ), file = sys.stderr, flush = True)
            else:
                self._conf[op] = al4op
                print("{0}.{1}[{2}]: operation '{3}' is not implemented!".\
                    format(
                        Path(inspect.stack()[0].filename).stem,
                        inspect.stack()[0].function,
                        inspect.stack()[0].lineno,
                        op
                    ), file = sys.stderr, flush = True)

    def __init__(self):
        self.defaultConfiguration()
        self._apps = self._startApps()
        self._checkApiUniqueNames()
        atexit.register(self._destroyAllApps)

    def getConfiguration(self, op: str = None):
        if op is None:
            # Just return the whole configuration
            return self._conf
        
        if op in self._conf:
            # Or return the configuration for op,
            # if not None
            return self._conf[op]
        else:
            return None

    def configure(self, op: str, algo: str):
        availableOps = PipAlgo.getAvailableOperations()
        availableAlgos = PipAlgo.getAvailableAlgorithms()

        if op not in availableOps:
            raise RuntimeError("Operation '" + op + "' is not recognized. See class PipAlgo.")

        if algo not in availableAlgos:
            raise RuntimeError(
                "NLP app '" + algo + "' is not recognized. See class PipAlgo.")

        if not PipAlgo.canPerform(algo, op):
            raise RuntimeError(
                "NLP app '" + algo + "' cannot perform operation '" + op + "'. See class PipAlgo.")

        print("{0}.{1}[{2}]: requesting operation '{3}' be performed with '{4}'".\
            format(
                Path(inspect.stack()[0].filename).stem,
                inspect.stack()[0].function,
                inspect.stack()[0].lineno,
                op,
                algo
            ), file = sys.stderr, flush = True)

        self._conf[op] = algo

    def pcFull(self, text: str) -> PipDTO:
        """This is the complete processing chain (pc), executing
        all NLP ops enumerated in PipAlgo."""

        # Just run everything we know about on text.
        return self.pcExec(text, PipAlgo.getAvailableOperations())

    def pcDiac(self, text: str) -> str:
        """This processing chain will insert diacritics in a text
        which does not have them."""
        
        # You can specify the whole call chain, if you know it.
        return self.pcExec(text, [
            PipAlgo.getTextNormOperName(),
            PipAlgo.getDiacRestorationOperName()])

    def pcLemma(self, text: str) -> PipDTO:
        """This processing chain will do POS tagging and lemmatization
        on the input text, splitting the text in sentences and tokens beforehand."""
        
        # Or you can specify a few operations like 'lemmatization', 
        # pcExec will infer the dependencies.
        return self.pcExec(text, [PipAlgo.getLemmatizationOperName()])

    def pcParse(self, text: str) -> PipDTO:
        """This processing chain will do chunking and dependency parsing
        on the input text, splitting the text in sentences and tokens and
        doing POS tagging and lemmatization beforehand."""
        
        return self.pcExec(text, [PipAlgo.getDependencyParsingOperName()])

    def pcExec(self, text: str, ops: list) -> PipDTO:
        availableOps = PipAlgo.getAvailableOperations()
        maxIndex = 0

        # 1. Check if all requested ops are valid
        # 2. Find the requested operation with the
        # maximum index in the availableOps list
        for op in ops:
            if op not in availableOps:
                raise RuntimeError("Operation '" + op + "' is not recognized. See class PipAlgo.")
            else:
                opi = availableOps.index(op)

                if opi > maxIndex:
                    maxIndex = opi

        # 3. Fill in all operations, up to the requested
        # operation that has the largest index in the ordered
        # list of availableOps
        allOps = []

        for i in range(maxIndex + 1):
            allOps.append(availableOps[i])

        return self._execOps(text, allOps)

    def _appCompareFunc(self, x: PipApi, y: PipApi) -> int:
        if x._algoName == y._algoName:
            # The same app, return 0
            return 0

        minXIndex = PipAlgo.getMinOperIndex(x._algoName)
        minYIndex = PipAlgo.getMinOperIndex(y._algoName)

        if minXIndex == -1 and minYIndex == -1:
            # Neither can perform anything, so don't
            # swap when sorting PipApi objects
            return -1

        if minYIndex == -1:
            # y PipApi cannot perform anything,
            # x comes before it
            return -1

        if minXIndex < minYIndex:
            # x has a minimum op index less than y,
            # x comes first
            return -1
        elif minXIndex == minYIndex:
            # If minimum ops indexes are the same,
            # see which one is preferred
            xop = PipAlgo.getOperationsForAlgo(x._algoName)[0]

            if self._conf[xop] == x._algoName:
                return -1

        return 1

    def _execOps(self, text: str, ops: list) -> PipDTO:
        """This processing chain will make sure that the full list of
        requested operations (ops) are executed on the input text."""

        configuredApps = []

        # 0 Dynamically alter the configuration
        # depending on exceptions.
        # For instance ner-icia requires ttl-icia, not nlp-cube-adobe
        for op in ops:
            app = self._conf[op]
            sconf = PipAlgo.getConfSpecial(op, app)

            if sconf is not None:
                for sop in sconf:
                    self._conf[sop] = sconf[sop]
                    print(("{0}.{1}[{2}]: " + \
                        "configuration exception triggered by operation '{3}' with algorithm '{4}': " + \
                        "reconfiguring operation '{5}' with algorithm '{6}'"). \
                        format(
                            Path(inspect.stack()[0].filename).stem,
                            inspect.stack()[0].function,
                            inspect.stack()[0].lineno,
                            op,
                            app,
                            sop,
                            sconf[sop]
                        ), file = sys.stderr, flush = True)

        # 1. Get instantiated apps for the requested operations.
        for op in ops:
            opi = self._indexOfAlgo(self._conf[op])

            if opi >= 0:
                app = self._apps[opi]

                if app not in configuredApps:
                    configuredApps.append(app)
            else:
                print("{0}.{1}[{2}]: operation '{3}' is not supported yet.".\
                    format(
                        Path(inspect.stack()[0].filename).stem,
                        inspect.stack()[0].function,
                        inspect.stack()[0].lineno,
                        op
                    ), file = sys.stderr, flush = True)

        # 2. Sort apps in order of their execution rank,
        # so that operations are applied in the proper order.
        configuredApps = sorted(configuredApps, key = cmp_to_key(self._appCompareFunc))

        # 3. Run all configured NLP apps in sequence on
        # the dto object.
        dto = PipDTO(text, self._conf)

        for app in configuredApps:
            print("{0}.{1}[{2}]: running NLP app '{3}'".\
                format(
                    Path(inspect.stack()[0].filename).stem,
                    inspect.stack()[0].function,
                    inspect.stack()[0].lineno,
                    app.getAlgoName()
                ), file = sys.stderr, flush = True)
            dto = app.doWork(dto)

        # 4. Work done, return the dto object.
        return dto

    def _destroyAllApps(self):
        """Destroys the instantiated NLP apps."""

        for app in self._apps:
            print("{0}.{1}[{2}]: destroying NLP app '{3}'".\
                format(
                    Path(inspect.stack()[0].filename).stem,
                    inspect.stack()[0].function,
                    inspect.stack()[0].lineno,
                    app.getAlgoName()
                ), file = sys.stderr, flush = True)
            app.destroyApp()
