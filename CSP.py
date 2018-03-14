# -*- coding: utf-8 -*-
import random as r
from Timetable import *
import copy as copy
import xlwings as xw
from Subject import *
import time as t
from matplotlib import pyplot as plt

def readFromFile(filename):
    book = xw.Book(filename)
    sht = book.sheets[0].range('A1').expand().value  
    sht = [list(map(str,row)) for row in sht]
    teachers = []
    subjects=[]
    app = xw.apps.active    
    
    for i in range(1,len(sht)):
        teachers.append(Teacher(int(float(sht[i][0])) ,list(map(int,sht[i][1].split(';'))), list(map(int,sht[i][2].split(';'))), int(float(sht[i][3]))))
    sht = book.sheets[1].range('A1').expand().value
    for i in range(1,len(sht)):
        subjects.append(Subject(int(float(sht[i][0])),sht[i][1],int(float(sht[i][2]))))
    app.quit()
    return(teachers,subjects)       

class PG():
    def __init__(self,initN,iterNum,mutPr,crossPr,roomN, tup,beamSearch = False):
        self.roomN = roomN
        self.initN = initN
        self.teachers = []
        self.subjects = []
        self.getFromFile(tup)
        self.pop = self.createPop()
        self.bestTb = []
        self.iterNum = iterNum
        self.mutPr = mutPr
        self.crossPr = crossPr
        self.beamSearch = False
        
    def getFromFile(self,tup):
        self.teachers,self.subjects = tup

    def createPop(self):
        pop = []
        for i in range(self.initN):
            pop.append(Timetable(self.teachers,self.subjects,self.roomN))
        return pop
        
    def classify(self):
        for item in self.pop:
            item.setConflicts()
        self.bestTb.append(self.getBestTimetable().conflicts)
            
    def sampleTwoObjects(self):
        sampInd = r.sample(range(self.initN),2)              
        return (self.pop[sampInd[0]],self.pop[sampInd[1]])
    
    def takeBest(self):
        pair = self.sampleTwoObjects()
        if (pair[0].conflicts<pair[1].conflicts):
            return pair[0]
        return pair[1]
    
    def selection(self):
        parents = []
        for i in range(self.initN-2):
            parents.append(self.takeBest())
        parents.append(self.getBestTimetable())        
        parents.append(self.getBestTimetable())
        return parents
    
    def makePairs(self,parents):
        helpList = r.sample(parents,len(parents))        
        return list(zip(helpList[::2],helpList[1::2]))
#    
    def mutate(self, descendents,k):
        for i in range(len(descendents)):
            pr = r.randint(0,100)
            if pr< self.mutPr:    
                helpDesc = copy.deepcopy(descendents[i])
                randInd = r.randrange(0,len(helpDesc.records))
                
                if (r.randint(1,self.iterNum)<k*r.random()):     
                    worstRec = helpDesc.getWorstRecord()
                    randInd = helpDesc.getRecordId(worstRec)
                    
                helpDesc.records[randInd] = Record(helpDesc.teacherList,helpDesc.roomN)
                helpDesc.setConflicts()
                
                if helpDesc.conflicts < descendents[i].conflicts:
                    descendents[i] = helpDesc
        return descendents
        
                    
    def crossing(self, pairs):
        descendents =[]
        for item in pairs:
            pr = r.randint(0,100)
            if pr < self.crossPr:
                pCopy = copy.deepcopy(item)
                
                fstConflicts = item[0].conflicts
                sndConflicts = item[1].conflicts
                
                fstInd = r.randrange(0,len(item[0].records))
                sndInd = r.randrange(0,len(item[1].records))
                
                pCopy[0].records[fstInd],pCopy[1].records[sndInd] = pCopy[1].records[sndInd],pCopy[0].records[fstInd]
                
                pCopy[0].setConflicts()
                pCopy[1].setConflicts()
                
                if (fstConflicts>pCopy[0].conflicts or sndConflicts>pCopy[1].conflicts):
                    if pCopy[0].conflicts < pCopy[1].conflicts:
                        item = (pCopy[0],pCopy[0])
                    else:
                        item = (pCopy[1],pCopy[1])
            descendents.extend(item)
        return descendents
        
    def run(self):
        self.classify()
        lastconflicts = []
        if self.beamSearch:
            a = int(0.1*self.iterNum)
        i = 0
        while (i < self.iterNum and self.getBestTimetable().conflicts!=0):
            i += 1
            parents = self.selection()
            pairs = self.makePairs(parents)
            descendents = self.crossing(pairs) 
            self.pop = self.mutate(descendents,i)
            self.classify()
            lastconflicts.append(self.getBestTimetable())
            if (self.beamSearch and len(lastconflicts)>a and lastconflicts[-a:].count(lastconflicts[-1]) == a):
                self.beamSearch(2,self.pop)
                lastconflicts=[]
    
    def beamSearch(self,k,pop):
        pop = self.pop
        sortedPop = sorted(pop, key = lambda x: x.conflicts)
        kBestPop = sortedPop[:k]
        minConf = kBestPop[0].conflicts
        counter =0
        while(self.getBestTimetable(kBestPop).conflicts > minConf-1 and counter<10):
            counter +=1
            for i in range(k):                                
                oldConflicts = kBestPop[i].conflicts
                for j in range(len(kBestPop[i].records)):
                    tableCopy = copy.deepcopy(kBestPop[i])
                    tableCopy.records[j] = Record(tableCopy.teacherList,tableCopy.roomN)
                    tableCopy.setConflicts()
                    if oldConflicts > tableCopy.conflicts:
                        kBestPop[i] = tableCopy
                        oldConflicts =  kBestPop[i].conflicts
                        break
        
        sortedPop[-k:] = kBestPop   
        self.pop = sortedPop
                        
    def getBestTimetable(self, pop = [] ):
        if len(pop)==0:
            pop=self.pop
        return min(pop, key = lambda x: x.conflicts)    

    def getWorstTimetable(self, pop = [] ):
        if len(pop)==0:
            pop=self.pop
        return max(pop, key = lambda x: x.conflicts) 

    def generateBest(self,path,show):
        self.getBestTimetable().generate(path,show)          
                    
            

        
if __name__ == '__main__':
    path = r'C:\Users\Mateusz\Desktop\Semestr 6\Artificial Intelligence\Constraint satisfaction problem\timetable.xlsx'
    mProb = 100
    cProb = 0
    filename = r'C:\Users\Mateusz\Desktop\Semestr 6\Artificial Intelligence\Constraint satisfaction problem\data.xlsx'
    dataTuple = readFromFile(filename)
    pg = PG(initN = 4,iterNum = 2000,mutPr=mProb,crossPr = cProb,roomN=4 ,tup = dataTuple,beamSearch = False)        
    pg.run()
    pg.generateBest(path,True)
