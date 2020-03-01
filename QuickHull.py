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
        return math.sqrt(self.x**2, self.y**2, self.z**2)

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


class Edge:
    def __init__(self, pointA, pointB):
        self.pointA = pointA
        self.pointB = pointB


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


def CreateSimplex(cloud):
    """
    Find a maximal simplex of the current dimension. In our case, find 4 points which define maximal tetrahedron,
    and create the tetrahedron which will be our seed partial answer.
    :return:
    """
    max_ = Point()
    min_X = Point()
    max_Y = Point()
    min_Y = Point()
    max_Z = Point()
    min_Z = Point

    for point in cloud:

        if point[0] > max_x[0]:
            max_x = point
        if point[1] > max_y[1]:
            max_y = point
        if point[2] > max_z[2]:
            max_z = point
