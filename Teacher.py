# -*- coding: utf-8 -*-

import random as r

class Teacher():
    def __init__(self,idd,subjects=[],notAvailHours=[],limit = 4):
        self.id = idd
        self.subjects = subjects
        self.notAvailHours = notAvailHours
        self.limit = limit

        