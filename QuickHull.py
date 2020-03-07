import math
import sys

#https://github.com/swapnil96/Convex-hull/blob/master/hull.py


def cross(pointA, pointB):
    """
    cross product
    """
    x = (pointA.y*pointB.z) - (pointA.z*pointB.y)
    y = (pointA.z*pointB.x) - (pointA.x*pointB.z)
    z = (pointA.x*pointB.y) - (pointA.y*pointB.x)
    return Point(x, y, z)


def dotProduct(pointA, pointB):
    """
    dot product
    :param pointA:
    :param pointB:
    :return:
    """
    return pointA.x*pointB.x + pointA.y*pointB.y + pointA.z*pointB.z


class Point:
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z
    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y, self.z-other.z)

    def __add__(self,other):
        return Point(self.x+other.x, self.y+other.y, self.z+other.z)

    def length(self):
        """
        calculates Euqlidean distance to 0,0,0
        """
        return length(self, Point(0,0,0,))

    def length(self, other):
        """
        Calculates euqlidean distance to other point
        """
        return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2)

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


class Edge:
    def __init__(self, pointA, pointB):
        self.pointA = pointA
        self.pointB = pointB
        self.length = pointA.length(pointB) 

    def distToPoint(self, pointX):
        vecAX = pointX - self.pointA
        vecAB = self.pointB - self.pointA
        crossVec = cross(vecAX, vecAB)
        if(vecAB.length()==0):
            return None
        else:
            return crossVec.length()/vecAB.length()




class Plane:
    def __init__(self, pointA, pointB, pointC):
        self.pointA = pointA
        self.pointB = pointB
        self.pointC = pointC
        self.normal = None
        self.distance = None
        self.calcNorm()
        self.to_do = set()
        self.edge1 = Edge(pointA, pointB)
        self.edge2 = Edge(pointB, pointC)
        self.edge3 = Edge(pointC, pointA)

    def calcNorm(self):
        """
        calculates normal to the plane
        :return:
        """
        point1 = self.pointA - self.pointB
        point2 = self.pointB - self.pointC
        normVector = cross(point1, point2)
        length = normVector.length()
        normVector.x = normVector.x / length
        normVector.y = normVector.y / length
        normVector.z = normVector.z / length
        self.normal = normVector
        self.distance = dotProduct(self.normal, self.pointA)

    def distToPoint(self, pointX):
		return (dotProduct(self.normal,pointX - self.pointA))


def CreateSimplex(cloud):
    """
    Find a maximal simplex of the current dimension. In our case, find 4 points which define maximal tetrahedron,
    and create the tetrahedron which will be our seed partial answer.
    :return:
    """
    max_x = Point(-10**9,0,0)
    min_x = Point(10**9,0,0)
    max_y = Point(0,-10**9,0)
    min_y = Point(0,10**9,0)
    max_z = Point(0,0,-10**9)
    min_z = Point(0,0,10**9)
    
    #znajdź punkty skraje w każdej osi
    for point in cloud:
        if point.x > max_x.x:
            max_x = point
        if point.x < min_x.x:
            min_x = point
        if point.y > max_y.y:
            max_y = point
        if point.y < min_y.y:
            min_y = point
        if point.z > max_z.z:
            max_z = point
        if point.z < min_z.z:
            min_z = point
    
    maxes = []
    if max_x != min_x:
        maxes.append(max_x)
        maxes.append(min_x)
    if max_y != min_y:
        maxes.append(max_y)
        maxes.append(min_y)
    if max_z != min_z:
        maxes.append(max_z)
        maxes.append(min_z)

    dim = len(maxes)/2

    # jeśli pinkty są w 0 wumiarach, to mamy tylko jeden punkt, bez sensu coś liczyć, zwracam wymiar i jedyny punkt
    if dim == 0:
        return 0, cloud[0], None, None, None
    #znajdź początkową krawędź, tam gdzie odległość między maxymalnymi punktami jest największa
    max_edge = Edge(maxes[0], maxes[1])
    for point1 in maxes:
        for point2 in maxes:
            tmpEdge = Edge(point1, point2)
            max_edge = tmpEdge if tmpEdge.length > max_edge.length else max_edge

    #jeżeli wymiar to 1, to nic dalej nie stworzymy, zwracam wymiar i wierzchołek/prostą
    if dim == 1:
        return 1, max_edge.pointA, max_edge.pointB, None, None

    #W chumrze punktów znajdź punkt najbardziej odległy od krawędzi
    maxEdgeDist = 0
    for point in cloud:
        tmpDist = max_edge.distToPoint(point)
        if tmpDist > maxEdgeDist:
            maxDistEdgePoint = point
            maxEdgeDist = tmpDist

    initialPlane = Plane(max_edge[0], max_edge[1], maxDistEdgePoint)

    #jeśli wymiar jest 2, to nie stworzymy czworościanu. Zwracam wymiar i startowy plane, bo można z niego tworzyć otoczkę w 2d
    if dim == 2:
        return 2, initialPlane.PointA, initialPlane.pointB, initialPlane.pointC, None

    #Znajdź punkt najbardziej odległy od utworzonego planu

    maxPlaneDist = 0
    for point in cloud:
        tmpDist = initialPlane.distToPoint(point)
        if tmpDist > maxPlaneDist:
            maxDistPlanePoint = point
            maxPlaneDist = tmpDist

    return 3, initialPlane.PointA, initialPlane.pointB, initialPlane.pointC, maxDistPlanePoint

    





        
    

    
