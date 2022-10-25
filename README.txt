Created by Luo Rui Russell
For any bugs/suggestions email me at luorrussell@gmail.com

Objectives:
1. Assigns a namelist of people to a list of dutyposts without conflict, accounting for rest time between duties
2. Balances out the hours such that there are no possible giving/1-1 swapping of duties that will result in a more equal distribution of hours

Usage instructions:
1. Create csv(comma-separated values) files with duties and names in the format of the sample csv files in the duties and names directories
2. In duties, start_time refers to the hours since the start of the cycle (e.g. for a monday-wednesday cycle, monday 12pm is 0, monday 6pm is 6, tuesday 12pm is 24 and wednesday 11am is 47)
3. In duties, location refers to the name of the dutypost (eg sky(ag), super(checker))
4. In duties, duration refers to the length of the duty
5. In duties, rest refers to the time a trooper is barred from duties following a duty (for rest and to account for transport)
7. Values in duties can be changed to minutes if you multiply all values by 60
8. Place csv files in the duties/names directories respectively
9. Click on runner.exe
10. In the interface, select the csv files (make sure the correct csv file goes in the correct field)
11. In the interface, choose filenames for the output files (remember to set the filetype to csv e.g. output_namelist.csv)
12. Press begin
13. Find your freshly baked output files in the output folder

FAQs

What if x is banned armed guard, y has early bookout etc.
Plan their duties by hand and remove them from namelist and remove the duties assigned to them from the dutylist.

X took mc halfway, what do?
Plan duties by hand :(

I got an error saying there is insufficient people to assign.
Request for more manpower or cut down on rest time. Or both.
