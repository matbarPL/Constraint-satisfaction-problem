# -*- coding: utf-8 -*-
import random as r
class Record():
    def __init__(self,teacherList,roomN,subject = 0,timeN = 20):
        self.room_id = r.randint(1,roomN)
        self.recConflicts = 0
        self.teacher = r.sample(teacherList,1)[0]        
        self.subject_id = r.sample(self.teacher.subjects,1)[0]
        self.time_id = r.sample(list(frozenset(list(range(1,21)))-frozenset(self.teacher.notAvailHours)),1)[0]
        
    def tablePos(self):
        columns = ['B','C','D','E','F']
        return columns[(self.time_id-1) % 5] + str(2+(self.time_id-1)//5)
        
    def __str__(self):
        return 'teacher_id ' + str(self.teacher.id) + '\n' + \
                'room_id ' + str(self.room_id) + '\n' + \
                'subject_id ' + str(self.subject_id) + '\n' + \
                'time_id ' + str(self.time_id) + '\n' + \
                'recConflict ' + str(self.recConflict)
                