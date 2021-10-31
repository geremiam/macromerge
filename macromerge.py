import argparse
import re
import collections


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.prog = "merge.py"
    parser.description = "Merge sty files."
    
    parser.add_argument("inputfile", help="Input file", nargs='+', type=str)
    parser.add_argument("-o", "--outputname", help="Name for output", required=True, type=str)
    parser.add_argument("-v", "--verbose", help="Show merged macros", action="store_true")
    #parser.add_argument("-q", "--quiet", help="", action="store_true")
    args = parser.parse_args()
    
    newcommands = []
    renewcommands = []
    
    com1_re = r'(\\newcommand)'
    com2_re = r'(\\renewcommand)'
    name_re = r'[ {]*(\\[^ \[\]{}\\]*)'
    
    p1 = re.compile(com1_re + name_re)
    p2 = re.compile(com2_re + name_re)
    
    for filename in args.inputfile:
        with open(filename, 'r') as fh:
            all_lines = fh.readlines()
        
        for line in all_lines:
            line += r' % ' + filename
            m1 = p1.search(line)
            m2 = p2.search(line)
        
            if m1 is not None:
                assert m2 is None
                newcommands += [(m1.group(1), m1.group(2), line)]
        
            if m2 is not None:
                assert m1 is None
                renewcommands += [(m2.group(1), m2.group(2), line)]
    
    # Make list of all commands, with 'newcommand' definitions coming last
    allcommands = newcommands + renewcommands
    # Sort list in place. Sorting algorithm is stable, so secondary order is preserved
    allcommands.sort(key=lambda x: x[1])
    
    if args.verbose:
        for i in allcommands: print(i)
    
    names = [el[1] for el in allcommands]
    print(names)
    print()
    counter = collections.Counter(names)
    print(counter)