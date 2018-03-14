# -*- coding: utf-8 -*-

class Subject():
    def __init__(self,idd,name,TimesPerWeek):
        self.id = idd
        self.name = name
        self.timesPerWeek = TimesPerWeek
        
    def __str__(self):
        return str(self.id) + " " + str(self.name) + " " + str(self.timesPerWeek) 