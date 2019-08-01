import sys
import numpy as np

def main(files):
    outputPath = "final/" + files[-1]
    del(files[0])
    del(files[-1])
    
    fc_results = [0, 0, 0]
    br_results = [0, 0, 0, 0, 0]
    
    n_files= 0
    for file in files:
        f = open(file, 'r')
        fc = f.readline().split('\t')
        br = f.readline().split('\t')
        del(fc[-1])
        del(br[-1])
        for i in range(0, len(fc)):
            fc_results[i] += float(fc[i])
        for i in range(0, len(br)):
            br_results[i] += float(br[i])
        n_files += 1

    for i in range(0, len(fc_results)):
        fc_results[i] /= n_files
    for i in range(0, len(br_results)):
        br_results[i] /= n_files
        
    outF = open(outputPath, 'w')
    for result in fc_results:
        outF.write(str(result))
        outF.write('\t')
    outF.write('\n')
    for result in br_results:
        outF.write(str(result))
        outF.write('\t')
        
    print(fc_results)
    print(br_results)
    
if __name__ == "__main__":
    main(sys.argv)
