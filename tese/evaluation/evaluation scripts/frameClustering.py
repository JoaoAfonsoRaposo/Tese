import parse_fc

def intersect_dicts(dAlg, dGT):
    dAlgX = {}
    for keyAlg in dAlg:
        for valueAlg in dAlg[keyAlg]:
            for keyGT in dGT:
                for valueGT in dGT[keyGT]:
                    if ((valueAlg[1] > valueGT[0]) and (valueAlg[0] < valueGT[1])):
                        concat = keyAlg + keyGT
                        interval = [max(valueAlg[0], valueGT[0]), min(valueAlg[1], valueGT[1])]
                        if dAlgX.get(concat) == None:
                            dAlgX[concat] = [interval]
                        else:
                            dAlgX[concat].append(interval)
    return dAlgX


def frame_pairs(dictSegs, fps = 0.5):
	totalTime = 0
	for key in dictSegs:
		segTime = 0 
		for value in dictSegs[key]:
			segTime += value[1] - value[0]
		frame_pairs = float(segTime)/fps				
		totalTime += (frame_pairs * (frame_pairs-fps)) / 2
	return totalTime


def frameClustering(algFile, algName, gtFile, gtName):
    dictAlg = parse_fc.getSegs(algFile, algName)
    dictGT = parse_fc.getSegs(gtFile, gtName)
    intersectedDicts = intersect_dicts(dictAlg, dictGT)
    #print(mergedDicts)
    similar_frame_pairs_alg = frame_pairs(dictAlg)
    similar_frame_pairs_gt = frame_pairs(dictGT)
    similar_frame_pairs_intersection = frame_pairs(intersectedDicts)
    precision = similar_frame_pairs_intersection/similar_frame_pairs_alg
    recall = similar_frame_pairs_intersection/similar_frame_pairs_gt
    f_value = 2*precision*recall / (precision + recall)
    return precision, recall, f_value





