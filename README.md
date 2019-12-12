# ACAS
## Air collision avoidance system

This repository contains a script to simulate an air collision avoidance system written as part
of the final project of the CS 6376-01 Hybrid and Embedded Systems at Vanderbilt University. 

The script can take up to four arguments namely source1, source2, dest1 and dest2 which represents
the source coordinates of first and second aircraft and destination of first and second
aircraft respectively. 

To run the script:
```
python3 acas.py -source1 x1 y1 direction1 -source2 x2 y2 direction2 -dest1 dx1 dy1 
-dest2 dx2 dy2
```
where x1, y1 are integer source coordinates and direction1 is the direction with which the
first aircraft is initialized. dx1 and dy1 are destination coordinates.  

There is a project report present here as well.