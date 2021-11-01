Merges files (typically sty files) containing LaTex macro definitions. 

usage: merge.py [-h] -o OUTPUTNAME [-v] inputfile1 inputfile2 [inputfile3 ...]

Only works with "newcommand" and "renewcommand" statements.
Statements must begin at the start of a new line; otherwise, they are ignored.
Order of the input files is preserved, and the first instance of a duplicate command is retained.
Only compares commands of the same type; does not check whether a "newcommand" conflicts with a "renewcommand".
