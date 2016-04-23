import re
import random
import string
import numpy as np
import sys
import Viterbi

class SpellingCorrection:

    doc = None
    trainingSet = []
    testSet = []
    corruptedTrainingSet = []
    corruptedTestSet = []

    def __init__(self):
        self.wordsList = []
        self.alphabets = string.ascii_lowercase
        self.Aij = np.zeros((len(self.alphabets), len(self.alphabets)), dtype=int)
        self.Eis = np.zeros((len(self.alphabets), len(self.alphabets)), dtype=int)
        self.probAij = np.zeros((len(self.alphabets), len(self.alphabets)), dtype=float)
        self.probEis = np.zeros((len(self.alphabets), len(self.alphabets)), dtype=float)

    def readFromFile(self, fileName ='unabom.txt'):
        """
        Read dataset from the filename.
        """
        file = open(fileName, "r")
        self.doc = file.read()

    def splitToWords(self):
        """
        Splits the words from the text and inserts into wordList
        """
        self.wordsList = re.findall(r'\w+', self.doc)

    def splitDocument(self):
        """
        Splits the document into training set (80%) and test set (20%)
        """
        # self.readFromFile('basicTest.txt')
        self.readFromFile('testdata.txt')
        # self.readFromFile()
        self.splitToWords()
        indexSplit = int(0.8 * len(self.wordsList))
        # splits into training set and test set
        self.trainingSet = self.wordsList[:indexSplit]
        self.testSet = self.wordsList[indexSplit:]


    def corruptText(self, wordList, isTrainingSet = False):
        """
        Corrupts the text and updates the emission count and transition count if it is training set
        :param wordList:
        :return:
        """
        corruptedlist = []
        for word in wordList:
            tempWord = ""
            for i in range(0, len(word)):
                if (word[i].isalpha()):
                    r = random.uniform(0, 1)
                    # To corrupt the letter if the random value generated is less than threshold
                    if (r < 0.2):
                        tempWord += random.choice(string.ascii_lowercase)
                    else:
                        tempWord += word[i].lower()
                    # updates the count for emission probability and transition probability
                    if (isTrainingSet):
                        self.incrEmissionCount(word[i].lower(), tempWord[i].lower())
                        # Keep track of the transitions from state i to state j
                        if (i is not len(word)-1):
                            # count the transition from state i to state j
                            self.incrTransitionCount(word[i].lower(), word[i+1].lower())

            corruptedlist.append(tempWord)
        return corruptedlist

    def incrTransitionCount(self, stateI, stateJ):
        self.Aij[self.alphabets.index(stateI)][self.alphabets.index(stateJ)] += 1

    def incrEmissionCount(self, currentSymbol, symbolS):
        self.Eis[self.alphabets.index(currentSymbol)][self.alphabets.index(symbolS)] += 1

    def probabilityAij(self):
        for i in range(0, len(self.alphabets)):
            # Smoothing (helps to add the transition from the state where there is no count in training set
            if (0 in self.Aij[i]):
                self.Aij[i] = [x+1 for x in self.Aij[i]]
            sum = self.Aij[i].sum()
            for j in range(0, len(self.alphabets)):
                self.probAij[i][j] = float(self.Aij[i][j]) / sum

    def probabilityEmission(self):
        for i in range(0, len(self.alphabets)):
            # Smoothing (helps to add the transition from the state where there is no count in training set
            if (0 in self.Eis[i]):
                self.Eis[i] = [x+1 for x in self.Eis[i]]
            sum = self.Eis[i].sum()
            for j in range(0, len(self.alphabets)):
                self.probEis[i][j] = float(self.Eis[i][j]) / sum

    def getEmissionProbabilities(self):
        return self.probEis

    def getTransitionProbabilities(self):
        return self.probAij

    def trainHMModel(self):
        self.splitDocument()
        # Corrupt the text splited for training set and test set
        self.corruptedTrainingSet = self.corruptText(self.trainingSet, True)
        # Calculate the probability for transition from state i to state j
        self.corruptedTestSet = self.corruptText(self.testSet, False)
        self.probabilityAij()
        self.probabilityEmission()
        # print self.Aij
        # print self.Eis
        # print self.probAij
        # print self.probEis


objSC = SpellingCorrection()
objSC.trainHMModel()
objViterbi = Viterbi.Viterbi(objSC.getEmissionProbabilities(), objSC.getTransitionProbabilities(), objSC.corruptedTestSet)
objViterbi.process()

