import numpy as np
import math
import string
import sys
class Viterbi:
    delta = []
    def __init__(self, probEmission, probTransition, testSet):
        self.symbols = list(string.ascii_lowercase)
        self.symbolLength = len(self.symbols)
        self.corruptedTestSet = testSet
        self.emissionProbabilities = probEmission
        self.transitionProbabilities = probTransition
        self.initialProbabilities = list([float(1)/self.symbolLength] * self.symbolLength)
        # print "Initial Probabilities:\n", self.initialProbabilities
        # print "\n\nEmission Probabilities:\n", self.emissionProbabilities
        # print "\n\nTransition Probabilities:\n", self.transitionProbabilities

    def calculateInitialDelta(self, symbolChar):
        for i in range(0, self.symbolLength):
            # print self.initialProbabilities
            # print self.emissionProbabilities[i][self.symbols.index(symbolChar)]
            # print "-------------",i, "---------------"
            init = self.initialProbabilities[i]
            # init = np.log(self.initialProbabilities[i])
            emission = self.emissionProbabilities[i][self.symbols.index(symbolChar)]
            # emission = np.log(self.emissionProbabilities[i][self.symbols.index(symbolChar)])
            # if (not np.isinf(emission)):
            #     print init + emission
            # else:
            #     print emission
            # print init * emission
            self.delta.append(init * emission)
            # print "----------------------------"
        print self.delta

    def calculateDelta(self, symbolChar):
        # for i in range(0, self.symbolLength):
        print

    def process(self):
        print self.corruptedTestSet
        # self.corruptedTestSet = ['NUU']
        # self.symbols = "NUU"
        # self.symbolLength = len(self.symbols)
        for word in self.corruptedTestSet:
            print word
            for i in range(0, len(word)):
                symChar = word[i]
                print symChar
                if (i is 0):
                    self.calculateInitialDelta(symChar)
                else:
                    self.calculateDelta(symChar)
            sys.exit(1)


