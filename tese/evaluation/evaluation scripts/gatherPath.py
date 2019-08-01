import sys, getopt
import os

def main(algName, outP):
    path = 'Results/' + algName
    evaluationFiles = os.listdir(path)
    for i in range(0, len(evaluationFiles)-1):
        if evaluationFiles[i] == 'Aggregate':
            evaluationFiles.pop(i)
            break
    for i in range(0, len(evaluationFiles)):
        evaluationFiles[i] = path + '/' + evaluationFiles[i] 
    fc_precision = 0
    fc_recall = 0
    fc_f_value = 0
    mttg = 0
    mgtt = 0
    br_precision = 0
    br_recall = 0
    br_f_value = 0
    fc_metrics = [fc_precision, fc_recall, fc_f_value]
    br_metrics = [mttg, mgtt, br_precision, br_recall, br_f_value]
    nr_of_files = 0
    for evaluationFile in evaluationFiles:
        if evaluationFile.endswith(".csv"):
            nr_of_files += 1
            inFile = open(evaluationFile, "r")
            fc_results = inFile.readline().split('\t')
            br_results = inFile.readline().split('\t')
            for i in range(0, 3):
                fc_metrics[i] += float(fc_results[i])
            for i in range(0, 5):
                br_metrics[i] += float(br_results[i])
    for i in range(0, 3):
        fc_metrics[i] = fc_metrics[i]/nr_of_files
    for i in range(0, 5):
        br_metrics[i] = br_metrics[i]/nr_of_files
    outPath = "Results/" + algName + "/Aggregate/" + outP
    writeResults(outPath, fc_metrics, br_metrics)
    
def writeResults(outputPath, fc_results, br_results):
    outFile = open(outputPath, "w")
    outFile.write("fc_results: ")
    for result in fc_results:
        outFile.write(str(result))
        outFile.write('\t')
    outFile.write('\n')
    outFile.write("br_results: ") 
    for result in br_results:
        outFile.write(str(result))
        outFile.write('\t')

    
if __name__ == "__main__":
   main(sys.argv[1], sys.argv[2])	
