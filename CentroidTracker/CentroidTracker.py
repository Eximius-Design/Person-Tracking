from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
nextObjectID = 0
objects = OrderedDict()
disappeared = OrderedDict()
maxDisappeared =10 
def register(centroid):
   global nextObjectID
   objects[nextObjectID] = centroid
   disappeared[nextObjectID] = 0
   nextObjectID += 1
def deregister(objectID):
   del objects[objectID]
   del disappeared[objectID]
def update(rects):
	if len(rects) == 0:
		for objectID in disappeared.keys():
			disappeared[objectID] += 1
			if disappeared[objectID] > maxDisappeared:
				deregister(objectID)
	inputCentroids = np.zeros((len(rects), 2), dtype="int")
	for (i, (startX, startY, endX, endY)) in enumerate(rects):
		cY = int((startX + endX) / 2.0)
		cX = int((startY + endY) / 2.0)
		inputCentroids[i] = (cX, cY)
		#print(i,"-------------------------",inputCentroids[i])
	if len(objects) == 0:
		print("hello sudheep")
		for i in range(0, len(inputCentroids)):
			register(inputCentroids[i])
	else:
		objectIDs = list(objects.keys())
		objectCentroids = list(objects.values())
		D = dist.cdist(np.array(objectCentroids), inputCentroids)
		rows = D.min(axis=1).argsort()
		cols = D.argmin(axis=1)[rows]
		usedRows = set()
		usedCols = set()
		for (row, col) in zip(rows, cols):
			if row in usedRows or col in usedCols:
				continue
			objectID = objectIDs[row]
			objects[objectID] = inputCentroids[col]
			disappeared[objectID] = 0
			usedRows.add(row)
			usedCols.add(col)
			unusedRows = set(range(0, D.shape[0])).difference(usedRows)
			unusedCols = set(range(0, D.shape[1])).difference(usedCols)
			if D.shape[0] >= D.shape[1]:
				for row in unusedRows:
					objectID = objectIDs[row]
					disappeared[objectID] += 1
					if disappeared[objectID] > maxDisappeared:
						deregister(objectID)
					else:
						for col in unusedCols:
							register(inputCentroids[col])
	return objects
   
