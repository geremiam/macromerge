import argparse
import re
import collections
import more_itertools

def indices(input_list, val):
    return list(more_itertools.locate(input_list, pred=lambda x: x==val))

def isolate_dupes(commandlist, verbose=True):
    # List of command names
    names = [el[1] for el in commandlist]
    # Dictionnary giving frequency of each name
    counter = collections.Counter(names)
    
    if verbose: print(counter)
    
    # List for outputting the commands
    outputlist = []
    
    # Iterate over the distinct keys
    for key in counter:
        # Get the indices at which "key" occurs in the list of names
        idxs = indices(names, key)
        
        for i, idx in enumerate(idxs):
            if i==0: # Add the first occurence as is
                outputlist.append( commandlist[idx] )
            else: # Add further occurences as comments
                commandtemp = commandlist[idx]
                commandtemp[2] = r'%' + commandtemp[2]
                outputlist.append( commandtemp )
    
    return outputlist


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.prog = "merge.py"
    parser.description = "Merge sty files."
    
    parser.add_argument("inputfile", help="Input file", nargs='+', type=str)
    parser.add_argument("-o", "--outputname", help="Name for output", required=True, type=str)
    parser.add_argument("-v", "--verbose", help="Show merged macros", action="store_true")
    #parser.add_argument("-q", "--quiet", help="", action="store_true")
    args = parser.parse_args()
    
    # List for holding commands
    newcommands = []
    renewcommands = []
    
    # Regular expressions for matching
    com1_re = r'(\\newcommand)'
    com2_re = r'(\\renewcommand)'
    name_re = r'[ {]*(\\[^ \[\]{}\\]*)'
    
    p1 = re.compile(com1_re + name_re) # Matches "newcommand" definitions
    p2 = re.compile(com2_re + name_re) # Matches "renewcommand" definitions
    
    # Open files and collect command definitions
    for filename in args.inputfile:
        with open(filename, 'r') as fh:
            all_lines = fh.readlines()
        
        for line in all_lines:
            m1 = p1.search(line) # Search for "newcommand" definitions
            m2 = p2.search(line) # Search for "renewcommand" definitions
            
            # Strip trailing whitespaces (including newlines) and add file of origin
            line = line.rstrip() + r' % ' + filename
        
            if m1 is not None:
                assert m2 is None # Consistency check
                newcommands.append( [m1.group(1), m1.group(2), line] ) # Append to list
        
            if m2 is not None:
                assert m1 is None # Consistency check
                renewcommands.append( [m2.group(1), m2.group(2), line] ) # Append to list
    
    newcommands_nodupes   = isolate_dupes(newcommands, verbose=False)
    renewcommands_nodupes = isolate_dupes(renewcommands, verbose=False)
    
    for val in newcommands_nodupes: print(val[2])
    