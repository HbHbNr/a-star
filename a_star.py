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
        print(self._weights)

    def getWeight(self, node: Node) -> int:
        return self._weights[node.y][node.x]


class MatrixAStar:

    @classmethod
    def findPath(cls, matrix: Matrix, startNode: Node, targetNode: Node) -> int:
        openList: List[PathNode] = []  # heapq
        # startNode is its own parent:
        openList.append(PathNode(startNode.heuristicPathLength(targetNode), 0, startNode, startNode))
        openListMap: Dict[Node, PathNode] = {}
        closeList: Dict[Node, PathNode] = {}
        while openList:
            print()
            print(openList)
            currentPathNode: PathNode = heapq.heappop(openList)
            print(currentPathNode)
            distanceFromStart: int = currentPathNode.distanceFromStart
            closeList[currentPathNode.node] = currentPathNode
            if currentPathNode.node == targetNode:
                # reached target
                print('target reached, distance', distanceFromStart)
                break
            else:
                neighbours: List[PathNode] = \
                    cls.findNeighbours(matrix, closeList, distanceFromStart, currentPathNode, targetNode)
                needsHeapify = False
                for neighbour in neighbours:  # all neighbours are not in closeList
                    if neighbour.node not in openListMap:
                        openList.append(neighbour)
                        openListMap[neighbour.node] = neighbour
                        needsHeapify = True
                        print('  ', neighbour, ' new', sep='')
                    else:
                        oldneighbour: PathNode = openListMap[neighbour.node]
                        if neighbour.pathLength < oldneighbour.pathLength:  # new neighbour has shorter total path
                            oldneighbour.pathLength = neighbour.pathLength
                            oldneighbour.distanceFromStart = neighbour.distanceFromStart
                            oldneighbour.parent = neighbour.parent
                            needsHeapify = True
                            print('  ', neighbour, ' updated', sep='')
                        else:
                            print('  ', neighbour, ' ignored, because not shorter', sep='')
                if needsHeapify:
                    print('will reorder heap')
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
                print('  Neighbour:', neighbourNode)
            if neighbourNode not in closeList:
                g = distanceFromStart + matrix.getWeight(neighbourNode)
                h = neighbourNode.heuristicPathLength(targetNode)
                f = g + h
                neighbourPathNode = PathNode(f, g, neighbourNode, currentPathNode.node)
                print('    ', neighbourPathNode, sep='')
                neighbours.append(neighbourPathNode)
            else:
                print('    ignored, because in closeList')
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
    targetNode = Node(len(weights[0]) - 1, len(weights) - 1)
    print(targetNode)

    matrix = Matrix(weights)
    distanceFromStart = MatrixAStar.findPath(matrix, startNode, targetNode)
    print(distanceFromStart)
