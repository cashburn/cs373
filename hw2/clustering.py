import random
import math
import csv
import sys
import pandas as pd

if len(sys.argv) != 4:
    print 'Usage: python clustering.py ./some/path/file_name.csv K ac'
    quit()

K = sys.argv[2]
data = pd.read_csv(sys.argv[1], sep=',', quotechar='"', header=0)
data = data[['latitude', 'longitude', 'reviewCount', 'checkins']]
X = data.as_matrix()
n = len(X)

class Point(object):
    def __init__(self, array, ind):
        self.array = array
        self.index = ind
        self.latitude = array[0]
        self.longitude = array[1]
        self.reviewCount = array[2]
        self.checkins = array[3]
        self.cluster = 0
    def toString(self):
        return '[{0},{1},{2},{3}]'.format(self.array[0],
                                          self.array[1],
                                          self.array[2],
                                          self.array[3])
    def distance(self, point):
        squares = list()
        for i in range(0, 4):
            squares.append(self.array[i] - point.array[i])
        sumA = 0
        for x in squares:
            sumA += math.pow(x, 2)
        return math.sqrt(sumA)
    def sqDistance(self, point):
        squares = list()
        for i in range(0, 4):
            squares.append(self.array[i] - point.array[i])
        sumA = 0
        for x in squares:
            sumA += math.pow(x, 2)
        return sumA

def wc_sse(points, centroids):
    summ = 0
    for i in points:
        summ += i.sqDistance(centroids[i.cluster])
    return summ

def kmeans(points, k):
    centroids = list()
    for i in range(0, k):
        a = random.randint(0, n - 1)
        centroids.append(points[a])
    condition = True
    sse = 0
    while condition:
        for i in range(0, n):
            distance = -1
            for j in range(0, k):
                dist = points[i].distance(centroids[j])
                if dist < distance or distance < 0:
                    distance = dist
                    points[i].cluster = j
        clustersize = list()
        sums = list()
        for i in range(0, k):
            sums.append([0, 0, 0, 0])
            clustersize.append(0)
        for i in points:
            clustersize[i.cluster] += 1
            for j in range(0, 4):
                sums[i.cluster][j] += i.array[j]
        for i in range(0, k):
            for j in range(0, 4):
                if clustersize[i] != 0:
                    sums[i][j] = sums[i][j] / clustersize[i]
                else:
                    sums[i][j] = 0
            newpoint = Point(sums[i], -1)
            centroids[i] = newpoint
        sse_new = wc_sse(points, centroids)
        if math.fabs(sse_new - sse) < 0.005:
            condition = False
        print str(sse) + ',' + str(sse_new)
        sse = sse_new

    with open('points.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['cluster'])
        for i in points:
            writer.writerow([i.cluster])
    with open('centroids.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['latitude', 'longitude', 'reviewCount', 'checkins'])
        for i in range(0, k):
            writer.writerow(centroids[i].array)

    print 'WC-SSE=' + str(wc_sse(points, centroids))

    for i in range(0, k):
        print 'Centroid' + str(i+1) + '=' + centroids[i].toString()

def agglomerative(points):
    pass
pointList = list()
for index in range(0, n):
    pointList.append(Point(X[index], index))
if sys.argv[3] == 'km':
    kmeans(pointList, int(K))
elif sys.argv[3] == 'ac':
    agglomerative(pointList)
else:
    print 'Invalid clustering method'
