Merges files (typically sty files) containing LaTex macro definitions, keeping the first instance of duplicate definitions. 

usage: macromerge [-h] -o OUTPUTNAME [-v] inputfile1 inputfile2 [inputfile3 ...]

Only works with "newcommand" and "renewcommand" statements.
Statements must begin at the start of a new line; otherwise, they are ignored.
Order of the input files determines the order of the commands, except for the duplicate commands, which are placed after the first instance of the command (and are commented out).
Only compares commands of the same type; does not check whether a "newcommand" conflicts with a "renewcommand".
