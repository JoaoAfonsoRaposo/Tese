import numpy as np
import math
import parse_br

def hitRate(gtBounds, algBounds, th=3):
    totalEst = len(algBounds)
    totalBound = len(gtBounds)
    trueEst = 0
    trueBound = 0
    for algBoundary in algBounds:
        for gtBoundary in gtBounds:
            if abs(algBoundary - gtBoundary) < th:
                trueEst += 1
                break
    for gtBoundary in gtBounds:
        for algBoundary in algBounds:
            if abs(gtBoundary - algBoundary) < th:
                trueBound += 1
                break
    if(totalEst == 0):
        print(algBounds, totalEst)
        print(gtBounds, totalBound)
        precision = 1
    else:
        precision = trueEst/(totalEst)
    if(totalBound == 0):
        print(algBounds, totalEst)
        print(gtBounds, totalBound)
        recall = 1
    else:
        recall = trueBound/(totalBound)
    if (precision or recall) == 0:
        return 0, 0, 0
    fValue = 2*precision*recall/(precision + recall)
    return precision, recall, fValue


def medianTrueToGuess(gtBounds, algBounds):
    trueToGuess = []
    for gtBoundary in gtBounds:
        min_diff = math.inf
        for algBoundary in algBounds:
            diff = abs(gtBoundary - algBoundary) 
            if diff < min_diff:
                min_diff = diff
        trueToGuess.append(min_diff)
    time_btw_ttg = np.array(trueToGuess)
    median_time_btw_ttg = np.median(time_btw_ttg)
    return median_time_btw_ttg
    

def medianGuessToTrue(gtBounds, algBounds):
    guessToTrue = []
    for algBoundary in algBounds:
        min_diff = math.inf
        for gtBoundary in gtBounds:
            diff = abs(algBoundary - gtBoundary) 
            if diff < min_diff:
                min_diff = diff
        guessToTrue.append(min_diff)
    time_btw_gtt = np.array(guessToTrue)
    median_time_btw_gtt = np.median(time_btw_gtt)
    return median_time_btw_gtt

def boundaryRetrieval(algFile, algName, gtFile, gtName):
    algBounds =  parse_br.getBounds(algFile, algName)
    gtBounds = parse_br.getBounds(gtFile, gtName)
    hR = hitRate(gtBounds, algBounds, th=3)
    mttg = medianTrueToGuess(gtBounds, algBounds)
    mgtt = medianGuessToTrue(gtBounds, algBounds)
    precision = hR[0]
    recall = hR[1]
    f_value = hR[2]
    return mttg, mgtt, precision, recall, f_value

'''gtB = [1, 3, 7, 12, 22, 26, 35, 43, 67]
algB = [1.2, 4, 7.4, 12.2, 25, 26.4]
hit_rate = hitRate(gtB, algB, th = 0.5)
median_ttg = medianTrueToGuess(gtB, algB)
median_gtt = medianGuessToTrue(gtB, algB)
print("precision: ", hit_rate[0])
print("recall: ", hit_rate[1])
print("f-Value: ", hit_rate[2])
print("median_ttg: ", median_ttg)
print("median_gtt: ", median_gtt)'''
#precision = 0.6666
#recall = 0.4444
#f-value = 0.5333
#median_ttg = 1
#median_gtt = 0.4












