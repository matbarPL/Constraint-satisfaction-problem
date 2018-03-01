# -*- coding: utf-8 -*-
from Record import *
import xlsxwriter
from xlrd import open_workbook
import subprocess
from openpyxl import load_workbook

class Timetable():
    def __init__(self,teacherN,subjectN,roomN):
        self.conflicts = 0
        self.records = [Record(teacherN,subjectN,roomN) for i in range(subjectN)]
        self.teacherN = teacherN
        self.subjectN = subjectN
        self.roomN = roomN
        
    def setConflicts(self):
        self.conflicts = 0
        dic = {}
        for i in range(len(self.records)-1):
            fst = self.records[i]
            for j in range(i+1,len(self.records)):
                snd = self.records[j]
                if (fst.time_id == snd.time_id):
                    if (fst.teacher_id == snd.teacher_id):
                        self.conflicts +=1
                        
                    if (fst.room_id == snd.room_id):
                        self.conflicts +=1
                        
            if (fst.teacher_id) not in dic:
                dic[fst.teacher_id] = 1
            else:
                dic[fst.teacher_id] += 1
                
        greater = [(x[0],x[1]) for x in list(dic.items()) if x[1]>4]
        
        self.conflicts += sum( [x[1] -4 for x in greater])
    
    def generate(self,path,openfile=True):
        workbook = xlsxwriter.Workbook('timetable.xlsx')
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
            rec_str = 'teacher_id '+ str(record.teacher_id) + \
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
            subprocess.call(path+'timetable.xlsx',shell=True)
        
        
if __name__ == '__main__':
    #type your path in here!
    path = ' '
    tbl = Timetable(2,15,2)
    tbl.setConflicts()
    print (tbl.conflicts)
    tbl.generate(path,True)
    
    