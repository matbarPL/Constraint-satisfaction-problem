# -*- coding: utf-8 -*-
from Record import *
import xlsxwriter
from xlrd import open_workbook
import subprocess
from openpyxl import load_workbook
from Teacher import *

class Timetable():
    def __init__(self,teacherList,subjectsList,roomN):
        self.teacherList = teacherList
        self.subjectsList = subjectsList
        self.roomN = roomN
        self.records = []
        
        for el in subjectsList:
            for i in range(el.timesPerWeek):
                self.records.append(Record(self.teacherList,roomN,el.id))
        self.conflicts = 0
        
    def getTeacher(self,idd):
        for item in self.teacherList:
            if item.id == idd:
                return item
    def getSubject(self,idd):
        for item in self.subjectsList:
            if item.id == idd:
                return item  
    
    def setConflicts(self):
        self.conflicts = 0
        dicSub = dict(zip(self.subjectsList, len(self.subjectsList)*[0]))
        dic = dict(zip(self.teacherList, len(self.teacherList)*[0]))
        
        for i in range(len(self.records)):
            old = self.conflicts
            fst = self.records[i]
            teacher = self.getTeacher(fst.teacher.id)
            subject = self.getSubject(fst.subject_id)
            if (fst.time_id in teacher.notAvailHours):
                self.conflicts +=1
            if (fst.subject_id not in teacher.subjects):
                self.conflicts +=1
                
            for j in range(i+1,len(self.records)):
                snd = self.records[j]
                if (fst.time_id == snd.time_id):
                    if (fst.teacher.id == snd.teacher.id):
                        self.conflicts +=1
                    if (fst.room_id == snd.room_id):
                        self.conflicts +=2
           
            dicSub[subject] += 1
            dic[teacher]    += 1    
            
            fst.help = self.conflicts - old 
            
        greaterSub = [(x[0],x[1]) for x in list(dicSub.items()) if x[1]!=x[0].timesPerWeek]
        greater    = [(x[0],x[1]) for x in list(dic.items()) if x[1]>x[0].limit]  
        
        self.conflicts +=3*sum( [abs(x[1] -x[0].timesPerWeek) for x in greaterSub])
        self.conflicts += sum( [x[1] -x[0].limit for x in greater])
        
    def getWorstRecord(self):
        return max(self.records, key = lambda x: x.recConflicts)
        
    def getRecordId(self, record):
        for i in range(len(self.records)):
            if self.records[i] == record:
                return i
                
        
    def generate(self,path,openfile=True):
        workbook = xlsxwriter.Workbook(path.split('/')[-1])
        worksheet = workbook.add_worksheet()
        worksheet.set_default_row(70)
        worksheet.set_row(0,30)
        worksheet.set_column(0, 0, 10)
        worksheet.set_column(1, 10, 33)
        cell_format= workbook.add_format({'text_wrap': True,'valign': 'vcenter', 'align': 'center'})
        cell_format1 = workbook.add_format({'text_wrap': True,'valign': 'vcenter', 'align': 'center','bold':True})
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        letters = 'BCDEFGHIJKL'
        columns = []
        for i in range(len(days)):
            columns.append(letters[i] + '1')
        for i in range(len(days)):
            worksheet.write(columns[i],days[i],cell_format1)
        hours = ['7:30-9:00','9:15-10:45','13:15-14:45','15:15-17:00']
        hrows = ['A'+str(i) for i in range(2,2+len(hours))]
        for i in range(len(hours)):
            worksheet.write(hrows[i], hours[i],cell_format1)
        helpRecords = sorted(self.records, key = lambda x : x.time_id)
        last = [None,None]
        for record in helpRecords:
            rec_str = 'teacher_id '+ str(record.teacher.id) + \
                            ' room_id '+str(record.room_id)+' subject_id '+ \
                            str(record.subject_id)
            where = record.tablePos()
            if (record.time_id != last[1] ):
                worksheet.write(where,rec_str,cell_format)
                last = [rec_str,record.time_id]
            else:
                rec_str += '\n'
                rec_str += last[0]
                last[0] = rec_str
                worksheet.write(where,rec_str,cell_format)
                
        if openfile:
            workbook.close()
            subprocess.call(path,shell=True)
    
    