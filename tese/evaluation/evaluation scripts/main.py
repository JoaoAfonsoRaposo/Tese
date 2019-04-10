import sys, getopt
import frameClustering
import boundaryRetrieval

def main(algFile, algName, gtFile, gtName):
    fc_results = frameClustering.frameClustering(algFile, algName, gtFile, gtName)
    br_results = boundaryRetrieval.boundaryRetrieval(algFile, algName, gtFile, gtName)
    outputPath = setFileOutputPath(algFile, algName)
    writeResults(outputPath, fc_results, br_results)
     
def writeResults(outputPath, fc_results, br_results):
    outFile = open(outputPath, "w")
    for result in fc_results:
        outFile.write(str(result))
        outFile.write('\t')
    outFile.write('\n')    
    for result in br_results:
        outFile.write(str(result))
        outFile.write('\t')
    
def setFileOutputPath(filePath, algName):
    i = 0
    for c in reversed(filePath):
        if(c == "/"):
            break
        i+=1
    path = filePath[-i:]
    outputPath = 'Results/' + algName + '/' + path
    return outputPath

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])	


   #outFile.write("FC:")
    #FCresults = "precision:" + str(fc_precision) + "recall:" + str(fc_recall) + "f_value:" + str(fc_fValue)
    #outFile.write(FCresults)
    #outFile.write("BR:")
    #BRresults = "mttg:" + str(mttg) + "mgtt" + str(mgtt) + "precision:" + str(fc_precision) + "recall:" + str(fc_recall) + "f_value:" + str(fc_fValue)
