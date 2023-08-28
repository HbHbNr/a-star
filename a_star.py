from typing import List, NamedTuple, Dict
from dataclasses import dataclass
import heapq
import fileinput


class Node(NamedTuple):

    x: int
    y: int

    def heuristicPathLength(self, target: 'Node') -> int:
        diffx = abs(target.x - self.x)
        diffy = abs(target.y - self.y)
        h = diffx + diffy  # Manhattan distance
        if diffx and diffy:
            h -= 1  # count crossroad only once
        return h

    def __repr__(self) -> str:
        return f'({self.x}/{self.y})'


@dataclass(order=True)
class PathNode:

    pathLength: int
    distanceFromStart: int
    node: Node
    parent: Node

    def __repr__(self) -> str:
        return f'({self.pathLength};{self.distanceFromStart};{self.node};{self.parent})'


class Matrix:

    def __init__(self, weights: List[List[int]]) -> None:
        self._maxx = len(weights[0])
        self._maxy = len(weights)
        self._weights = weights
        # print(self._weights)

    def getWeight(self, node: Node) -> int:
        return self._weights[node.y][node.x]


class Matrix5x5(Matrix):

    def __init__(self, matrix: Matrix) -> None:
        self._baseMatrix = matrix
        self._maxx = matrix._maxx * 5
        self._maxy = matrix._maxy * 5
        self._weights = []

    def getWeight(self, node: Node) -> int:
        sectorX = node.x // self._baseMatrix._maxx
        sectorY = node.y // self._baseMatrix._maxy
        inSectorX = node.x % self._baseMatrix._maxx
        inSectorY = node.y % self._baseMatrix._maxy
        weight = self._baseMatrix._weights[inSectorY][inSectorX] + sectorX + sectorY
        weight = ((weight - 1) % 9) + 1
        return weight


class MatrixAStar:

    @classmethod
    def findPath(cls, matrix: Matrix, startNode: Node, targetNode: Node) -> int:
        openList: List[PathNode] = []  # heapq
        # startNode is its own parent:
        openList.append(PathNode(startNode.heuristicPathLength(targetNode), 0, startNode, startNode))
        openListMap: Dict[Node, PathNode] = {}
        closeList: Dict[Node, PathNode] = {}
        while openList:
            # print()
            # print(openList)
            currentPathNode: PathNode = heapq.heappop(openList)
            distanceFromStart: int = currentPathNode.distanceFromStart
            closeList[currentPathNode.node] = currentPathNode
            if currentPathNode.node == targetNode:
                # target reached
                # print('target reached, distance', distanceFromStart)
                break
            else:
                neighbours: List[PathNode] = \
                    cls.findNeighbours(matrix, closeList, distanceFromStart, currentPathNode, targetNode)
                needsHeapify = False
                for neighbour in neighbours:  # all neighbours are not in closeList
                    if neighbour.node not in openListMap:
                        heapq.heappush(openList, neighbour)
                        openListMap[neighbour.node] = neighbour
                        # print('  ', neighbour, ' new', sep='')
                    else:
                        oldneighbour: PathNode = openListMap[neighbour.node]
                        if neighbour.pathLength < oldneighbour.pathLength:  # new neighbour has shorter total path
                            oldneighbour.pathLength = neighbour.pathLength
                            oldneighbour.distanceFromStart = neighbour.distanceFromStart
                            oldneighbour.parent = neighbour.parent
                            needsHeapify = True
                            # print('  ', neighbour, ' updated', sep='')
                        # else:
                            # print('  ', neighbour, ' ignored, because not shorter', sep='')
                if needsHeapify:
                    # print('will reorder heap')
                    heapq.heapify(openList)
        if targetNode in closeList:
            return closeList[targetNode].distanceFromStart
        else:
            # no path between startNode and targetNode
            return -1

    @classmethod
    def findNeighbours(cls, matrix: Matrix, closeList, distanceFromStart: int, currentPathNode: PathNode, targetNode: Node) \
            -> List[PathNode]:
        neighbours: List[PathNode] = []
        for offset in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # right, below, left, above
            neighbourNode = Node(currentPathNode.node.x + offset[0], currentPathNode.node.y + offset[1])
            if neighbourNode.x == matrix._maxx or neighbourNode.y == matrix._maxy \
                    or neighbourNode.x == -1 or neighbourNode.y == -1:
                continue  # ignore coordinates outside of the matrix
            else:
                # print('  Neighbour:', neighbourNode)
                pass
            if neighbourNode not in closeList:
                g = distanceFromStart + matrix.getWeight(neighbourNode)
                h = neighbourNode.heuristicPathLength(targetNode)
                f = g + h
                neighbourPathNode = PathNode(f, g, neighbourNode, currentPathNode.node)
                # print('    ', neighbourPathNode, sep='')
                neighbours.append(neighbourPathNode)
            else:
                # print('    ignored, because in closeList')
                pass
        return neighbours


def readinputfile(inputfile: str) -> List[List[int]]:
    weights: List[List[int]] = []
    for line in fileinput.input(inputfile):
        weights.append([int(c) for c in line.strip()])
    return weights


if __name__ == '__main__':
    # weights = readinputfile('../adventofcode2021/inputfiles/day15_example.txt')
    weights = readinputfile('../adventofcode2021/inputfiles/day15_input.txt')
    startNode = Node(0, 0)

    matrix = Matrix(weights)
    targetNode = Node(len(weights[0]) - 1, len(weights) - 1)
    distanceFromStart = MatrixAStar.findPath(matrix, startNode, targetNode)
    print('Day {:>3}: {}'.format('15a', distanceFromStart))  # e:40 / i:458

    matrix5x5 = Matrix5x5(matrix)
    targetNode = Node(len(weights[0]) * 5 - 1, len(weights) * 5 - 1)
    distanceFromStart = MatrixAStar.findPath(matrix5x5, startNode, targetNode)
    print('Day {:>3}: {}'.format('15b', distanceFromStart))  # e:315 / i:2800
