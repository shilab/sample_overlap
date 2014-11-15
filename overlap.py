from __future__ import print_function
import sys
import collections
import argparse

#Overlap samples. Inputs are files, will take any number of files.

def main():
    """Overlap samples"""
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='*', help='Files to overlap')
    args = parser.parse_args()

    id_dict = collections.OrderedDict()
    pos_dict = {}

    #Find the overlapping samples
    for arg in range(0, len(args.file)):
        with open(args.file[arg], 'r') as f:
            header = f.readline().rstrip()
            ids = header.split("\t")
            i = 0
            for id_val in ids:
                i += 1
                if id_val in id_dict:
                    id_dict[id_val] += 1
                else:
                    id_dict[id_val] = 1

                if id_val in pos_dict:
                    pos_dict[id_val] += ","+str(i)
                else:
                    pos_dict[id_val] = str(i)

    #print out the overlapping samples from each file
    for arg in range(0, len(args.file)):
        with open(args.file[arg], 'r') as f:
            pos = []
            for key in id_dict:
                if id_dict[key] == len(sys.argv)-1:
                    ind = pos_dict[key].split(",")
                    pos.append(int(ind[arg]))
            with open(str(args.file[arg]+'.out'), 'w') as fo:
                for line in f:
                    line = line.rstrip()
                    temp = line.split("\t")
                    new_line = [temp[y-1] for y in pos]
                    new_line_str = "\t".join(new_line)
                    print(new_line_str, file=fo)

if __name__ == '__main__':
    main()
