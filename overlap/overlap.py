from __future__ import print_function
import sys
import collections
import argparse

#Overlap samples from different files.
#Takes files from command line, and overlaps based on header and sample IDs.
#Currently only works on tab-delimited files.

def find_overlaps(filename, id_dict, pos_dict):
    with open(filename, 'r') as f:
        #Read the header and split it
        header = f.readline().rstrip()
        ids = header.split("\t")
        #Add IDs to the ID count dictionary
        for counter, id_val in enumerate(ids):
            if id_val in id_dict:
                id_dict[id_val] += 1
            else:
                id_dict[id_val] = 1

            #Add the position of the IDs to the position dictionary
            if id_val in pos_dict:
                pos_dict[id_val] += "," + str(counter + 1)
            else:
                pos_dict[id_val] = str(counter + 1)

def extract_columns(filename, keep_columns, extension, numfiles, arg, id_dict, pos_dict):
    with open(filename, 'r') as f:
        pos = []
        if keep_columns:
            pos.append(int(keep_columns))
        #Loop through the keys in the count dictionary
        for key in id_dict:
            #Only keep keys that have a count equal to the number of files
            if id_dict[key] == numfiles:
                ind = pos_dict[key].split(",")
                #Add the position of the column to the position array
                pos.append(int(ind[arg]))

        #Open the file
        if extension:
            filename = filename + extension + '.out'
        else:
            filename = filename + '.out'
        with open(str(filename), 'w') as fo:
            #Split each line, reorder using the position array,
            #join to string and write to *.out file
            for line in f:
                line = line.rstrip()
                temp = line.split("\t")
                new_line = [temp[y-1] for y in pos]
                new_line_str = "\t".join(new_line)
                print(new_line_str, file=fo)

def main():
    """Overlap samples"""
    #Set up command line arguments options
    parser = argparse.ArgumentParser()
    parser.add_argument('-k','--keepcolumns',nargs='?', help='')
    parser.add_argument('-e','--extension',nargs='?', help='')
    parser.add_argument('file', nargs='*', help='Files to overlap')
    args = parser.parse_args()

    id_dict = collections.OrderedDict()
    pos_dict = {}

    if args.extension and '.' not in args.extension:
        args.extension = '.' + args.extension

    #Find the overlapping samples
    #Open each file from the arguments one by one
    for arg in range(0, len(args.file)):
        find_overlaps(args.file[arg], id_dict, pos_dict)

    #print out the overlapping samples from each file
    for arg in range(0, len(args.file)):
        extract_columns(args.file[arg], args.keepcolumns, args.extension, len(args.file), arg, id_dict, pos_dict)

if __name__ == '__main__':
    main()
