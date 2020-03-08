import math
import sys

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


def set_correct_normal(plane,possible_internal_points): #Make the orientation of Normal correct
    for point in possible_internal_points:
        dist = dotProduct(plane.normal,point - plane.pointA)
        if dist != 0 :
            if(dist > 10**-10):
                plane.normal.x = -1*plane.normal.x
                plane.normal.y = -1*plane.normal.y
                plane.normal.z = -1*plane.normal.z
                return

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
        return self.distToPoint(Point(0,0,0,))

    def distToPoint(self, other):
        """
        Calculates euqlidean distance to other point
        """
        return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2)

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))


class Edge:
    def __init__(self, pointA, pointB):
        self.pointA = pointA
        self.pointB = pointB
        self.length = pointA.distToPoint(pointB)

    def distToPoint(self, pointX):
        vecAX = pointX - self.pointA
        vecAB = self.pointB - self.pointA
        crossVec = cross(vecAX, vecAB)
        if(vecAB.length()==0):
            return None
        else:
            return crossVec.length()/vecAB.length()

    def __eq__(self, other):
        if ((self.pointA == other.pointA)and(self.pointB == other.pointB)) or ((self.pointB == other.pointA)and(self.pointA == other.pointB)):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.pointA, self.pointB))

    def __str__(self):
        return "Edge " + "A: " + str(self.pointA) + "-B: " + str(self.pointB)



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
        self.pointsToCheck = []

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

    def calculatePointsToCheck(self, cloud):
        ret = []
        if cloud or len(cloud)>0:
            for point in cloud:
                if self.distToPoint(point) > 10**-10:
                    self.pointsToCheck.append(point)
                else:
                    ret.append(point)
        return ret

    def getEdges(self):
        return[self.edge1, self.edge2, self.edge3]

    def __eq__(self, other):
        if (self.pointA == other.pointA or self.pointA == other.pointB or self.pointA == other.pointC) and (self.pointB == other.pointA or self.pointB == other.pointB or self.pointB == other.pointC) and (self.pointC == other.pointA or self.pointC == other.pointB or self.pointC == other.pointC):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.pointA, self.pointB, self.pointC))

    def __str__(self):
        return "Plane: " + "A: " + str(self.pointA) + "B: " + str(self.pointB) + "C: " + str(self.pointC)

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
        return 0, cloud[0]
    #znajdź początkową krawędź, tam gdzie odległość między maxymalnymi punktami jest największa
    max_edge = Edge(maxes[0], maxes[1])
    for point1 in maxes:
        for point2 in maxes:
            tmpEdge = Edge(point1, point2)
            max_edge = tmpEdge if tmpEdge.length > max_edge.length else max_edge

    #jeżeli wymiar to 1, to nic dalej nie stworzymy, zwracam wymiar i wierzchołek/prostą
    if dim == 1:
        return 1, max_edge

    #W chumrze punktów znajdź punkt najbardziej odległy od krawędzi
    maxEdgeDist = 0
    for point in cloud:
        tmpDist = max_edge.distToPoint(point)
        if tmpDist > maxEdgeDist:
            maxDistEdgePoint = point
            maxEdgeDist = tmpDist

    initialPlane = Plane(max_edge.pointA, max_edge.pointB, maxDistEdgePoint)

    #jeśli wymiar jest 2, to nie stworzymy czworościanu. Zwracam wymiar i startowy plane, bo można z niego tworzyć otoczkę w 2d
    if dim == 2:
        return 2, initialPlane

    #Znajdź punkt najbardziej odległy od utworzonego planu

    maxPlaneDist = 0
    for point in cloud:
        tmpDist = initialPlane.distToPoint(point)
        if tmpDist > maxPlaneDist:
            maxDistPlanePoint = point
            maxPlaneDist = tmpDist

    return 3, initialPlane.pointA, initialPlane.pointB, initialPlane.pointC, maxDistPlanePoint


def calcHorizon(workingPlane, visitedPlanes, eyePoint, edgeList, hullPlanes):

    if workingPlane.distToPoint(eyePoint) > 10 ** -10:
        visitedPlanes.append(workingPlane)
        edges = workingPlane.getEdges()

        # dla każdej krawędzi znajdź sąsiadujące płaszczyzny
        for edge in edges:             
            neighbour = findNeighbour(workingPlane, edge, hullPlanes)
            #jeżeli nie sprawdzaliśmy jeszcze sąsiadującej płaszczyzny to szukamy horyzontu z jej perspektywy
            if neighbour and neighbour not in visitedPlanes:
                end = calcHorizon(neighbour, visitedPlanes, eyePoint, edgeList, hullPlanes)
                if end:
                    edgeList.add(edge)
        return False
    else:
        return True
    
def findNeighbour(workingPlane, edge, hullPlanes):
    for plane in hullPlanes:
        edges = plane.getEdges()
        if (plane != workingPlane) and (edge in edges):
                    return plane

cloud = []
cloud.append(Point(0,0,0))
cloud.append(Point(0,0,1))
cloud.append(Point(0,1,0))
cloud.append(Point(0,1,1))
cloud.append(Point(1,0,0))
cloud.append(Point(1,0,1))
cloud.append(Point(1,1,0))
cloud.append(Point(1,1,1))
cloud.append(Point(2,1,0.5))
cloud.append(Point(2,0.5,1))
cloud.append(Point(2,5,1))
cloud.append(Point(2,3,3))
cloud.append(Point(5,3,1))
cloud.append(Point(2,0.5,5))



ret = CreateSimplex(cloud)
dim = ret[0]
if dim == 0:
    print("Podano tylko jeden punkt")
    exit()
if dim == 1:
    print("Wszytkie punkty leżą na prostej")
    exit()
if dim == 2:
    print("Wszystkie punkty leżą na płaszczyźnie")
    exit()
if dim == 3:
    point1 = ret[1]
    point2 = ret[2]
    point3 = ret[3]
    point4 = ret[4]
    print("Wyznaczyłem 4 punkty startowego czworościanu " + str(point1) + " " + str(point2) + " " + str(point3) + " " + str(point4))

    #startowe płaszczyzny
    plane1 = Plane(point1, point2, point3)
    plane3 = Plane(point1, point2, point4)
    plane2 = Plane(point2, point3, point4)
    plane4 = Plane(point3, point1, point4)

    internalPoints = [point1,point2,point3,point4]
    set_correct_normal(plane1, internalPoints)
    set_correct_normal(plane2, internalPoints)
    set_correct_normal(plane3, internalPoints)
    set_correct_normal(plane4, internalPoints)

    cloud = plane1.calculatePointsToCheck(cloud)
    cloud = plane2.calculatePointsToCheck(cloud)
    cloud = plane3.calculatePointsToCheck(cloud)
    cloud = plane4.calculatePointsToCheck(cloud)

    hullPlanes = []
    hullPlanes.append(plane1)
    hullPlanes.append(plane2)
    hullPlanes.append(plane3)
    hullPlanes.append(plane4)

    AnyLeft = True

    while AnyLeft:
        AnyLeft = False
        for workingPlane in hullPlanes:
            if len(workingPlane.pointsToCheck)>0:
                AnyLeft = True
                eyePointDist = 0
                #find eye point
                for point in workingPlane.pointsToCheck:
                    tempDist = workingPlane.distToPoint(point)
                    if tempDist > eyePointDist:
                        eyePointDist = tempDist
                        eyePoint = point

                edgeList = set()
                visitedPlanes =[]

                calcHorizon(workingPlane, visitedPlanes, eyePoint, edgeList, hullPlanes)

                pointsToCheck = set()
                #All visited
                for internalPlane in visitedPlanes:
                    hullPlanes.remove(internalPlane)
                    pointsToCheck.union(internalPlane.pointsToCheck)

                for edge in edgeList:
                    newPlane = Plane(edge.pointA, edge.pointB, eyePoint)
                    set_correct_normal(newPlane, internalPoints)
                    pointsToCheck = newPlane.calculatePointsToCheck(pointsToCheck)
                    hullPlanes.append(newPlane)

    hullPoints = set()
    for hullPlane in hullPlanes:
        hullPoints.add(hullPlane.pointA)
        hullPoints.add(hullPlane.pointB)
        hullPoints.add(hullPlane.pointC)

    print("punkty w otoczce")
    for hullPoint in hullPoints:
        print(str(hullPoint))


