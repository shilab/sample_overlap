from __future__ import print_function
import sys
import collections
import argparse
import gzip

#Overlap samples from different files.
#Takes files from command line, and overlaps based on header and sample IDs.
#Currently only works on tab-delimited files.

def find_duplicates(ids):
    from collections import Counter
    unique_ids = set(ids)
    id_count = Counter(ids)
    for id in unique_ids:
        if id_count[id] > 1:
            print(id + ' is not unique')
    raise Exception('Non-unique IDs in header')

def find_overlaps(fileobj, id_dict, pos_dict):
        #Read the header and split it
        header = fileobj.readline().rstrip()
        ids = header.split("\t")
        if len(ids) > len(set(ids)):
            find_duplicates(ids)
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

def extract_columns(fileobj, filename, keep_columns, extension, numfiles, arg, id_dict, pos_dict):
#with open(filename, 'r') as f:
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
        if '.gz' in str(filename):
            filename = str(filename).replace('.gz','') + '.gz'
            with gzip.open(str(filename), 'wb') as fo:
                write_file(fileobj, fo, pos)
        else:
            with open(str(filename), 'w') as fo:
                write_file(fileobj, fo, pos)

def write_file(readfile, writefile, pos):
    for line in readfile:
        #Split each line, reorder using the position array,
        #join to string and write to *.out file
        line = line.rstrip()
        temp = line.split("\t")
        new_line = [temp[y-1] for y in pos]
        new_line_str = "\t".join(new_line)
        print(new_line_str, file=writefile)

def get_extension(extension):
    if extension and '.' not in extension:
        extension = '.' + extension
    return extension

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

    args.extension = get_extension(args.extension)

    #Find the overlapping samples
    #Open each file from the arguments one by one
    for arg in range(0, len(args.file)):
        if '.gz' in args.file[arg]:
            with gzip.open(args.file[arg], 'rb') as f:
                find_overlaps(f, id_dict, pos_dict)
        else:
            with open(args.file[arg], 'r') as f:
                find_overlaps(f, id_dict, pos_dict)

    #print out the overlapping samples from each file
    for arg in range(0, len(args.file)):
        if '.gz' in args.file[arg]:
            with gzip.open(args.file[arg], 'rb') as f:
                extract_columns(f, args.file[arg], args.keepcolumns, args.extension, len(args.file), arg, id_dict, pos_dict)
        else:
            with open(args.file[arg], 'r') as f:
                extract_columns(f, args.file[arg], args.keepcolumns, args.extension, len(args.file), arg, id_dict, pos_dict)


if __name__ == '__main__':
    main()
