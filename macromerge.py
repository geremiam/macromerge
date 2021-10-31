import argparse
import re


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.prog = "merge.py"
    parser.description = "Merge sty files."
    
    parser.add_argument("-i", "--inputfile", help="Input file", action='append', required=True, type=str)
    parser.add_argument("outputname", help="Name for output", type=str)
    #parser.add_argument("--Wannierbands", action="store_true", help="Plot Wannier bands")
    #parser.add_argument("--Wannierpol", action="store_true", help="Calculate Wannier polarization")
    args = parser.parse_args()
    
    newcommands = []
    renewcommands = []
    
    com1_re = r'(\\newcommand)'
    com2_re = r'(\\renewcommand)'
    name_re = r'[ {]*(\\[^ {}\\]*)'
    
    #p = re.compile(r'(\\newcommand)[ {]*(\\[^ {}\\]*)')
    p1 = re.compile(com1_re + name_re)
    p2 = re.compile(com2_re + name_re)
    
    for filename in args.inputfile:
        # May be important: are the objects unpacked from 'list' actual copies?
        with open(filename, 'r') as fh:
            all_lines = fh.readlines()
    
        for line in all_lines:
            m1 = p1.search(line)
            m2 = p2.search(line)
        
            if m1 is not None:
                assert m2 is None
                newcommands += [(m1.group(1), m1.group(2), line)]
        
            if m2 is not None:
                assert m1 is None
                renewcommands += [(m2.group(1), m2.group(2), line)]
    
    #newcommands.sort(key=lambda x: x[1])
    
    print(newcommands)
    print()
    print(renewcommands)
    