import random
import math
import csv
import sys
from Queue import PriorityQueue
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
        self.distances = [None] * n
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
        return sumA

class Cluster(object):
    def __init__(self, pointArray, clusterIndex):
        self.points = pointArray
        self.distances = [None]*n
        self.index = clusterIndex
    def avgDist(self, cluster):
        clustSum = 0
        linkCount = 0
        for i in self.points:
            for j in cluster.points:
                clustSum += i.distance(j)
                linkCount += 1
        return clustSum / linkCount
    def merge(self, clusters, rightI):
        for i in range(n):
            if clusters[i] is None:
                continue
            if self.distances[i] is None:
                print str(i)
            oldSize1 = len(self.points) * len(clusters[i].points)
            oldSize2 = len(clusters[rightI].points) * len(clusters[i].points)
            oldSum1 = self.distances[i] * oldSize1
            oldSum2 = clusters[rightI].distances[i] * oldSize2
            newAvg = (oldSum1 + oldSum2) / (oldSize1 + oldSize2)
            self.distances[i] = newAvg
            clusters[i].distances[self.index] = newAvg
        for i in range(n):
            if clusters[i] is None:
                continue
            clusters[i].distances[rightI] = None
        self.points += clusters[rightI].points
        clusters[rightI] = None

def wc_sse(points, centroids):
    summ = 0
    for i in points:
        summ += i.distance(centroids[i.cluster])
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
        if math.fabs(sse_new - sse) < 0.025:
            condition = False
        #print str(sse) + ',' + str(sse_new)
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

def agglomerative_preprocess(clusters, q):
    for i in range(0, n):
        for j in range(0, n):
            if i == j:
                clusters[i].distances[j] = 0
                continue
            if clusters[j].distances[i] != None:
                avg = clusters[j].distances[i]
            else:
                avg = clusters[i].avgDist(clusters[j])
                q.put((avg, [i, j]))
            clusters[i].distances[j] = avg
            clusters[i].points[0].cluster = i

def agglomerative(clusters, k):
    q = PriorityQueue()
    print 'Precomputing distances'
    agglomerative_preprocess(clusters, q)
    print 'Finished preprocessing for k=' + str(k)

    numClusters = len(clusters)

    while numClusters > k:
        minI = q.get()[1]
        if clusters[minI[0]] is None or clusters[minI[1]] is None:
            continue
            #print str(i) + ': ' + str(minI) + ' at ' + str(minIAvg)
        clusters[minI[0]].merge(clusters, minI[1])
        numClusters -= 1
        print 'clustered ' + str(minI[1]) + ' into ' + str(minI[0])
        print str(numClusters) + ' clusters'
    print 'finished clustering'
    with open('points.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['index', 'cluster'])
        count = 0
        for i in clusters:
            if i is None:
                continue
            for j in i.points:
                writer.writerow([j.index, count])
            count += 1
    with open('centroids.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['latitude', 'longitude', 'reviewCount', 'checkins'])
        for i in clusters:
            if i is None:
                continue
            writer.writerow(i.points[0].array)
pointList = list()
clusterList = list()
for index in range(0, n):
    p = Point(X[index], index)
    pointList.append(p)
    clusterList.append(Cluster([p], index))
if sys.argv[3] == 'km':
    kmeans(pointList, int(K))
elif sys.argv[3] == 'ac':
    agglomerative(clusterList, int(K))
else:
    print 'Invalid clustering method'
