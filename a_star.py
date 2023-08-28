from typing import List, NamedTuple, Dict
from dataclasses import dataclass
import heapq


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
        return f'({self.pathLength};{self.node};{self.parent})'


class Graph:

    def __init__(self, weights: List[List[int]]) -> None:
        self._maxx = len(weights[0])
        self._maxy = len(weights)
        self._weights: List[List[int]] = []
        self._weights.append([9] * (1 + self._maxx + 1))
        self._weights.extend([[9] + weights2 + [9] for weights2 in weights])
        self._weights.append([9] * (1 + self._maxx + 1))
        print(self._weights)

    def findPath(self, startNode: Node, targetNode: Node) -> int:
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
            if currentPathNode.node == targetNode:
                # reached target
                print('target reached, distance', distanceFromStart)
                break
            else:
                closeList[currentPathNode.node] = currentPathNode
                neighbours: List[PathNode] = self.findNeighbours(closeList, distanceFromStart, currentPathNode, targetNode)
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
                            oldneighbour.parent = neighbour.parent
                            needsHeapify = True
                            print('  ', neighbour, ' updated', sep='')
                        else:
                            print('  ', neighbour, ' ignored, because not shorter', sep='')
                if needsHeapify:
                    print('will reorder heap')
                    heapq.heapify(openList)
        return currentPathNode.pathLength

    def findNeighbours(self, closeList, distanceFromStart: int, currentPathNode: PathNode, targetNode: Node) \
            -> List[PathNode]:
        neighbours: List[PathNode] = []
        for offset in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # right, below, left, above
            neighbourNode = Node(currentPathNode.node.x + offset[0], currentPathNode.node.y + offset[1])
            if neighbourNode.x == self._maxx + 1 or neighbourNode.y == self._maxy + 1 \
                    or neighbourNode.x == 0 or neighbourNode.y == 0:
                continue  # ignore coordinates outside of the matrix
            else:
                print('  Neighbour:', neighbourNode)
            if neighbourNode not in closeList:
                g = distanceFromStart + self._weights[neighbourNode.y][neighbourNode.x]
                h = neighbourNode.heuristicPathLength(targetNode)
                f = g + h
                neighbourPathNode = PathNode(f, g, neighbourNode, currentPathNode.node)
                print('    ', neighbourPathNode, sep='')
                neighbours.append(neighbourPathNode)
            else:
                print('    ignored, because in closeList')
        return neighbours


if __name__ == '__main__':
    weightsstring = \
        '1163751742,1381373672,2136511328,3694931569,7463417111,1319128137,1359912421,3125421639,1293138521,2311944581'
    startNode = Node(1, 1)
    targetNode = Node(10, 10)
    # -> distance: 40

    # weightsstring = '1163,1381,2136'
    # startNode = Node(1, 1)
    # targetNode = Node(4, 3)
    # -> distance: 13

    # weightsstring = '116,138,213'
    # startNode = Node(1, 1)
    # targetNode = Node(3, 3)
    # -> distance: 7

    # weightsstring = '12,13'
    # startNode = Node(1, 1)
    # targetNode = Node(2, 2)
    # -> distance: 4

    weights: List[List[int]] = [list(map(int, list(row))) for row in weightsstring.split(',')]
    graph = Graph(weights)
    distanceFromStart = graph.findPath(startNode, targetNode)  # consider additional frame with 9s
    print(distanceFromStart)
