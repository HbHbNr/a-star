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

    def findNeighbourNodes(self, isNodeInCloseList, currentNode: Node, currentParentNode: Node) -> List[Node]:
        neighbourNodes: List[Node] = []
        for offset in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # right, below, left, above
            neighbourNode = Node(currentNode.x + offset[0], currentNode.y + offset[1])
            if neighbourNode == currentParentNode:
                continue  # do not go one step back
            elif neighbourNode.x == self._maxx or neighbourNode.y == self._maxy \
                    or neighbourNode.x == -1 or neighbourNode.y == -1:
                continue  # ignore coordinates outside of the matrix
            # print('  Neighbour:', neighbourNode)
            if isNodeInCloseList(neighbourNode):
                # print('    ignored, because in closeList')
                continue
            neighbourNodes.append(neighbourNode)
        return neighbourNodes

    def getWeight(self, node: Node) -> int:
        return self._weights[node.y][node.x]

    def getMaxX(self):
        return self._maxx

    def getMaxY(self):
        return self._maxy


class Matrix5x5(Matrix):

    def __init__(self, matrix: Matrix) -> None:
        self._baseMatrix = matrix
        self._maxx = matrix._maxx * 5
        self._maxy = matrix._maxy * 5
        self._weights = []

    def getWeight(self, node: Node) -> int:
        sectorX = node.x // self._baseMatrix.getMaxX()
        sectorY = node.y // self._baseMatrix.getMaxY()
        inSectorX = node.x % self._baseMatrix.getMaxX()
        inSectorY = node.y % self._baseMatrix.getMaxY()
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
        # isNodeInCloseList = lambda node: node in closeList
        def isNodeInCloseList(node): return node in closeList
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
                    cls.findValidNeighbours(matrix, isNodeInCloseList, distanceFromStart, currentPathNode, targetNode)
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
    def findValidNeighbours(cls, matrix: Matrix, isNodeInCloseList, distanceFromStart: int, currentPathNode: PathNode,
                            targetNode: Node) -> List[PathNode]:
        currentNode = currentPathNode.node
        neighbourNodes: List[Node] = matrix.findNeighbourNodes(isNodeInCloseList, currentNode, currentPathNode.parent)
        validNeighbours: List[PathNode] = []
        for neighbourNode in neighbourNodes:
            g = distanceFromStart + matrix.getWeight(neighbourNode)
            h = neighbourNode.heuristicPathLength(targetNode)
            f = g + h
            neighbourPathNode = PathNode(f, g, neighbourNode, currentNode)
            # print('    ', neighbourPathNode, sep='')
            validNeighbours.append(neighbourPathNode)
        return validNeighbours


def readinputfile(inputfile: str) -> List[List[int]]:
    weights: List[List[int]] = []
    for line in fileinput.input(inputfile):
        weights.append([int(c) for c in line.strip()])
    return weights


def main():
    # weights = readinputfile('inputfiles/aoc2021_day15_example.txt')
    weights = readinputfile('inputfiles/aoc2021_day15_input.txt')
    startNode = Node(0, 0)

    matrix = Matrix(weights)
    targetNode = Node(len(weights[0]) - 1, len(weights) - 1)
    distanceFromStart = MatrixAStar.findPath(matrix, startNode, targetNode)
    print('Day {:>3}: {}'.format('15a', distanceFromStart))  # e:40 / i:458

    matrix5x5 = Matrix5x5(matrix)
    targetNode = Node(len(weights[0]) * 5 - 1, len(weights) * 5 - 1)
    distanceFromStart = MatrixAStar.findPath(matrix5x5, startNode, targetNode)
    print('Day {:>3}: {}'.format('15b', distanceFromStart))  # e:315 / i:2800


if __name__ == '__main__':
    main()
