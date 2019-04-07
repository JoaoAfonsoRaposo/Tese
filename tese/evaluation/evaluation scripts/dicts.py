
#merge dicts

def intersect_dicts(dA, dX):
    dAX = {}
    for keyA in dA:
        for valueA in dA[keyA]:
            for keyX in dX:
                for valueX in dX[keyX]:
                    if ((valueA[1] > valueX[0]) and (valueA[0] < valueX[1])):
                        concat = keyA + keyX
                        interval = [max(valueA[0], valueX[0]), min(valueA[1], valueX[1])]
                        if dAX.get(concat) == None:
                            dAX[concat] = [interval]
                        else:
                            dAX[concat].append(interval)
    return dAX

def frame_pairs(dictSegs, fps = 0.1):
	totalTime = 0
	for key in dictSegs:
		segTime = 0 
		for value in dictSegs[key]:
			segTime += value[1] - value[0]
		frame_pairs = float(segTime)/fps				
		totalTime += (frame_pairs * (frame_pairs-fps)) / 2
		
	return totalTime




#if((valueA[0] >= valueX[0]) and (valueA[0] < valueX[1]) or (valueA[1] >= valueX[0]) and (valueA[0] < valueX[1])):
