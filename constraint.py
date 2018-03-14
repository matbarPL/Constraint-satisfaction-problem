# -*- coding: utf-8 -*-
import random as r
from Timetable import *
import copy as copy

class PG():
    def __init__(self,initN,iterNum,mutPr,crossPr,teacherN,subjectN,roomN):
        self.teacherN = teacherN
        self.subjectN = subjectN
        self.roomN = roomN
        self.initN = initN
        self.pop = self.createPop()
        self.iterNum = iterNum
        self.mutPr = mutPr
        self.crossPr = crossPr
        self.descendents = []
        self.parents = []
        
    def createPop(self):
        pop = []
        for i in range(self.initN):
            pop.append(Timetable(self.teacherN,self.subjectN,self.roomN))
        return pop
        
    def classify(self):
        for item in self.pop:
            item.setConflicts()
            
    def sampleTwoObjects(self):
        first = r.randint(0,self.initN-1)
        second = r.randint(0,self.initN-1)
        while (second == first):
            second = r.randint(0,self.initN-1)
            
        return (self.pop[first],self.pop[second])
    
    def takeBest(self):
        pair = self.sampleTwoObjects()
        if (pair[0].conflicts<pair[1].conflicts):
            return pair[0]
        return pair[1]
    
    def selection(self):
        self.parents = []
        for i in range(self.initN):
            self.parents.append(self.takeBest())
    
    def makePairs(self):
        self.pairs = []
        helpPop = copy.copy(self.parents)
        helpList = [i for i in range(len(self.parents))]
        for i in range(len(helpPop)//2):
            fst = r.sample(helpList,1)[0]
            helpList.remove(fst)
            snd = r.sample(helpList,1)[0]
            helpList.remove(snd)
            self.pairs.append((self.pop[fst],self.pop[snd]))
        
    
    def mutate(self):
        for desc in self.descendents:
            pr = r.randint(0,100)
            if pr< self.mutPr:
                desc.records[ r.randrange(0,len(desc.records)) ] = Record(desc.teacherN, desc.subjectN,desc.roomN)
        
    def crossing(self):
        for item in self.pairs:
            r1 = r.randint(0,100)
            if self.crossPr < r1:
                fst = r.randrange(0,len(item[0].records))
                snd = r.randrange(0,len(item[1].records))
                
                temp = item[0].records[fst]
                item[0].records[fst] = item[1].records[snd]
                item[1].records[snd] = temp
                
            self.descendents.extend((item[0],item[1]))
        
        
    def run(self):
        self.classify()
        for i in range(self.iterNum):
            self.selection()
            self.makePairs()
            self.crossing()
            self.mutate()
            self.pop = copy.copy(self.descendents)
            self.descendents = []
            self.classify()
            printProgressBar(i,self.iterNum-1,"Progress","Creating timetable")
    
    def getBestTimetable(self):
        return min(self.pop, key = lambda x: x.conflicts)
    
    def getAllConflicts(self,pop):
        return [x.conflicts for x in pop ]
    
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 70, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')

    if iteration == total: 
        print()    
if __name__ == '__main__':
    pg = PG(initN = 100, iterNum = 2000,mutPr=2,crossPr = 2,teacherN=4,subjectN=15,roomN=2)
    pg.run()
    print ('Number of conflicts: ' + str(pg.getBestTimetable().conflicts))
    path = 'C:/Users/Mateusz/Desktop/Semestr 6/Artificial Intelligence/Constraint satisfaction problem/'
    pg.getBestTimetable().generate(path,True)