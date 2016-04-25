import numpy as np
import math
import string
import sys
class Viterbi:
    def __init__(self, probEmission, probTransition, testSet):
        self.delta = []
        self.states = list(string.ascii_lowercase)
        self.symbols = list(string.ascii_lowercase)
        self.corruptedTestSet = testSet
        self.emissionProbabilities = probEmission
        self.transitionProbabilities = probTransition
        self.initialProbabilities = float(1)/len(self.states)      # Same initial probabilities for every states

        self.totalCorrected = 0
        self.totalCorrectCorrection = 0
        # self.totalIncorrectCorrection = 0
        self.totalCorrectionsNeeded = 0
        #Precision = totalCorrectCorrections/totalCorrected
        #Recall = totalCorrectCorrections/totalCorrectionsNeeded

        # print "Initial Probabilities:\n", self.initialProbabilities
        # print "\n\nTransition Probabilities:\n", self.transitionProbabilities
        # print "\n\nEmission Probabilities:\n", self.emissionProbabilities

    def calculateInitialDelta(self, symbolChar):
        self.delta = []
        for i in range(0, len(self.states)):
            init = self.initialProbabilities
            emission = self.emissionProbabilities[i][self.symbols.index(symbolChar)]
            self.delta.append(math.log(emission) + math.log(init))

    def calculateDelta(self, symChar):
        backTrack = [None] * len(self.states)
        deltaTemp = [None] * len(self.states)
        for j in range(0, len(self.states)):
            maxValue = None
            for i in range(0, len(self.states)):
                transition = self.transitionProbabilities[i][j]
                mul = self.delta[i] + math.log(transition)
                if (mul > maxValue or maxValue is None):
                    maxValue = mul
                    backTrack[j] = self.symbols[i]
            deltaCalc = maxValue + math.log((self.emissionProbabilities[j][self.symbols.index(symChar)]))
            # deltaTemp.append(deltaCalc)
            deltaTemp[j] = deltaCalc
        self.delta = deltaTemp
        return backTrack

    def correctedWord(self, backTrack):
        temp = self.delta.index(max(self.delta))
        # print self.delta
        # print temp
        word = [self.symbols[temp]]
        if (backTrack):
            for l in backTrack:
                word.append(l[temp])
                temp = self.states.index(l[temp])
            word.reverse()
        return ''.join(word)

    def process(self, testSet):
        #Precision = totalCorrectCorrections/totalCorrected
        #Recall = totalCorrectCorrections/totalCorrectionsNeeded

        testSet = [x for x in testSet if x.isalpha()]
        counter = 0
        for word in self.corruptedTestSet:
            # print "==============================="
            # print "Actual:", testSet[counter]
            # print "Corrupted:", word
            backtrack = []
            for i in range(0, len(word)):
                symChar = word[i]
                if (i is 0):
                    self.calculateInitialDelta(symChar)
                else:
                    backtrack.insert(0, self.calculateDelta(symChar))

            corrected = self.correctedWord(backtrack)
            # print "Corrected:", corrected
            # Corrections Needed
            if (testSet[counter] != word):
                self.totalCorrectionsNeeded += 1
                # Total Correct Corrections
                if (testSet[counter] == corrected):
                    self.totalCorrectCorrection += 1
                # total corrections
                if (word != corrected):
                    self.totalCorrected += 1


            counter += 1
            # print "==============================="

        print "Total Correct Corrections:", self.totalCorrectCorrection
        print "Total Corrections Needed:", self.totalCorrectionsNeeded
        print "Total Corrected: ", self.totalCorrected
        print "Recall: ", float(self.totalCorrectCorrection)/self.totalCorrectionsNeeded
        print "Precision: ", float(self.totalCorrectCorrection)/self.totalCorrected