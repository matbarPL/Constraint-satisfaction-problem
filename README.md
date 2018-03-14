# Constraint-satisfaction-problem
AI constraint satisfaction problem, timetable generating, created during the student exchange program in collaboration with my friend Piotr Janus. 

input: excel file with specified constraints for every subject and teacher  
![](https://github.com/matbarPL/Constraint-satisfaction-problem/blob/master/subjects.png)
![](https://github.com/matbarPL/Constraint-satisfaction-problem/blob/master/teachers.png)

Input data

Constraints:

 - a teacher can teach maximum <limit> times in a week 

 - one room can be used only by one teacher in the sime time slot

 - a teacher can teach one subject in one time slot

 - a teacher can teach only specified subject

 - subject has to be in a timetable <timesPerWeek> times
  
 - teacher cannot teach in <notAvaialableHours>

The population in genetic algorithm is created from timetables.

![](https://github.com/matbarPL/Constraint-satisfaction-problem/blob/master/mut0.png)
Timetable before mutation
![](https://github.com/matbarPL/Constraint-satisfaction-problem/blob/master/mut.png)
Timetable after mutation
![](https://github.com/matbarPL/Constraint-satisfaction-problem/blob/master/cross1.png)
![](https://github.com/matbarPL/Constraint-satisfaction-problem/blob/master/cross2.png)
Timetables chose to crossing
![](https://github.com/matbarPL/Constraint-satisfaction-problem/blob/master/aftercross.png)
![](https://github.com/matbarPL/Constraint-satisfaction-problem/blob/master/aftercross2.png)
Timetables after crossing

![](https://github.com/matbarPL/Constraint-satisfaction-problem/blob/master/first.png)
First timetable in a population
![](https://github.com/matbarPL/Constraint-satisfaction-problem/blob/master/best.png)
Best timetable generated after ~ 4 seconds.
![](https://github.com/matbarPL/Constraint-satisfaction-problem/blob/master/specExWithoutCross.png)

Estimated execution time ~4.5 seconds
