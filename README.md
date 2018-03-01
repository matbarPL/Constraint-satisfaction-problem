# Constraint-satisfaction-problem
AI constraint satisfaction problem, timetable generating.
input: domain of values teachers: t1,t2,3...,tn, subject: s1,s2,...,sm, room: r1,r2,...rk and timedays = d11,d12,d13,d14,d15,d21,d22,....d54
output: timetable which in which are no conflicts     

Preknowledge: 

-teacher can teach different subject

Constraints:

-a teacher can teach maximum 4 times in a week 

-one room can be used only by one teacher in the sime time slot

-a teacher can teach one subject in one time slot

I used genetic algorithm. The population is created from timetables.
