# -*- coding: utf-8 -*-
import random as r
from math import floor,ceil
class Record():
    def __init__(self,teachersN,subjectN,roomN,timeN = 20):
        self.teacher_id = r.randint(1,teachersN)
        self.room_id = r.randint(1,roomN)
        self.subject_id = r.randint(1,subjectN)
        self.time_id = r.randint(1,timeN)
        
    def tablePos(self):
        columns = ['B','C','D','E','F']
        
        return columns[(self.time_id-1) % 5] + str(2+(self.time_id-1)//5)
        
    def __str__(self):
        return 'teacher_id ' + str(self.teacher_id) + '\n' + \
                'room_id ' + str(self.room_id) + '\n' + \
                'subject_id ' + str(self.subject_id) + '\n' + \
                'time_id ' + str(self.time_id)
                
if __name__ == '__main__':
    r1 = Record(5,5,5)
    print(r1.time_id)
    print (r1.tablePos())