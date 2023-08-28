from typing import List, NamedTuple, Dict
from dataclasses import dataclass
import heapq


class Node(NamedTuple):

    x: int
    y: int

    def heuristicPathLength(self, target: 'Node') -> int:
        h = abs(target.x - self.x) + abs(target.y - self.y)  # Manhattan distance
        return h

    def __repr__(self) -> str:
        return f'({self.x}/{self.y})'


@dataclass(order=True)
class PathNode:

    pathLength: int
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
        openList.append(PathNode(0, startNode, startNode))  # startNode is its own parent
        openListMap: Dict[Node, PathNode] = {}
        closeList: Dict[Node, PathNode] = {}
        while openList:
            print(openList)
            currentPathNode: PathNode = heapq.heappop(openList)
            distanceFromStart: int = currentPathNode.pathLength
            if currentPathNode.node == targetNode:
                # reached target
                print("target reached, distance ", distanceFromStart)
                break
            else:
                closeList[currentPathNode.node] = currentPathNode
                neighbours: List[PathNode] = self.findNeighbours(closeList, distanceFromStart, currentPathNode, targetNode)
                needsHeapify = False
                for neighbour in neighbours:  # only neighbours not in closeList
                    if neighbour.node not in openListMap:
                        openList.append(neighbour)
                        openListMap[neighbour.node] = neighbour
                    else:
                        oldneighbour: PathNode = openListMap[neighbour.node]
                        if neighbour.pathLength < oldneighbour.pathLength:  # new neighbour has shorter path
                            oldneighbour.pathLength = neighbour.pathLength
                            oldneighbour.parent = neighbour.parent
                            needsHeapify = True
                if needsHeapify:
                    print('will reorder heap')
                    heapq.heapify(openList)
        return currentPathNode.pathLength

    def findNeighbours(self, closeList, distanceFromStart: int, currentPathNode: PathNode, targetNode: Node) \
            -> List[PathNode]:
        neighbours: List[PathNode] = []
        for offset in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # right, below, left, above
            neighbour = Node(currentPathNode.node.x + offset[0], currentPathNode.node.y + offset[1])
            print('Neighbour:', neighbour)
            if neighbour.x == self._maxx + 1 or neighbour.y == self._maxy + 1 or neighbour.x == 0 or neighbour.y == 0:
                continue  # ignore frame of 9s
            if neighbour not in closeList:
                g = distanceFromStart + self._weights[neighbour.y][neighbour.x]
                h = neighbour.heuristicPathLength(targetNode)
                f = g + h
                neighbours.append(PathNode(f, neighbour, currentPathNode.node))
        return neighbours


if __name__ == '__main__':
    weightsstring = \
        '1163751742,1381373672,2136511328,3694931569,7463417111,1319128137,1359912421,3125421639,1293138521,2311944581'
    weights: List[List[int]] = [list(map(int, list(row))) for row in weightsstring.split(',')]
    graph = Graph(weights)
    distanceFromStart = graph.findPath(Node(1, 1), Node(10, 10))  # consider additional frame with 9s
    print(distanceFromStart)
