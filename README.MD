# Ioet test task

## Task text:

The company ACME offers their employees the flexibility to work the hours they want. But due to some external circumstances they need to know what employees have been at the office within the same time frame

The goal of this exercise is to output a table containing pairs of employees and how often they have coincided in the office.

Input: the name of an employee and the schedule they worked, indicating the time and hours. This should be a .txt file with at least five sets of data. You can include the data from our examples below:

Example 1:

INPUT:  
RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00  
ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00  
ANDRES=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00  

OUTPUT:  
ASTRID-RENE: 2
ASTRID-ANDRES: 3
RENE-ANDRES: 2

Example 2:

INPUT:  
RENE=MO10:15-12:00,TU10:00-12:00,TH13:00-13:15,SA14:00-18:00,SU20:00-21:00
ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00

OUTPUT:  
RENE-ASTRID: 3


## Requirements

Python3
[download](https://www.python.org/downloads)


## How to run the solution

### main.py

```
Usage: main.py [-h] [-i INPUT] [-o OUTPUT]  

Optional arguments:  
  -h, --help                    show this help message and exit  
  -i INPUT, --input INPUT       input file name e.g. "INPUT"  
  -o OUTPUT, --output OUTPUT    output file name e.g. "OUTPUT"  
```

Description:  
  Run from your console.  
  Use it to run on a file containig single input.  
  Use -i or --input to specify input txt filename (without .txt). Default = INPUT.  
  Use -o or --output to specify output txt filename (without .txt). Default = OUTPUT.  

Input file example:
```
RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00
ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
ANDRES=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
```
Output file example:
```
ASTRID-RENE: 2
ASTRID-ANDRES: 3
RENE-ANDRES: 2
```


### main_multiple_inputs.py

```
Usage: main_multiple_inputs.py [-h] [-i INPUT] [-o OUTPUT]

Optional arguments:  
  -h, --help                    show this help message and exit  
  -i INPUT, --input INPUT       input file name e.g. "MULTIPLE_INPUT"  
  -o OUTPUT, --output OUTPUT    output file name e.g. "MULTIPLE_OUTPUT" 
``` 

Description:  
  Run from your console.  
  Use it to run on a file containig multiple inputs.  
  Use -i or --input to specify input txt filename (without .txt). Default = INPUT.  
  Use -o or --output to specify output txt filename (without .txt). Default = OUTPUT.  
  Each input block in input file should start with line INPUT: {input name}.  
 
Input file example:  
```
INPUT: Example 1:
RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00
ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
ANDRES=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
INPUT: Example 2:
RENE=MO10:15-12:00,TU10:00-12:00,TH13:00-13:15,SA14:00-18:00,SU20:00-21:00
ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
```
Output file example:
```
Example 1:
RENE-ASTRID: 2
RENE-ANDRES: 2
ASTRID-ANDRES: 3
Example 3:
RENE-ASTRID: 3
```


## Solution

### Step 1: Deserialize input text

Program transforms input text lines to a python dictionary where keys are names and values are lists of tuples, representing time frames when the employee was at the office. Connecting or intersecting time frames would be merged together.  
Lines 
```
"ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-20:30,SU20:30-21:30"
...
```
would be transformed to 
```
{
    "ASTRID":[
        (0,600,720), 
        (3,720,840),
        (6,1200,1260)
    ],
    ...
}
```
*SU20:00-20:30 and SU20:30-21:30 where merged to (6,1200,1260)  


### Step 2: Iterate over all pairs of names and count coincidences

In a double for-loop program iterates over all pairs of names and for each pair it iterates over all pairs of timeframs in a double for-loop and counts its intersections. Two frames are considered intersected if:  
1) Its days are equal and one of timeframes start is more than or equal to other timeframe finish.
2) One timeframes day is less by 1 than the other timeframe day and finish time of its timeframe is 1440(24:00) and start time of the other timeframe is 0(00:00).  
Example:  
if dict is
```
{
    "ASTRID":[
        (0,600,720), 
        (3,720,840),
        (6,0,240)
    ],
    "RENE":[
        (0,540,660),
        (4,720,840),
        (5,1200,1440)
    ],
    ...
}
```
it returns
```
(
    ("ASTRID","RENE",2),
    ...
)
```
*(6,0,240) and (5,1200,1440) are counted because Saturday 24:00 and Sunday 00:00 are the same time  


### Step 3: Write the results

Finally we write the results to an output file.


## Testing

To run tests, run next command from your cosole:
```
python -m unittest -v test
```
