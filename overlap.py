from __future__ import print_function
import sys
import collections

id_dict = collections.OrderedDict()
pos_dict = {}


for x in range (1,len(sys.argv)):
    with open(sys.argv[x], 'r') as f:
        header = f.readline().rstrip()
        ids=header.split("\t")
        i=0
        for id in ids:
            i+=1
            if id in id_dict:
                id_dict[id]+=1
            else:
                id_dict[id]=1

            if id in pos_dict:
                pos_dict[id]+=","+str(i)
            else:
                pos_dict[id]=str(i)

for x in range (1,len(sys.argv)):
    with open(sys.argv[x], 'r') as f:
        pos = []
        for key in id_dict:
            if id_dict[key]==len(sys.argv)-1:
                ind = pos_dict[key].split(",")
                pos.append(int(ind[x-1]))
        with open(str(sys.argv[x]+'.out'),'w') as fo:
            for line in f:
                line = line.rstrip()
                temp = line.split("\t")
                new_line=[temp[y-1] for y in pos] 
                new_line_str="\t".join(new_line)
                print(new_line_str, file=fo)
