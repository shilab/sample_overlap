from __future__ import print_function
import sys
import collections

id_dict = collections.OrderedDict()
pos_dict = {}


for x in range (1,len(sys.argv)):
    #print sys.argv[x]
    with open(sys.argv[x], 'r') as f:
        header = f.readline().rstrip()
        #print(first_line)
        ids=header.split("\t")
        i=0
        for vals in ids:
            i+=1
            if vals in id_dict:
                id_dict[vals]+=1
            else:
                id_dict[vals]=1

            if vals in pos_dict:
                pos_dict[vals]+=","+str(i)
            else:
                pos_dict[vals]=str(i)

for x in range (1,len(sys.argv)):
    with open(sys.argv[x], 'r') as f:
        with open(str(sys.argv[x]+'.out'),'w') as fo:
            for line in f:
                li = line.rstrip()
                temp = li.split("\t")
                pos = []
                for key in id_dict:
                    if id_dict[key]==len(sys.argv)-1:
                        ind = pos_dict[key].split(",")
                        pos.append(int(ind[x-1]))
                new_line=[temp[y-1] for y in pos] 
                new_line_str="\t".join(new_line)
                print(new_line_str, file=fo)
