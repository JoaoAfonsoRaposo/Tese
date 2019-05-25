#edit QM segmentation files to add the timestamp of the last segment

import sys, getopt
import pdb

def editQMfile(qmFile, gtFile):
    gtf = open(gtFile, 'r').readlines()
    end_time = gtf[-1].split('\t')[1]
    lines = open(qmFile, 'r').readlines()
    last_line = lines[-1].split(',')
    last_line = last_line[:3]
    delimiter = len(last_line[1]) + 2
    last_line[-1] = last_line[-1][:delimiter]
    new_last_line = str('')
    for elem in last_line:
        new_last_line = new_last_line + elem + ','
    new_last_line += end_time
    lines[-1] = new_last_line
    open(qmFile, 'w').writelines(lines)

if __name__ == "__main__":
    editQMfile(sys.argv[1], sys.argv[2])	
